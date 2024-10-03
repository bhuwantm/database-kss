from dotenv import dotenv_values

config = dotenv_values(".env")

# Database connection configuration
SERVER = config['SERVER']
DATABASE = config['DATABASE']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
PORT = config['PORT']

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER},{PORT};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    "Pooling=True;"
    "Max Pool Size=100;"
)
