from flask import Flask, request, jsonify
import random

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=82)

registered_services = []

@app.route('/nrf/register', methods=['POST'])
def register_services():
    data = request.get_json()

    if not data or "service_name" not in data or "service_version" not in data or "service_endpoint" not in data:
        return jsonify({"error": "Missing required data fields for Network Function"}), 400

    service_name = data["service_name"]
    service_version = data["service_version"]
    service_endpoint = data["service_endpoint"]

    registered_services.append({
        "name": service_name,
        "version": service_version,
        "endpoint": service_endpoint
    })

    return jsonify({"message": "Service registered successfully"})

@app.route('/nrf/discover', methods=['GET'])
def discover_services():
    if not registered_services:
        return jsonify({"error": "Service not registered"}), 404

    service = random.choice(registered_services)

    return jsonify({
        "service_name": service["name"],
        "service_version": service["version"],
        "service_endpoint": service["endpoint"]
    })

@app.route('/nrf/services', methods=['GET'])
def list_registered_services():
    return jsonify({"services": registered_services})
