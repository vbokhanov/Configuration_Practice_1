## Эмулятор консоли

### Поддерживаемые команды

- **ls** - вывод текущей директории
- **cd** - смена текущей директории
- **touch** - см [wiki](https://ru.wikipedia.org/wiki/Touch)
- **cal** - выводит календаря на текущий месяц
- **chown** - смена владельца файла
- **exit** - выход из эмулятора

### Тестирование
Производилось с помощью ```unittest```. Запуск тестов - ```python3 test_commands.py```

<img src="img/tests_result.png" width="500"/>

### Ручной запуск
```python3 run.py``` запускает эмулятор в стандартном режиме

<img src="img/run_example.png" width="500"/>

<img src="img/run_example2.png" width="500"/>

### Логи
Логи пишутся в файл ```log.csv```

<img src="img/logs.png" width="500"/>

### Тестовая папка
Запускаемый тест имеет вид

<img src="img/test_folder.png" width="300"/>