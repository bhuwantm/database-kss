import db

def create_tables():
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

    conn = db.get_connection()

    try:
        print("Seeding tables...")

        cursor = conn.cursor()

        # Start a transaction
        conn.autocommit = False  # Disable autocommit to start a transaction

        # Execute both queries
        cursor.execute(create_student_query)
        cursor.execute(create_subject_query)

        # Commit the transaction
        conn.commit()

        print("Both tables created successfully within a single transaction.")

    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"Transaction failed. Rolled back due to error: {e}")

    finally:
        # Close the connection
        conn.close()


def drop_tables():
    drop_student_query = "DROP TABLE school;"
    drop_subject_query = "DROP TABLE subject;"

    conn = db.get_connection()

    try:
        print("Dropping tables...")

        cursor = conn.cursor()

        # Start a transaction
        conn.autocommit = False  # Disable autocommit to start a transaction

        # Execute both queries
        cursor.execute(drop_student_query)
        cursor.execute(drop_subject_query)

        # Commit the transaction
        conn.commit()

        print("Both tables dropped successfully within a single transaction.")

    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"Transaction failed. Rolled back due to error: {e}")

    finally:
        # Close the connection
        conn.close()
