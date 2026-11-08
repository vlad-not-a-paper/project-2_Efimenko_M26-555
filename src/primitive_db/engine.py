from .utils import load_metadata, save_metadata
from .core import create_table, drop_table

import prompt
import shlex

META_FILE = "db_meta.json"

def welcome():
    """Prints the first message for the current mode."""

    print('project')
    print('\nПервая попытка запустить проект!')
    print('\n***')
    print('\n<command> exit - выйти из программы')
    print('<command> help - справочная информация')
    while True:
        input_command = prompt.string('Введите команду: ')
        if input_command == 'help':
            print_help()
        elif input_command == 'exit':
            break
        else:
            print('Неправильно введена команда')

def run():
    # welcome()
    print_help()
    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string('>>>Введите команду: ')
        args = shlex.split(user_input)
        command = args[0]
        match command:
            case 'create_table':
                table_name = args[1]
                columns = args[2:]
                create_table(metadata, table_name, columns)
            case 'drop_table':
                table_name = args[1]
                drop_table(metadata, table_name)
        save_metadata(META_FILE, metadata)

def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")