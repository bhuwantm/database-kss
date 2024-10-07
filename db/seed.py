import random
from faker import Faker
from pyodbc import Connection

from db.utils import in_transaction


@in_transaction
def create_tables(conn: Connection):
    create_student_query = """
    CREATE TABLE student (
        id INT IDENTITY(1,1) PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        roll_number VARCHAR(255) NOT NULL,
        grade TINYINT NOT NULL CHECK (grade BETWEEN 1 AND 10),
        address VARCHAR(255) NULL
    );
    """

    create_subject_query = """
    CREATE TABLE subject (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(500) NULL
    );
    """

    cursor = conn.cursor()
    cursor.execute(create_student_query)
    cursor.execute(create_subject_query)
    print("Competed creating tables.")


@in_transaction
def drop_tables(conn: Connection):
    drop_student_query = "DROP TABLE student;"
    drop_subject_query = "DROP TABLE subject;"

    cursor = conn.cursor()
    cursor.execute(drop_student_query)
    cursor.execute(drop_subject_query)


@in_transaction
def insert_data(conn: Connection):
    data_count = 10000
    fake = Faker()
    cursor = conn.cursor()

    # Insert data into student table
    print("Inserting data into student table...")

    for i in range(0, data_count):
        print(f"Inserting row {i} of {data_count}... \r", end="", flush=True)

        insert_student_query = f"""
        INSERT INTO student (first_name, last_name, roll_number, grade, address)
        VALUES ('{fake.first_name()}', '{fake.last_name()}', 'std-{i}', '{random.randint(1, 10)}', '{fake.address()}');
        """
        cursor.execute(insert_student_query)

    print(f"Completed inserting {data_count} number of rows into student table.")


def seed():
    create_tables()
    insert_data()


def unseed():
    drop_tables()
