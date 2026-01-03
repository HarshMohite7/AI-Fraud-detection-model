import os
import sys

sys.path.append(os.getcwd())

from backend.db.db_connection import get_db_connection

def check_schema():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect.")
        return

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables:", tables)
    
    # Check columns if transactions exists
    for table in tables:
        if 'transactions' in table:
            cursor.execute("DESCRIBE transactions")
            print("Transactions Schema:", cursor.fetchall())

    cursor.close()
    conn.close()

if __name__ == "__main__":
    check_schema()
