# SQL Validator

This project is a SQL validator that checks SQL queries against a predefined list of allowed table names. The list of allowed table names is stored in `table.txt`, and the main validation logic is implemented in `src/validator.py`.

## Project Structure

```
sql-validator
├── src
│   ├── validator.py      # Main logic for SQL validation
│   └── utils
│       └── __init__.py   # Utility functions for the validator
├── table.txt             # List of allowed table names
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd sql-validator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Populate `table.txt` with the allowed table names, one per line.

## Usage

To validate a SQL query, run the validator script with the query as input. The validator will check the query against the allowed table names in `table.txt` and raise errors for any invalid table names.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.