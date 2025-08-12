def read_allowed_tables(file_path):
    with open(file_path, 'r') as file:
        return {line.strip() for line in file if line.strip()}

def validate_sql_query(query, allowed_tables):
    # Simple SQL parsing to find table names (this is a basic implementation)
    import re
    pattern = r'\bFROM\s+(\w+)|\bJOIN\s+(\w+)'
    found_tables = re.findall(pattern, query, re.IGNORECASE)
    found_tables = {table for match in found_tables for table in match if table}

    invalid_tables = found_tables - allowed_tables
    if invalid_tables:
        raise ValueError(f"Invalid table names found in query: {', '.join(invalid_tables)}")

def main():
    allowed_tables = read_allowed_tables('table.txt')
    query = input("Enter your SQL query: ")
    
    try:
        validate_sql_query(query, allowed_tables)
        print("SQL query is valid.")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()