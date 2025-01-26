from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2

app = Flask(__name__)

# Database connection
DATABASE_URL = os.environ['DATABASE_URL']

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Create table if not exists
with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS waste_data
                       (id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP,
                        bin_id TEXT,
                        bin_location TEXT,
                        category TEXT,
                        class_name TEXT,
                        probability FLOAT)''')
    conn.commit()

@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''INSERT INTO waste_data
                           (timestamp, bin_id, bin_location, category, class_name, probability)
                           VALUES (%s, %s, %s, %s, %s, %s)''',
                        (datetime.utcfromtimestamp(data['timestamp']),
                         data['bin_id'], data['bin_location'], data['category'],
                         data['class_name'], data['probability']))
        conn.commit()
    
    return jsonify({"message": "Data received successfully", "data": data}), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM waste_data')
            data = cur.fetchall()
    return jsonify(data), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Waste classification API"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

