def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
    else:
        flag = True
        for column in columns:
            if column.count(':') == 1:
                column_type = column.split(':')[1]
            else:
                print(f'Некорректное значение: {column}. Попробуйте снова.')
                flag = False
                break
            if column_type not in ['int', 'str', 'bool']:
                print(f'Некорректное значение: {column_type}. Попробуйте снова.')
                flag = False
                break
        table_columns = ['ID:int']
        if flag:
            table_columns.extend(columns)
            metadata[table_name] = table_columns
            columns_str = ', '.join(table_columns)
            print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    return metadata

def drop_table(metadata, table_name):
    if table_name in metadata:
        del metadata[table_name]
        print(f'Таблица "{table_name}" успешно удалена.')
    else:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
    return metadata