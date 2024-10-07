import time
import random
import multiprocessing
from faker import Faker
from pyodbc import Connection

from db.utils import in_transaction

@in_transaction
def deadlock(conn: Connection):
    cursor = conn.cursor()
    fake = Faker()

    update_student_query = f"""
    UPDATE dbo.student SET first_name = '{fake.first_name()}' WHERE id=1;
    """

    print('Exclusive lock is acquired on the row with id 1 using transaction 1.')
    cursor.execute(update_student_query)
    print("Updated firstname for row with id 1 using transaction 1...")

    print("Sleeping for 5 seconds...", '\n')
    time.sleep(5)

    print('Getting values of row 2 from transaction 1.', '\n')
    cursor.execute("SELECT * FROM dbo.student where id = 2").fetchone()




@in_transaction
def deadlock_modifier(conn: Connection):
    time.sleep(1)
    cursor = conn.cursor()
    fake = Faker()

    update_student_query = f"""
    UPDATE dbo.student SET first_name = '{fake.first_name()}' WHERE id=2;
    """

    print('Exclusive lock is acquired on the row with id 2 using transaction 2.')
    cursor.execute(update_student_query)
    print("Updated firstname for row with id 2 using transaction 2...")

    print("Sleeping for 5 seconds...",'\n')
    time.sleep(5)

    print('Getting values of row 1 from transaction 2.', '\n')
    cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()


if __name__ == "__main__":
    # Creating processes
    process1 = multiprocessing.Process(target=deadlock)
    process2 = multiprocessing.Process(target=deadlock_modifier)

    # Starting processes
    process1.start()
    process2.start()

    # Waiting for processes to complete
    process1.join()
    process2.join()
