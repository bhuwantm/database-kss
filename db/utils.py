import db


def in_transaction(func):
    def wrapper(*args, **kwargs):
        conn = db.get_connection()

        try:
            conn.autocommit = False

            result = func(conn, *args, **kwargs)

            # Commit the transaction
            conn.commit()

        except Exception as e:
            # Rollback the transaction in case of an error
            conn.rollback()
            print(f"Transaction failed. Rolled back due to error: {e}")
            raise

        finally:
            # Close the connection
            conn.close()

        return result

    return wrapper
