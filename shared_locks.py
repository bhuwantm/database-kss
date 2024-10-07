import time
import random
import multiprocessing
from faker import Faker
from pyodbc import Connection

from db.utils import in_transaction

@in_transaction
def shared_locks(conn: Connection):
    cursor = conn.cursor()
    
    print('Shared locks are acquired on the row with id 1.')

    count_one = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 1:", count_one[1])

    print('Shared locks are released but transaction is not yet committed.')

    print("Sleeping for 5 seconds...")
    time.sleep(5)


    count_two = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 1:", count_two[1])


@in_transaction
def shared_locks_modifier(conn: Connection):
    time.sleep(1)
    fake = Faker()
    cursor = conn.cursor()
    
    update_student_query = f"""
    UPDATE dbo.student SET first_name = '{fake.first_name()}' WHERE id=1;
    """

    print('Exclusive lock is acquired on the row with id 1.')
    cursor.execute(update_student_query)
    print("Updated firstname for row with id 1 using transaction 2...")

    count = cursor.execute("SELECT * FROM dbo.student where id = 1").fetchone()
    print(f"First name from row with id 1 using transaction 2:", count[1])

    print("Exclusive lock is released.")


if __name__ == "__main__":
    # Creating processes
    process1 = multiprocessing.Process(target=shared_locks)
    process2 = multiprocessing.Process(target=shared_locks_modifier)

    # Starting processes
    process1.start()
    process2.start()

    # Waiting for processes to complete
    process1.join()
    process2.join()
