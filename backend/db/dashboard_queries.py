from backend.db.db_connection import get_db_connection

def get_dashboard_stats():
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Total Volume
        cursor.execute("SELECT SUM(amount) as total_volume FROM transactions")
        res_vol = cursor.fetchone()
        total_volume = res_vol['total_volume'] if res_vol['total_volume'] else 0
        
        # Fraud Detected Count
        cursor.execute("SELECT COUNT(*) as fraud_count FROM transactions WHERE is_fraud = TRUE")
        res_fraud = cursor.fetchone()
        fraud_count = res_fraud['fraud_count']
        
        # Avg Risk Score
        cursor.execute("SELECT AVG(risk_score) as avg_risk FROM transactions")
        res_risk = cursor.fetchone()
        avg_risk = float(res_risk['avg_risk']) if res_risk['avg_risk'] else 0
        
        return {
            "total_volume": float(total_volume),
            "fraud_count": fraud_count,
            "avg_risk_score": round(avg_risk, 1),
            "accuracy": 99.9 # Hardcoded for now as it's model metric
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_recent_transactions(limit=5):
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT id, amount, location, risk_score, is_fraud, timestamp 
            FROM transactions 
            ORDER BY timestamp DESC 
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        transactions = cursor.fetchall()
        
        # Convert values for JSON serialization if needed
        for tx in transactions:
            tx['amount'] = float(tx['amount'])
            # Format timestamp as string
            if tx['timestamp']:
                tx['timestamp'] = tx['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                
        return transactions
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
