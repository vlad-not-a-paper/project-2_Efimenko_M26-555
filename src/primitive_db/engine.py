def welcome():
    output = []
    output.append('Первая попытка запустить проект!')
    output.append('')
    output.append('***')
    output.append('<command> exit - выйти из программы')
    output.append('<command> help - справочная информация')
    output.append('Введите команду: help')
    output.append('')
    output.append('<command> exit - выйти из программы')
    output.append('<command> help - справочная информация')
    output.append('Введите команду: _')
    return '\n'.join(output)

def run():
    while True:
        pass

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