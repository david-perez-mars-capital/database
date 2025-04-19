from setuptools import setup, find_packages

setup(
    name="database",
    version="0.1.0",
    description="A database connection utility for MS SQL Server",
    author="David Perez",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "python-dotenv>=1.0.0",
        "sqlalchemy>=2.0.23",
        "pyodbc>=4.0.39",
        "pandas>=2.1.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 