import logging
from flask import Flask, request, jsonify
import requests
import time

# Configure logging for SMF
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Mapping of site codes to URLs
site_mapping = {
    "1": "https://www.bing.com",
    "2": "https://www.google.com",
    "3": "https://www.yahoo.com"
}

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"}), 200


@app.route('/smf/route', methods=['GET'])
def route_session():
    site_code = request.args.get('code')

    # Retrieve the corresponding URL from the site code
    site_url = site_mapping.get(site_code)

    if not site_url:
        return jsonify({"error": "Invalid or unsupported site code"}), 400

    # Determine QoS profile based on site code
    qos_profile = "high" if site_code == "2" else "low"

    if qos_profile != "high":
        time.sleep(5)

    logging.info(f"SMF: Routing request to {site_url} with QoS profile {qos_profile}")

    # Simulate routing by making a request to the selected site
    try:
        response = requests.get(site_url, timeout=5)  # Adding timeout
        return jsonify({"message": f"Routed to {site_url}", "status_code": response.status_code, "qos_profile": qos_profile})
    except requests.exceptions.RequestException as e:
        logging.error(f"SMF: Error routing to {site_url}: {str(e)}")
        return jsonify({"error": f"Error routing to {site_url}: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82, debug=False)

