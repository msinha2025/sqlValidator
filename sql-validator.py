import re

DDL_COMMANDS = {"CREATE", "ALTER", "DROP", "TRUNCATE", "RENAME"}
DML_COMMANDS = {"SELECT", "INSERT", "UPDATE", "DELETE", "MERGE"}
DCL_COMMANDS = {"GRANT", "REVOKE"}
ALL_COMMANDS = DDL_COMMANDS | DML_COMMANDS | DCL_COMMANDS

def load_allowed_tables(filename):
    with open(filename, "r") as f:
        return set(line.strip() for line in f if line.strip())

def extract_table_names(sql):
    pattern = r"\b(?:FROM|JOIN|UPDATE|INTO|DELETE\s+FROM|CREATE\s+TABLE|ALTER\s+TABLE|DROP\s+TABLE|TRUNCATE\s+TABLE|RENAME\s+TABLE|ON)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
    return set(re.findall(pattern, sql, re.IGNORECASE))

def get_sql_command(sql):
    match = re.match(r"^\s*([a-zA-Z]+)", sql)
    if match:
        return match.group(1).upper()
    return None

def basic_syntax_check(sql, command):
    if command == "SELECT":
        has_select = re.search(r"\bSELECT\b", sql, re.IGNORECASE)
        has_from = re.search(r"\bFROM\b\s+[a-zA-Z_][a-zA-Z0-9_]*", sql, re.IGNORECASE)
        if not has_select:
            return False
        if has_from:
            return True
        # Accept SELECT statements without FROM if they only use functions/literals
        select_expr = re.sub(r"^\s*SELECT\s*", "", sql, flags=re.IGNORECASE).strip().rstrip(";")
        # Accept if select_expr is a function call or literal (no spaces, no commas, or only function calls)
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)$", select_expr) or select_expr.isdigit():
            return True
        return False
    elif command == "INSERT":
        # INSERT INTO <table> (...) VALUES (...)
        if not re.search(r"\bINSERT\b\s+INTO\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(.+\)\s*VALUES\s*\(.+\)", sql, re.IGNORECASE):
            return False
    elif command == "UPDATE":
        # UPDATE <table> SET ... WHERE ...
        if not re.search(r"\bUPDATE\b\s+[a-zA-Z_][a-zA-Z0-9_]*\s+SET\s+.+\s+WHERE\s+.+", sql, re.IGNORECASE):
            return False
    elif command == "CREATE":
        # CREATE TABLE <table> (...)
        if not re.search(r"\bCREATE\b\s+TABLE\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(.+\)", sql, re.IGNORECASE):
            return False
    return True

def validate_sql(sql, allowed_tables):
    command = get_sql_command(sql)
    if not command or command not in ALL_COMMANDS:
        return "INVALID SYNTAX", set()
    referenced_tables = extract_table_names(sql)
    # For DML/DDL, must reference at least one table unless SELECT is function/literal only
    if command in DML_COMMANDS | DDL_COMMANDS:
        if command == "SELECT":
            if not basic_syntax_check(sql, command):
                return f"INVALID SYNTAX for {command}", set()
            # If SELECT has FROM, check table reference
            if re.search(r"\bFROM\b", sql, re.IGNORECASE):
                if not referenced_tables:
                    return "INVALID SYNTAX - No table referenced", set()
                disallowed = referenced_tables - allowed_tables
                if disallowed:
                    return f"INVALID - Disallowed table(s): {', '.join(disallowed)}", disallowed
        else:
            if not referenced_tables:
                return "INVALID SYNTAX - No table referenced", set()
            disallowed = referenced_tables - allowed_tables
            if disallowed:
                return f"INVALID - Disallowed table(s): {', '.join(disallowed)}", disallowed
            if command in {"INSERT", "UPDATE", "CREATE"}:
                if not basic_syntax_check(sql, command):
                    return f"INVALID SYNTAX for {command}", set()
    # For DCL, check for ON <table>
    if command in DCL_COMMANDS:
        if not referenced_tables:
            return "INVALID SYNTAX - No table referenced in DCL", set()
        disallowed = referenced_tables - allowed_tables
        if disallowed:
            return f"INVALID - Disallowed table(s): {', '.join(disallowed)}", disallowed
    return "VALID", set()

def validate_sql_file(sql_file, tables_file):
    allowed_tables = load_allowed_tables(tables_file)
    with open(sql_file, "r") as f:
        queries = f.read().split(";")
        for idx, query in enumerate(queries, 1):
            query = query.strip()
            if not query:
                continue
            result, disallowed = validate_sql(query, allowed_tables)
            print(f"Query {idx}: {result}")

if __name__ == "__main__":
    sql_file = input("Enter SQL file name: ").strip()
    tables_file = input("Enter allowed tables file name: ").strip()
    validate_sql_file(sql_file, tables_file)