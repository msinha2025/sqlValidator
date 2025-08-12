import re

def load_allowed_tables(filename="tablenames.txt"):
    with open(filename, "r") as f:
        return set(line.strip() for line in f if line.strip())

def extract_table_names(sql):
    pattern = r"\b(?:FROM|JOIN|UPDATE|INTO)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
    return set(re.findall(pattern, sql, re.IGNORECASE))

def validate_sql(sql, allowed_tables):
    referenced_tables = extract_table_names(sql)
    disallowed = referenced_tables - allowed_tables
    if disallowed:
        return False, disallowed
    return True, set()

def validate_sql_file(sql_file, tables_file):
    allowed_tables = load_allowed_tables(tables_file)
    with open(sql_file, "r") as f:
        queries = f.read().split(";")
        for idx, query in enumerate(queries, 1):
            query = query.strip()
            if not query:
                continue
            valid, disallowed = validate_sql(query, allowed_tables)
            if valid:
                print(f"Query {idx}: VALID")
            else:
                print(f"Query {idx}: INVALID - Disallowed table(s): {', '.join(disallowed)}")

if __name__ == "__main__":
    validate_sql_file("validateSql.sql", "tablenames.txt")