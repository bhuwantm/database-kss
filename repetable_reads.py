import time
import random
import multiprocessing
from faker import Faker
from pyodbc import Connection

from db.utils import in_transaction


@in_transaction
def repetable_reads(conn: Connection):
    cursor = conn.cursor()
    count_one = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 1:", count_one[1])

    print("Sleeping for 10 seconds...")

    time.sleep(10)
    count_two = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 1:", count_two[1])


@in_transaction
def repetable_reads_modifier(conn: Connection):
    time.sleep(5)
    fake = Faker()
    cursor = conn.cursor()

    first_name = fake.first_name()
    print(first_name)
    
    update_student_query = f"""
    UPDATE dbo.student SET first_name = '{first_name}' WHERE id=1;
    """

    cursor.execute(update_student_query)
    print("Updated firstname for row with id 1 using transaction 2...")

    cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()


if __name__ == "__main__":
    # Creating processes
    process1 = multiprocessing.Process(target=repetable_reads)
    process2 = multiprocessing.Process(target=repetable_reads_modifier)

    # Starting processes
    process1.start()
    process2.start()

    # Waiting for processes to complete
    process1.join()
    process2.join()
