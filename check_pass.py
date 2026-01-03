from backend.db.db_connection import get_db_connection
import sys

def check_user_pass(email):
    conn = get_db_connection()
    if not conn:
        print("DB Connection Failed")
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    if user:
        print(f"User Found: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Stored Hash: {user['password_hash']}")
    else:
        print("User not found.")

    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_user_pass(sys.argv[1])
    else:
        print("Usage: python check_pass.py <email>")
