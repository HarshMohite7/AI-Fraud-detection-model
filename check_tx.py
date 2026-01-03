from backend.db.db_connection import get_db_connection

def count_transactions():
    conn = get_db_connection()
    if not conn:
        print("DB Connection Failed")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    print(f"Total Transactions: {count}")
    
    if count > 0:
        cursor.execute("SELECT * FROM transactions LIMIT 1")
        print("Sample:", cursor.fetchone())

    conn.close()

if __name__ == "__main__":
    count_transactions()
