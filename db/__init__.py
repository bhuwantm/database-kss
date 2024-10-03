import pyodbc

import settings as settings

def get_connection() -> pyodbc.Connection:
    return pyodbc.connect(settings.CONNECTION_STRING)
