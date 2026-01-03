import os
import sys

# Add the project root to the python path
sys.path.append(os.getcwd())

from backend.db.db_connection import get_db_connection

def list_users():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database.")
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, role FROM users")
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users:")
    for user in users:
        print(f"ID: {user['id']} | Name: {user['name']} | Email: {user['email']} | Role: {user['role']}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    list_users()
