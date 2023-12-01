import logging
from flask import Flask, request, jsonify
import requests

# Configure logging for AMF
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

# Placeholder for users data structure
users = {
    "user1": {"name": "Alin", "preferred_site": "https://www.youtube.com"},
    "user2": {"name": "Andrei", "preferred_site": "https://www.facebook.com"},
    "user3": {"name": "Maria", "preferred_site": "https://www.goolge.com"},
    "user4": {"name": "Bogdan", "preferred_site": "https://www.google.com"},
    "user5": {"name": "Robert", "preferred_site": "https://www.youtube.com"},
    "user6": {"name": "Ioana", "preferred_site": "https://www.facebook.com"}

}

@app.route('/amf/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    # Example registration logic
    user_id = data.get("user_id")
    name = data.get("name")
    preferred_site = data.get("preferred_site")

    if user_id in users:
        return jsonify({"error": "User already registered"}), 400

    users[user_id] = {"name": name, "preferred_site": preferred_site}
    logging.info(f"AMF: User {user_id} registered with preferred site {preferred_site}")
    return jsonify({"message": f"User {user_id} registered successfully"})

@app.route('/amf/access-smf', methods=['POST'])
def access_smf():
    user_data = request.get_json()
    user_id = user_data.get("user_id")

    # Check if the user is in the system
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    logging.info(f"AMF: Received access request from user {user_id}")

    # Request the SMF profile from NRF
    try:
        nrf_discover_smf_url = "http://nrf-service/nrf/discover/smf"
        smf_response = requests.get(nrf_discover_smf_url)
        if smf_response.status_code == 200:
            smf_data = smf_response.json()
            smf_endpoint = smf_data["service_endpoint"]
        else:
            return jsonify({"error": "SMF service not found"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with NRF: {str(e)}"}), 500

    # Use SMF endpoint to route user to their preferred site
    preferred_site = users[user_id]["preferred_site"]
    try:
        smf_route_response = requests.get(f"{smf_endpoint}?site={preferred_site}")
        logging.info(f"AMF: Routed user {user_id} to {preferred_site}")
        return jsonify({"smf_response": smf_route_response.json()})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error routing to preferred site via SMF: {str(e)}"}), 500


