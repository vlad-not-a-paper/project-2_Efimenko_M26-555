import shlex

from .constants import (
    BOOL_VALUES,
    CONDITION_SEPARATOR,
    QUOTES,
    SET_KEYWORD,
    VALUES_SEPARATOR,
    WHERE_KEYWORD,
)


def split_outside_quotes(text, separator):
    """Splits text by separator, but ignores separators inside quotes."""
    parts = []
    current = ""
    quote = None
    i = 0
    while i < len(text):
        char = text[i]
        if quote:
            if char == quote:
                quote = None
            current += char
            i += 1
        elif char in QUOTES:
            quote = char
            current += char
            i += 1
        elif text.startswith(separator, i):
            parts.append(current)
            current = ""
            i += len(separator)
        else:
            current += char
            i += 1
    if quote:
        raise ValueError(text)
    parts.append(current)
    return parts


def parse_value(raw_value):
    """Turns a string like '"Sergei"', '28' or 'true' into a Python value."""
    value = raw_value.strip()
    if len(value) >= 2 and value[0] in QUOTES and value[-1] == value[0]:
        return value[1:-1]
    if value.lower() in BOOL_VALUES:
        return BOOL_VALUES[value.lower()]
    try:
        return int(value)
    except ValueError:
        raise ValueError(value) from None


def parse_condition(condition):
    """Turns a string like 'age = 28' into a dict like {'age': 28}."""
    parts = split_outside_quotes(condition, CONDITION_SEPARATOR)
    if len(parts) != 2 or not parts[0].strip():
        raise ValueError(condition.strip())
    column = parts[0].strip()
    return {column: parse_value(parts[1])}


def parse_set_clause(set_text):
    """Turns a string like 'age = 29, name = "Ivan"' into a dict."""
    set_clause = {}
    for condition in split_outside_quotes(set_text, VALUES_SEPARATOR):
        set_clause.update(parse_condition(condition))
    return set_clause


def parse_values(values_text):
    """Turns a string like '("Sergei", 28, true)' into a list of values."""
    text = values_text.strip()
    if not (text.startswith("(") and text.endswith(")")):
        raise ValueError(text)
    inner_text = text[1:-1]
    values = []
    for raw_value in split_outside_quotes(inner_text, VALUES_SEPARATOR):
        values.append(parse_value(raw_value))
    return values


def split_where(user_input):
    """Splits a command into the part before 'where' and the where clause."""
    parts = split_outside_quotes(user_input, WHERE_KEYWORD)
    if len(parts) > 2:
        raise ValueError(user_input)
    if len(parts) == 1:
        return parts[0], None
    return parts[0], parse_condition(parts[1])


def parse_create_table(user_input):
    """Parses 'create_table <table> <col:type> ...' into name and columns."""
    args = shlex.split(user_input)
    if len(args) < 3:
        raise ValueError(user_input)
    return args[1], args[2:]


def parse_table_name(user_input):
    """Parses commands like 'drop_table <table>' or 'info <table>'."""
    args = shlex.split(user_input)
    if len(args) != 2:
        raise ValueError(user_input)
    return args[1]


def parse_insert(user_input):
    """Parses 'insert into <table> values (...)' into name and values."""
    parts = user_input.split(maxsplit=4)
    if len(parts) != 5 or parts[1] != "into" or parts[3] != "values":
        raise ValueError(user_input)
    return parts[2], parse_values(parts[4])


def parse_select(user_input):
    """Parses 'select from <table> [where ...]' into name and where clause."""
    head, where_clause = split_where(user_input)
    parts = head.split()
    if len(parts) != 3 or parts[1] != "from":
        raise ValueError(user_input)
    return parts[2], where_clause


def parse_update(user_input):
    """Parses 'update <table> set ... where ...' into name, set and where."""
    head, where_clause = split_where(user_input)
    if where_clause is None:
        raise ValueError(user_input)
    parts = split_outside_quotes(head, SET_KEYWORD)
    if len(parts) != 2:
        raise ValueError(user_input)
    command_parts = parts[0].split()
    if len(command_parts) != 2:
        raise ValueError(user_input)
    return command_parts[1], parse_set_clause(parts[1]), where_clause


def parse_delete(user_input):
    """Parses 'delete from <table> where ...' into name and where clause."""
    head, where_clause = split_where(user_input)
    parts = head.split()
    if where_clause is None or len(parts) != 3 or parts[1] != "from":
        raise ValueError(user_input)
    return parts[2], where_clause
