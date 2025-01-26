from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store waste classification data
data_store = []

@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    # Add timestamp for readability
    data['readable_timestamp'] = datetime.utcfromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    data_store.append(data)
    
    return jsonify({"message": "Data received successfully", "data": data}), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data_store), 200

@app.route('/', methods=['GET'])
def home():
	return jsonify({"message": "Waste classification API"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
