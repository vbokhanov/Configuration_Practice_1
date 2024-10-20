import os
import tarfile
import configparser
import csv
import calendar
import datetime
from pathlib import Path

class ShellEmulator:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        self.username = self.config['DEFAULT']['username']
        self.hostname = self.config['DEFAULT']['hostname']
        self.fs_archive = self.config['DEFAULT']['filesystem']
        self.log_file = self.config['DEFAULT']['logfile']
        
        self.current_directory = "/"
        self.filesystem = {}
        self.load_filesystem()

        file_path = Path(self.log_file)
        file_path.touch(exist_ok=True)

    def load_filesystem(self):
        with tarfile.open(self.fs_archive, 'r') as tar:
            for member in tar.getmembers():
                self.filesystem[member.name] = member
                if member.isdir():
                    self.filesystem[member.name] = {'type': 'dir', 'contents': []}
                else:
                    parent_dir = os.path.dirname(member.name)
                    if parent_dir in self.filesystem and 'contents' in self.filesystem[parent_dir]:
                        self.filesystem[parent_dir]['contents'].append(member.name)
                    self.filesystem[member.name] = {'type': 'file'}
    def log_action(self, action):
        with open(self.log_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([datetime.datetime.now(), self.username, action])

    def ls(self):
        current_dir = self.current_directory.strip("/")
        if len(current_dir) == 0:
            current_dir = '.'
        contents = []
        if current_dir in self.filesystem:
            contents = self.filesystem[current_dir]['contents']
        return contents

    def cd(self, path):
        if not path.startswith('.'):
            path = './'+ path
        if path == "..":
            self.current_directory = os.path.dirname(self.current_directory)
            self.log_action(f'cd {path}')
            return f'Changed directory to {self.current_directory}'
        elif path in self.filesystem and self.filesystem[path]['type'] == 'dir':
            self.current_directory = path
            self.log_action(f'cd {path}')
            return f'Changed directory to {path}'
        return 'No such file or directory'

    def touch(self, filename):
        new_file_path = os.path.join(self.current_directory, filename)
        if new_file_path not in self.filesystem:
            self.filesystem[new_file_path] = {'type': 'file'}
            parent_dir = os.path.dirname(new_file_path)
            if parent_dir in self.filesystem and 'contents' in self.filesystem[parent_dir]:
                self.filesystem[parent_dir]['contents'].append(new_file_path)
            self.log_action(f'touch {filename}')
            return f'Created file {filename}'
        else:
            return f'File {filename} already exists.'

    def cal(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month


        cal_text = calendar.month(year, month)
        self.log_action('cal')
        return cal_text

    def chown(self, user, filename):
        if not filename.startswith('.'):
            filename = './'+ filename
        if filename in self.filesystem and self.filesystem[filename]['type'] == 'file':
            self.log_action(f'chown {user} {filename}')
            return f'Changed ownership of {filename} to {user}'
        else:
            return f'File {filename} not found.'

    def exit(self):
        self.log_action('exit')
        return 'Exiting shell emulator.'

    def run(self):
        while True:
            command = input(f"{self.username}@{self.hostname}:{self.current_directory}$ ")
            parts = command.split()
            if not parts:
                continue
            
            cmd = parts[0]
            if cmd == 'ls':
                print(*[path.split('/')[-1] for path in self.ls()])
            elif cmd == 'cd':
                if len(parts) > 1:
                    print(self.cd(parts[1]))
                else:
                    print("cd: missing argument")
            elif cmd == 'touch':
                if len(parts) > 1:
                    print(self.touch(parts[1]))
                else:
                    print("touch: missing argument")
            elif cmd == 'cal':
                print(self.cal())
            elif cmd == 'chown':
                print(self.chown(parts[1], parts[2]))
            elif cmd == 'exit':
                print(self.exit())
                exit(0)
            else:
                print(f"{cmd}: command not found")
