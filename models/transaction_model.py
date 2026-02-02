# models/transaction_model.py

from config.db import get_connection

def _init_transactions_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            type VARCHAR(50) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def _fix_transaction_type_length():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Increase the length of the 'type' column to handle longer strings like 'TRANSFER_RECEIVED'
        cursor.execute("ALTER TABLE transactions MODIFY COLUMN type VARCHAR(50)")
        conn.commit()
    except Exception:
        pass
    finally:
        cursor.close()
        conn.close()

try:
    _init_transactions_table()
    _fix_transaction_type_length()
except Exception:
    pass

def get_balance(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE id = %s",
        (user_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row[0] if row else None


def get_transactions(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, amount, created_at
        FROM transactions
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def update_balance(cursor, user_id, amount):
   
    sql = """
    UPDATE users
    SET balance = balance + %s
    WHERE id = %s
    """
    cursor.execute(sql, (amount, user_id))


def insert_transaction(cursor, user_id, tx_type, amount):
   
    sql = """
    INSERT INTO transactions (user_id, type, amount)
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (user_id, tx_type, amount))

def get_daily_transfer_count(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Count how many 'TRANSFER_SENT' transactions this user made today
    sql = """
        SELECT COUNT(*) FROM transactions 
        WHERE user_id = %s AND type = 'TRANSFER_SENT' 
        AND DATE(created_at) = CURDATE()
    """
    cursor.execute(sql, (user_id,))
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    return count

def transfer_funds(sender_id, receiver_id, amount, sender_name):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Deduct from sender
        update_balance(cursor, sender_id, -amount)
        insert_transaction(cursor, sender_id, "TRANSFER_SENT", amount)
        
        # 2. Add to receiver
        update_balance(cursor, receiver_id, amount)
        insert_transaction(cursor, receiver_id, "TRANSFER_RECEIVED", amount)
        
        # 3. Create Notification for receiver
        sql_notif = "INSERT INTO notifications (user_id, message) VALUES (%s, %s)"
        msg = f"You received {amount:.2f} DA from {sender_name}"
        cursor.execute(sql_notif, (receiver_id, msg))
        
        conn.commit()
        return True, "Transfer successful"
    except Exception as e:
        conn.rollback()
        return False, f"Transfer failed: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def get_all_transactions_global():
    conn = get_connection()
    cursor = conn.cursor()
    # Join with users to get names
    sql = """
        SELECT t.id, u.full_name, t.type, t.amount, t.created_at 
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.created_at DESC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def delete_transaction(tx_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE id = %s", (tx_id,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        cursor.close()
        conn.close()
