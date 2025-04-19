"""
Database utility package for MS SQL Server.

This package provides tools for connecting to MS SQL Server databases and
executing queries using SQLAlchemy and pyodbc.

Classes:
    Database: Main class for database connections and query execution.

Functions:
    load_env_from_path: Utility function to load environment variables from a specified path.
"""

from .database import Database, load_env_from_path

__all__ = ['Database', 'load_env_from_path']
