import time
import random
import multiprocessing
from faker import Faker
from pyodbc import Connection

from db.utils import in_transaction


@in_transaction
def phantom_reads(conn: Connection):
    cursor = conn.cursor()
    count_one = cursor.execute("SELECT COUNT(*) AS count FROM dbo.student").fetchone()
    print(f"First Count from transaction 1:", count_one[0])

    print("Sleeping for 10 seconds...")

    time.sleep(10)
    count_two = cursor.execute("SELECT COUNT(*) AS count FROM dbo.student").fetchone()
    print(f"Secound Count from transaction 1", count_two[0])


@in_transaction
def phantom_reads_modifier(conn: Connection):
    time.sleep(5)
    fake = Faker()
    cursor = conn.cursor()
    
    insert_student_query = f"""
    INSERT INTO student (first_name, last_name, roll_number, grade, address)
    VALUES ('{fake.first_name()}', '{fake.last_name()}', 'std-{random.randint(100000, 100050)}', '{random.randint(1, 10)}', '{fake.address()}');
    """


    cursor.execute(insert_student_query)
    print("Inserted a row into student table using transaction 2...")


if __name__ == "__main__":
    # Creating processes
    process1 = multiprocessing.Process(target=phantom_reads)
    process2 = multiprocessing.Process(target=phantom_reads_modifier)

    # Starting processes
    process1.start()
    process2.start()

    # Waiting for processes to complete
    process1.join()
    process2.join()
