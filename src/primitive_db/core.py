from .constants import (
    COLUMN_SEPARATOR,
    FIRST_ID,
    ID_COLUMN,
    ID_TYPE,
    VALID_TYPES,
)
from .decorators import confirm_action, create_cacher, handle_db_errors, log_time

select_cache = create_cacher()


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Adds a new table with an ID column to the metadata."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
    elif not table_name.isidentifier():
        print(f"Некорректное значение: {table_name}. Попробуйте снова.")
    else:
        is_valid = True
        column_names = [ID_COLUMN]
        for column in columns:
            if column.count(COLUMN_SEPARATOR) == 1:
                column_name, column_type = column.split(COLUMN_SEPARATOR)
            else:
                print(f"Некорректное значение: {column}. Попробуйте снова.")
                is_valid = False
                break
            if not column_name.isidentifier() or column_name in column_names:
                print(f"Некорректное значение: {column_name}. Попробуйте снова.")
                is_valid = False
                break
            if column_type not in VALID_TYPES:
                print(f"Некорректное значение: {column_type}. Попробуйте снова.")
                is_valid = False
                break
            column_names.append(column_name)
        table_columns = [f"{ID_COLUMN}{COLUMN_SEPARATOR}{ID_TYPE}"]
        if is_valid:
            table_columns.extend(columns)
            metadata[table_name] = table_columns
            columns_str = ", ".join(table_columns)
            print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Removes a table from the metadata."""
    if table_name in metadata:
        del metadata[table_name]
        print(f'Таблица "{table_name}" успешно удалена.')
    else:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
    return metadata


def list_tables(metadata):
    """Prints the names of all tables."""
    if not metadata:
        print("Таблиц пока нет.")
    for table_name in metadata:
        print(f"- {table_name}")


def table_exists(metadata, table_name):
    """Checks that the table exists and prints an error if it does not."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return False
    return True


def get_columns(metadata, table_name):
    """Returns a dict of table columns like {'ID': 'int', 'name': 'str'}."""
    columns = {}
    for column in metadata[table_name]:
        column_name, column_type = column.split(COLUMN_SEPARATOR)
        columns[column_name] = column_type
    return columns


def check_value(column_type, value):
    """Raises ValueError if the value does not match the column type."""
    if type(value) is not VALID_TYPES[column_type]:
        raise ValueError(value)


def check_clause(metadata, table_name, clause):
    """Checks that clause columns exist and values have the right types."""
    columns = get_columns(metadata, table_name)
    for column_name, value in clause.items():
        if column_name not in columns:
            raise KeyError(column_name)
        check_value(columns[column_name], value)


def is_matching(record, where_clause):
    """Checks that the record matches every condition of the where clause."""
    for column_name, value in where_clause.items():
        if record.get(column_name) != value:
            return False
    return True


@handle_db_errors
@log_time
def insert(metadata, table_name, values, table_data):
    """Validates values and adds a new record with a generated ID."""
    columns = get_columns(metadata, table_name)
    del columns[ID_COLUMN]
    if len(values) != len(columns):
        print(f"Ошибка: Таблица \"{table_name}\" ожидает {len(columns)} "
              f"значений, получено {len(values)}.")
        return None
    record_id = FIRST_ID
    if table_data:
        record_id = max(record[ID_COLUMN] for record in table_data) + 1
    record = {ID_COLUMN: record_id}
    for column_name, value in zip(columns, values):
        check_value(columns[column_name], value)
        record[column_name] = value
    table_data.append(record)
    print(f'Запись с ID={record_id} успешно добавлена в таблицу "{table_name}".')
    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Returns all records or only the ones that match the where clause."""
    if where_clause is None:
        return table_data
    cache_key = f"{table_data}{where_clause}"

    def find_records():
        records = []
        for record in table_data:
            if is_matching(record, where_clause):
                records.append(record)
        return records

    return select_cache(cache_key, find_records)


@handle_db_errors
def update(table_name, table_data, set_clause, where_clause):
    """Updates fields of the records that match the where clause."""
    if ID_COLUMN in set_clause:
        raise ValueError(ID_COLUMN)
    is_found = False
    for record in table_data:
        if is_matching(record, where_clause):
            record.update(set_clause)
            is_found = True
            print(f'Запись с ID={record[ID_COLUMN]} в таблице "{table_name}" '
                  f'успешно обновлена.')
    if not is_found:
        print("Записи, подходящие под условие, не найдены.")
    return table_data


@handle_db_errors
@confirm_action("удаление записи")
def delete(table_name, table_data, where_clause):
    """Deletes the records that match the where clause."""
    remaining_records = []
    is_found = False
    for record in table_data:
        if is_matching(record, where_clause):
            is_found = True
            print(f'Запись с ID={record[ID_COLUMN]} успешно удалена из таблицы '
                  f'"{table_name}".')
        else:
            remaining_records.append(record)
    if not is_found:
        print("Записи, подходящие под условие, не найдены.")
    return remaining_records
