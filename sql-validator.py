import re

def load_allowed_tables(filename="tablenames.txt"):
    with open(filename, "r") as f:
        return set(line.strip() for line in f if line.strip())

def extract_table_names(sql):
    # Simple regex for table names after FROM, JOIN, UPDATE, INTO
    pattern = r"\b(?:FROM|JOIN|UPDATE|INTO)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
    return set(re.findall(pattern, sql, re.IGNORECASE))

def validate_sql(sql, allowed_tables):
    referenced_tables = extract_table_names(sql)
    disallowed = referenced_tables - allowed_tables
    if disallowed:
        print(f"Disallowed table(s) referenced: {', '.join(disallowed)}")
        return False
    print("SQL is valid.")
    return True

if __name__ == "__main__":
    allowed_tables = load_allowed_tables("table.txt")
    sql = input("Enter SQL query: ")
    validate_sql(sql, allowed_tables)