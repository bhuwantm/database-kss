import time
import random
import multiprocessing
from faker import Faker
from pyodbc import Connection

from db.utils import in_transaction


@in_transaction
def exclusive_locks(conn: Connection):
    time.sleep(1)
    print('Transaction 1 started...','\n')
    fake = Faker()
    cursor = conn.cursor()

    count_one = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 1:", count_one[1], '\n')
    
    update_student_query = f"""
    UPDATE dbo.student SET first_name = '{fake.first_name()}' WHERE id=1;
    """

    print('Exclusive lock is acquired on the row with id 1.')
    cursor.execute(update_student_query)
    print("Updated firstname for row with id 1 using transaction 1...")

    count = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 1:", count[1], '\n')

    print("Sleeping for 10 seconds...", '\n')
    time.sleep(10)
    print("Exclusive lock is released from transaction 1.", '\n')



@in_transaction
def exclusive_locks_modifier(conn: Connection):
    time.sleep(3)
    print('Transaction 2 started...','\n')
    fake = Faker()
    cursor = conn.cursor()
    
    update_student_query = f"""
    UPDATE dbo.student SET first_name = '{fake.first_name()}{random.randint(10, 100)}' WHERE id=1;
    """

    cursor.execute(update_student_query)
    print("Updated firstname for row with id 1 using transaction 2...")

    count_one = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 2:", count_one[1], '\n')



if __name__ == "__main__":
    # Creating processes
    process1 = multiprocessing.Process(target=exclusive_locks)
    process2 = multiprocessing.Process(target=exclusive_locks_modifier)

    # Starting processes
    process1.start()
    process2.start()

    # Waiting for processes to complete
    process1.join()
    process2.join()
