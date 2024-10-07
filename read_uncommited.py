import time
import multiprocessing
from faker import Faker
from pyodbc import Connection

from db.utils import in_transaction


@in_transaction
def read_uncommited(conn: Connection):
    conn.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;")

    cursor = conn.cursor()
    count_one = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 1:", count_one[1])

    print("Sleeping for 5 seconds...", '\n')

    time.sleep(5)
    count_two = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 1:", count_two[1], '\n')


@in_transaction
def read_uncommited_modifier(conn: Connection):
    conn.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;")

    time.sleep(1)
    fake = Faker()
    cursor = conn.cursor()
    
    update_student_query = f"""
    UPDATE dbo.student SET first_name = '{fake.first_name()}' WHERE id=1;
    """

    print('Exclusive lock is acquired on the row with id 1 using transaction 2.')
    cursor.execute(update_student_query)
    print("Updated firstname for row with id 1 using transaction 2...", '\n')

    time.sleep(10)
    print("Committing transaction 2 ....")


if __name__ == "__main__":
    # Creating processes
    process1 = multiprocessing.Process(target=read_uncommited)
    process2 = multiprocessing.Process(target=read_uncommited_modifier)

    # Starting processes
    process1.start()
    process2.start()

    # Waiting for processes to complete
    process1.join()
    process2.join()
