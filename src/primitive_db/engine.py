import prompt
from prettytable import PrettyTable

from .constants import COMMAND_PROMPT, META_FILE
from .core import (
    check_clause,
    create_table,
    delete,
    drop_table,
    get_columns,
    insert,
    list_tables,
    select,
    table_exists,
    update,
)
from .decorators import handle_db_errors
from .parser import (
    parse_create_table,
    parse_delete,
    parse_insert,
    parse_select,
    parse_table_name,
    parse_update,
)
from .utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def welcome():
    """Prints the first message for the current mode."""

    print("project")
    print("\nПервая попытка запустить проект!")
    print("\n***")
    print("\n<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    while True:
        input_command = prompt.string("Введите команду: ")
        if input_command == "help":
            print_help()
        elif input_command == "exit":
            break
        else:
            print("Неправильно введена команда")


def run():
    """Runs the main loop of the database."""
    # welcome()
    print_help()
    while True:
        metadata = load_metadata(META_FILE)
        try:
            user_input = prompt.string(COMMAND_PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        command = user_input.split()[0]
        match command:
            case "create_table":
                handle_create_table(metadata, user_input)
            case "drop_table":
                handle_drop_table(metadata, user_input)
            case "list_tables":
                list_tables(metadata)
            case "info":
                handle_info(metadata, user_input)
            case "insert":
                handle_insert(metadata, user_input)
            case "select":
                handle_select(metadata, user_input)
            case "update":
                handle_update(metadata, user_input)
            case "delete":
                handle_delete(metadata, user_input)
            case "help":
                print_help()
            case "exit":
                break
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")


@handle_db_errors
def handle_create_table(metadata, user_input):
    """Handles the create_table command."""
    table_name, columns = parse_create_table(user_input)
    metadata = create_table(metadata, table_name, columns)
    if metadata is not None:
        save_metadata(META_FILE, metadata)


@handle_db_errors
def handle_drop_table(metadata, user_input):
    """Handles the drop_table command."""
    table_name = parse_table_name(user_input)
    metadata = drop_table(metadata, table_name)
    if metadata is not None:
        save_metadata(META_FILE, metadata)
        delete_table_data(table_name)


@handle_db_errors
def handle_info(metadata, user_input):
    """Handles the info command."""
    table_name = parse_table_name(user_input)
    if not table_exists(metadata, table_name):
        return
    table_data = load_table_data(table_name)
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(metadata[table_name])}")
    print(f"Количество записей: {len(table_data)}")


@handle_db_errors
def handle_insert(metadata, user_input):
    """Handles the insert command."""
    table_name, values = parse_insert(user_input)
    if not table_exists(metadata, table_name):
        return
    table_data = load_table_data(table_name)
    table_data = insert(metadata, table_name, values, table_data)
    if table_data is not None:
        save_table_data(table_name, table_data)


@handle_db_errors
def handle_select(metadata, user_input):
    """Handles the select command and prints the result as a table."""
    table_name, where_clause = parse_select(user_input)
    if not table_exists(metadata, table_name):
        return
    if where_clause is not None:
        check_clause(metadata, table_name, where_clause)
    table_data = load_table_data(table_name)
    records = select(table_data, where_clause)
    if records is not None:
        print_records(metadata, table_name, records)


@handle_db_errors
def handle_update(metadata, user_input):
    """Handles the update command."""
    table_name, set_clause, where_clause = parse_update(user_input)
    if not table_exists(metadata, table_name):
        return
    check_clause(metadata, table_name, set_clause)
    check_clause(metadata, table_name, where_clause)
    table_data = load_table_data(table_name)
    table_data = update(table_name, table_data, set_clause, where_clause)
    if table_data is not None:
        save_table_data(table_name, table_data)


@handle_db_errors
def handle_delete(metadata, user_input):
    """Handles the delete command."""
    table_name, where_clause = parse_delete(user_input)
    if not table_exists(metadata, table_name):
        return
    check_clause(metadata, table_name, where_clause)
    table_data = load_table_data(table_name)
    table_data = delete(table_name, table_data, where_clause)
    if table_data is not None:
        save_table_data(table_name, table_data)


def print_records(metadata, table_name, records):
    """Prints records as a pretty table."""
    if not records:
        print("Записи не найдены.")
        return
    column_names = list(get_columns(metadata, table_name))
    table = PrettyTable()
    table.field_names = column_names
    for record in records:
        table.add_row([record.get(column_name) for column_name in column_names])
    print(table)


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...)"
          " - создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение>"
          " - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1>"
          " where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение>"
          " - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")
