from backend.db.db_connection import get_db_connection
import random
from datetime import datetime, timedelta

def init_db():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return

    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        amount DECIMAL(10, 2) NOT NULL,
        location VARCHAR(100),
        risk_score INT,
        is_fraud BOOLEAN DEFAULT FALSE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Check if we need to seed data
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Seeding sample transactions...")
        values = []
        for _ in range(50):
            amount = round(random.uniform(10.0, 5000.0), 2)
            location = random.choice(["New York", "London", "Tokyo", "Lagos", "Moscow", "Berlin"])
            risk_score = random.randint(1, 100)
            is_fraud = risk_score > 85
            timestamp = datetime.now() - timedelta(hours=random.randint(0, 48))
            
            values.append((amount, location, risk_score, is_fraud, timestamp))
            
        cursor.executemany("""
        INSERT INTO transactions (amount, location, risk_score, is_fraud, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """, values)
        conn.commit()
        print("Seeded 50 transactions.")
    else:
        print("Transactions table already exists and has data.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
