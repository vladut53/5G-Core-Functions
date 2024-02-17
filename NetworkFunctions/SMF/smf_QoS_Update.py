
import logging
from flask import Flask, request, jsonify
import requests

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Mapping of site codes to URLs
site_mapping = {
    "1": "https://www.bing.com",
    "2": "https://www.google.com",
    "3": "https://www.yahoo.com"
}

@app.route('/smf/route', methods=['GET'])
def route_session():
    user_id = request.args.get('user_id')
    site_code = request.args.get('site_code')

    if not user_id or not site_code:
        return jsonify({"error": "Missing user_id or site_code"}), 400

    # Determine QoS profile based on site code (assuming '2' is for Google)
    qos_profile = "high" if site_code == "2" else "low"

    site_url = site_mapping.get(site_code)
    if not site_url:
        return jsonify({"error": "Invalid or unsupported site code"}), 400

    # QoS-based routing logic
    logging.info(f"SMF: Routing for user {user_id} to {site_url} with QoS profile {qos_profile}")
    try:
        response = requests.get(site_url, timeout=5)
        return jsonify({"message": f"Routed to {site_url}", "status_code": response.status_code, "qos_profile": qos_profile})
    except requests.exceptions.RequestException as e:
        logging.error(f"SMF: Error routing to {site_url}: {str(e)}")
        return jsonify({"error": f"Error routing to {site_url}: {str(e)}"}), 500

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time >= 60:  # Check if 1 minute has elapsed
            return jsonify({"status": "timeout"}), 500
        time.sleep(1)  # Sleep for 1 second before checking again

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82, debug=False)
