"""
Database connection utility for MS SQL Server.

This module provides a Database class for connecting to MS SQL Server databases
and executing queries. It also includes a utility function for loading
environment variables from a specified file path.

The module requires the following environment variables:
- DB_DRIVER: The ODBC driver (e.g., "ODBC Driver 17 for SQL Server")
- DB_SERVER: Server address
- DB_DATABASE: Database name
- DB_USER: Username
- DB_PASSWORD: Password
"""

import os
import logging
from typing import Optional, Any, List, Dict
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd

log = logging.getLogger(__name__)

def load_env_from_path(env_path: str) -> bool:
    """
    Load environment variables from a specific .env file path.
    
    Args:
        env_path: Path to the .env file
        
    Returns:
        bool: True if the .env file was loaded successfully, False otherwise
    """
    try:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            log.info(f"Environment variables loaded from: {env_path}")
            return True
        else:
            log.error(f"Environment file not found at: {env_path}")
            return False
    except Exception as e:
        log.error(f"Error loading environment variables: {str(e)}")
        return False

class Database:
    """
    Database connection utility for MS SQL Server.
    
    This class handles database connections and query execution using
    SQLAlchemy and pyodbc. It reads connection parameters from environment
    variables and provides methods for executing SQL queries and files.
    
    Attributes:
        driver (str): The ODBC driver name
        server (str): The server address
        database (str): The database name
        user (str): The username
        password (str): The password
        connection_string (str): The formatted connection string
        engine: The SQLAlchemy engine instance
    """
    
    def __init__(self, env_path: str = None):   
        """
        Initialize the Database object with connection parameters.
        
        Args:
            env_path (str, optional): Path to a .env file containing 
                database connection parameters. If None, tries to load
                from a .env file in the current directory.
        """
        if env_path:
            load_env_from_path(env_path)
        else:
            load_dotenv()
            
        self.driver = os.getenv("DB_DRIVER")
        self.server = os.getenv("DB_SERVER")
        self.database = os.getenv("DB_DATABASE")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.connection_string = (
                f"DRIVER={{{self.driver}}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.user};"
                f"PWD={self.password}"
            )
        self.engine = self.get_engine()

    def get_engine(self):
        """
        Create and return a SQLAlchemy engine instance.
        
        Returns:
            Engine: A SQLAlchemy engine instance
            
        Raises:
            Exception: If there's an error creating the engine
        """
        try:
            connection_url = self.get_connection_string()
            engine = create_engine(connection_url)
            return engine
        except Exception as e:
            log.error(f'Error in {self.get_engine.__name__}: {e}')
    
    def get_connection_string(self):
        """
        Create and return a SQLAlchemy connection URL.
        
        Returns:
            URL: A SQLAlchemy URL object for connecting to the database
        """
        return URL.create("mssql+pyodbc", query={"odbc_connect": self.connection_string})

    def execute_sql_file(self, path:str, sql_file: str, params: dict = None) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a SQL file with optional parameters.
        
        Args:
            path (str): Directory path containing the SQL file
            sql_file (str): Name of the SQL file
            params (dict, optional): Parameters to use in the SQL query
            
        Returns:
            Optional[List[Dict[str, Any]]]: Query results if available, None otherwise
            
        Raises:
            FileNotFoundError: If the SQL file doesn't exist
            Exception: For other errors during execution
        """
        file_path = os.path.join(path, sql_file)
        if params is None:
            params = {}
        try:
            sql_commands = self._read_sql_file(file_path)
            return self._execute_query(sql_commands, params)
        except FileNotFoundError as e:
            log.error(f"SQL file not found: {file_path}")
            raise
        except Exception as e:
            log.error(f"Error executing SQL file: {str(e)}")
            raise

    def _read_sql_file(self, file_path: str) -> str:
        """
        Read the contents of a SQL file.
        
        Args:
            file_path (str): Path to the SQL file
            
        Returns:
            str: Contents of the SQL file
            
        Raises:
            Exception: If there's an error reading the file
        """
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            log.error(f"Error reading SQL file: {str(e)}")
            raise

    def _execute_query(self, sql_commands: str, params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a SQL query with parameters.
        
        Args:
            sql_commands (str): SQL commands to execute
            params (Dict[str, Any]): Parameters for the SQL query
            
        Returns:
            Optional[List[Dict[str, Any]]]: Query results if available, None otherwise
            
        Raises:
            Exception: If there's an error executing the query
        """
        try:
            with self.engine.connect() as connection:
                with connection.begin():
                    result = connection.execute(text(sql_commands), params)
                    if result.returns_rows:
                        return result.fetchall()
                    return None
        except Exception as e:
            log.error(f"Error executing query: {str(e)}")
            raise
    
    def load_data_from_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and load the results into a pandas DataFrame.
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            pd.DataFrame: Query results as a pandas DataFrame
            
        Raises:
            Exception: If there's an error executing the query
        """
        try:
            with self.engine.begin() as conn:
                return pd.read_sql_query(text(query), conn)
        except Exception as e:
            log.error(f"Error executing query: {str(e)}")
            raise
