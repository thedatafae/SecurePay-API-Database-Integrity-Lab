from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="8899",
        database="securepay_db"
    )

# --- 1. MAPPING/READ TEST (GET) ---
@app.route('/accounts', methods=['GET'])
def get_accounts():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accounts")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

# --- 2. THE BUSINESS LOGIC (POST) ---
@app.route('/transfer', methods=['POST'])
def transfer_money():
    data = request.json
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    amount = data.get('amount')

    # PRO-LEVEL VALIDATION: Check if amount is valid
    if not amount or amount <= 0:
        return jsonify({"error": "Invalid amount. Must be greater than 0"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        conn.start_transaction() # ACID Property: Atomicity

        # Check Sender Balance
        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (sender_id,))
        sender = cursor.fetchone()
        
        if not sender or sender['balance'] < amount:
            return jsonify({"error": "Insufficient funds or Sender not found"}), 400

        # Perform Transfer
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, sender_id))
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, receiver_id))
        
        # Log Transaction
        cursor.execute("INSERT INTO transactions (sender_id, receiver_id, amount) VALUES (%s, %s, %s)", 
                       (sender_id, receiver_id, amount))

        conn.commit() # Save changes
        return jsonify({"status": "Success", "message": "Transfer Completed"}), 200

    except Error as e:
        conn.rollback() # Undo everything if error occurs
        return jsonify({"error": "Database error occurred"}), 500
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

# --- 3. THE RESET (For Testing Cleanliness) ---
@app.route('/reset', methods=['POST'])
def reset_db():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = 1000.00 WHERE id = 1")
        cursor.execute("UPDATE accounts SET balance = 500.00 WHERE id = 2")
        cursor.execute("DELETE FROM transactions")
        conn.commit()
        return jsonify({"message": "Environment Reset"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)