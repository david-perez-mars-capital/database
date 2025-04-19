# Database Utility

A database connection utility for MS SQL Server that simplifies connecting to databases and executing queries.

## Installation

### From local source
```bash
pip install .
```

### From repository
```bash
# Install directly from the repository
pip install git+hhttps://github.com/david-perez-mars-capital/database.git

# Or clone and install
git clone https://github.com/david-perez-mars-capital/database
cd database
pip install .
```

## Configuration

This package requires the following environment variables to connect to a database:

| Variable | Description |
|----------|-------------|
| DB_DRIVER | The ODBC driver (e.g., "ODBC Driver 17 for SQL Server") |
| DB_SERVER | Server address |
| DB_DATABASE | Database name |
| DB_USER | Username |
| DB_PASSWORD | Password |

You can set these variables in a `.env` file with the following format:

```
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_SERVER=your-server.database.windows.net
DB_DATABASE=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

## Usage

### Basic Usage

```python
from database import Database

# Initialize database connection using .env file in current directory
db = Database()

# Or specify a custom path to your .env file
db = Database(env_path="/path/to/your/.env")

# Load environment variables separately
from database import load_env_from_path
load_env_from_path("/path/to/your/.env")
```

### Executing SQL Files

```python
# Execute a SQL file with parameters
results = db.execute_sql_file(
    path="sql",
    sql_file="your_query.sql",
    params={"param1": "value1"}
)
```

### Loading Data into Pandas

```python
# Load data from a query into a pandas DataFrame
df = db.load_data_from_query("SELECT * FROM your_table")
```
