def read_allowed_tables(file_path):
    with open(file_path, 'r') as file:
        allowed_tables = {line.strip() for line in file if line.strip()}
    return allowed_tables

def is_table_allowed(table_name, allowed_tables):
    return table_name in allowed_tables