import logging
from flask import Flask, request, jsonify
import requests
import os

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
        imsi = data.get("imsi")  # New field: IMSI

        if not data:
            logging.error("AMF: No data provided for registration")
            return jsonify({"error": "No data provided"}), 400

        if not user_id or not name or not site_code:
            logging.error("AMF: Missing registration information")
            return jsonify({"error": "Missing registration information"}), 400

        if user_id in users:
            logging.warning(f"AMF: User {user_id} is already registered")
            return jsonify({"error": "User already registered"}), 400

        users[user_id] = {"name": name, "site_code": site_code, "imsi": imsi}  # Include IMSI in user data
        logging.info(f"AMF: User {user_id} registered with site code {site_code} and IMSI {imsi}")
        return jsonify({"message": f"User {user_id} registered successfully"}), 201
    
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/amf/access-smf', methods=['POST'])
def access_smf():
    pcrf_discover_smf_url = os.getenv("NRF_DISCOVER_PCRF_URL", "http://service-nrf.nf-nrf.svc.cluster.local:81/nrf/discover/pcrf")
    pcrf_decision_url = os.getenv("PCRF_DECISION_URL", "http://localhost:84/pcrf/decision")
    pcrf_response = requests.post(pcrf_decision_url, json={"user_id": user_id, "imsi": imsi}, timeout=3)
    pcrf_response.raise_for_status()
    
    pcrf_data = pcrf_response.json()
    can_access_smf = pcrf_data["can_access_smf"]

    try:
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
        imsi = users[user_id]["imsi"]  # Get IMSI for the user

        if not imsi.startswith("123"):
            logging.info(f"AMF: User {user_id} denied access due to IMSI restriction")
            return jsonify({"error": "Access denied due to IMSI restriction"}), 403

        nrf_discover_smf_url = os.getenv("NRF_DISCOVER_SMF_URL", "http://service-nrf.nf-nrf.svc.cluster.local:81/nrf/discover/smf")
        smf_response = requests.get(nrf_discover_smf_url, timeout=10)  # Increased timeout to 10 seconds
        smf_response.raise_for_status()

        smf_data = smf_response.json()
        smf_endpoint = smf_data.get("service_endpoint")

        if not smf_endpoint:
            logging.error("AMF: SMF service endpoint not found in the response")
            return jsonify({"error": "SMF service endpoint not found"}), 500

        full_smf_routing_url = f"{smf_endpoint}/smf/route?code={site_code}"
        logging.info(f"Routing to SMF with URL: {full_smf_routing_url}")

        smf_route_response = requests.get(full_smf_routing_url, timeout=10)  # Increased timeout to 10 seconds
        smf_route_response.raise_for_status()

        return jsonify({"smf_response": smf_route_response.json()})
    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing SMF: {e}")
        return jsonify({"error": f"Error accessing SMF: {e}"}), 500
    except Exception as e:
        logging.error(f"Internal server error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"}), 200

@app.route('/amf/users', methods=['GET'])
def get_users():
    try:
        return jsonify({"users": users}), 200
    except Exception as e:
        logging.error(f"Error retrieving users: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=83)
