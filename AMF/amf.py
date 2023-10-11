from flask import Flask, request, jsonify
import sqlite3
import requests  # Import the requests library

app = Flask(__name__)

class DatabaseCreation:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                name TEXT
            )
        ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def insert_user(self, user_id, name):
        self.cursor.execute('INSERT INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
        self.conn.commit()

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        users_data = self.cursor.fetchall()
        users_list = [{"user_id": user[1], "name": user[2]} for user in users_data]
        return users_list

@app.route('/amf/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    if not data or "user_id" not in data or "name" not in data:
        return jsonify({"error": "Missing 'user_id' or 'name' in the request data"}), 400
    
    user_id = data["user_id"]
    name = data["name"]   
    
    # Perform service discovery to get the NRF endpoint
    nrf_discover_url = "http://nrf-service/nrf/discover"  # Use the Kubernetes service name "nrf-service"
    
    try:
        response = requests.get(nrf_discover_url)  # Perform service discovery by sending a GET request to NRF's /nrf/discover

        if response.status_code == 200:
            nrf_data = response.json()
            nrf_endpoint = nrf_data["service_endpoint"]  # Get the NRF's service endpoint
        else:
            return jsonify({"error": f"Error discovering NRF: {response.status_code}"}), 500
        
        
        # Now, you can use nrf_endpoint to communicate with the NRF
        # For example, you can send a POST request to register the user with the NRF
        nrf_register_url = f"{nrf_endpoint}/nrf/register-user"  # Use NRF's endpoint to register the user
        
        response = requests.post(nrf_register_url, json={"user_id": user_id, "name": name})  # Send a POST request to NRF
        
        if response.status_code == 200:
            return jsonify({"message": f"User {name} registered successfully"})
        else:
            return jsonify({"error": f"Error registering user with the NRF: {response.status_code}"}), 500
    except requests.exceptions.RequestException as e:  # Handle exceptions
        return jsonify({"error": f"Error communicating with NRF: {str(e)}"}), 500        

@app.route('/amf/users', methods=['GET'])
def get_users():
    db_handler = DatabaseCreation('users.db')
    users_list = db_handler.get_users()
    return jsonify({"users": users_list})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)
