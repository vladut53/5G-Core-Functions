
import logging
from flask import Flask, request, jsonify
import requests
import os

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Users in the network with site codes
users = {
    "user1": {"name": "Alin", "site_code": "1"},
    "user2": {"name": "Andrei", "site_code": "3"},
    "user3": {"name": "Maria", "site_code": "2"},
    "user4": {"name": "Bogdan", "site_code": "2"},
    "user5": {"name": "Robert", "site_code": "1"},
    "user6": {"name": "Ioana", "site_code": "3"}
}

@app.route('/amf/register', methods=['POST'])
def register_user():
    data = request.get_json(silent=True)

    if not data:
        logging.error("AMF: No data provided for registration")
        return jsonify({"error": "No data provided"}), 400

    user_id = data.get("user_id")
    name = data.get("name")
    site_code = data.get("site_code")

    if not user_id or not name or not site_code:
        logging.error("AMF: Missing registration information")
        return jsonify({"error": "Missing registration information"}), 400

    if user_id in users:
        logging.warning(f"AMF: User {user_id} is already registered")
        return jsonify({"error": "User already registered"}), 400

    users[user_id] = {"name": name, "site_code": site_code}
    logging.info(f"AMF: User {user_id} registered with site code {site_code}")
    return jsonify({"message": f"User {user_id} registered successfully"})

@app.route('/amf/access-smf', methods=['POST'])
def access_smf():
    user_data = request.get_json(silent=True)

    if not user_data:
        logging.error("AMF: No data provided for access")
        return jsonify({"error": "No data provided"}), 400

    user_id = user_data.get("user_id")

    if not user_id or user_id not in users:
        logging.error("AMF: User not found or not specified")
        return jsonify({"error": "User not found"}), 404

    logging.info(f"AMF: Received access request from user {user_id}")

    site_code = users[user_id]["site_code"]

    try:
        nrf_discover_smf_url = os.getenv("NRF_DISCOVER_SMF_URL", "http://nrf-service.nf-nrf.svc.cluster.local:81/nrf/discover/smf")
        smf_response = requests.get(nrf_discover_smf_url, timeout=3)
        smf_response.raise_for_status()

        smf_data = smf_response.json()
        smf_endpoint = smf_data["service_endpoint"]

        full_smf_routing_url = f"{smf_endpoint}/smf/route?code={site_code}"
        logging.info(f"Routing to SMF with URL: {full_smf_routing_url}")

        smf_route_response = requests.get(full_smf_routing_url, timeout=3)
        smf_route_response.raise_for_status()

        return jsonify({"smf_response": smf_route_response.json()})
    except requests.exceptions.RequestException as e:
        logging.error(f"Error routing to SMF: {e}")
        return jsonify({"error": f"Error routing to SMF: {e}"}), 500

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
