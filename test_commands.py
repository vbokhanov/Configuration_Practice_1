import unittest
from emulator import ShellEmulator
import calendar
import datetime

class TestShellBasics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.emulator = ShellEmulator('config.ini')
    
    def test_ls(self):
        self.assertIn('./file1.txt', self.emulator.ls())

    def test_touch(self):
        self.assertEqual(self.emulator.touch('new_file.txt'), 'Created file new_file.txt')

    def test_chown(self):
        self.assertEqual(self.emulator.chown('new_owner', './file1.txt'), 'Changed ownership of ./file1.txt to new_owner')

    def test_cal(self):
        now = datetime.datetime.now()
        expected_cal = calendar.month(now.year, now.month)
        self.assertEqual(self.emulator.cal(), expected_cal)

class TestShellCd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.emulator = ShellEmulator('config.ini')

    def test_cd(self):
        self.assertEqual(self.emulator.cd('./nonexistent_dir'), 'No such file or directory')
        self.assertEqual(self.emulator.cd('./dir1'), 'Changed directory to ./dir1')

class TestShellExit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.emulator = ShellEmulator('config.ini')

    def test_exit(self):
        self.assertEqual(self.emulator.exit(), 'Exiting shell emulator.')

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestShellBasics))
    suite.addTests(loader.loadTestsFromTestCase(TestShellCd))
    suite.addTests(loader.loadTestsFromTestCase(TestShellExit))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
