import logging
from flask import Flask, request, jsonify
import requests
import os
import time

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Users in the network with site codes
users = {}

@app.route('/amf/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json(silent=True)
        user_id = data.get("user_id")
        name = data.get("name")
        site_code = data.get("site_code")

        if not data:
            logging.error("AMF: No data provided for registration")
            return jsonify({"error": "No data provided"}), 400

        if not user_id or not name or not site_code:
            logging.error("AMF: Missing registration information")
            return jsonify({"error": "Missing registration information"}), 400

        if user_id in users:
            logging.warning(f"AMF: User {user_id} is already registered")
            return jsonify({"error": "User already registered"}), 400

        users[user_id] = {"name": name, "site_code": site_code}
        logging.info(f"AMF: User {user_id} registered with site code {site_code}")
        return jsonify({"message": f"User {user_id} registered successfully"}), 201
    
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/amf/access-smf', methods=['POST'])
def access_smf():
    try:
        user_data = request.get_json()
        user_id = user_data.get("user_id")

        if not user_id or user_id not in users:
            raise ValueError("User not found or not specified")

        site_code = users[user_id]["site_code"]

        # Assuming NRF_DISCOVER_SMF_URL is an environment variable
        nrf_discover_smf_url = os.getenv("NRF_DISCOVER_SMF_URL", "http://nrf-service.nf-nrf.svc.cluster.local:81/nrf/discover/smf")
        smf_response = requests.get(nrf_discover_smf_url, timeout=3)
        smf_response.raise_for_status()

        smf_data = smf_response.json()
        smf_endpoint = smf_data["service_endpoint"]

        full_smf_routing_url = f"{smf_endpoint}/smf/route?code={site_code}"
        logging.info(f"Routing to SMF with URL: {full_smf_routing_url}")

        smf_route_response = requests.get(full_smf_routing_url, timeout=3)
        smf_route_response.raise_for_status()

        return jsonify({"smf_response": smf_route_response.json()}), 200

    except Exception as e:
        logging.error(f"Error accessing SMF: {e}")
        return jsonify({"error": str(e)}), 500
 

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time >= 60:  # Check if 1 minute has elapsed
            return jsonify({"status": "timeout"}), 500
        time.sleep(1)  # Sleep for 1 second before checking again

@app.route('/amf/users', methods=['GET'])
def get_users():
    try:
        return jsonify({"users": users}), 200
    except Exception as e:
        logging.error(f"Error retrieving users: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
