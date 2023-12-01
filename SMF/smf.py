import logging
from flask import Flask, request, jsonify
import requests
import random

# Configure logging for SMF
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=82)
    

# List of external sites to simulate routing
external_sites = ["https://www.youtube.com", "https://www.facebook.com", "https://www.google.com"]

@app.route('/smf/route', methods=['GET'])
def route_session():
    site = request.args.get('site')

    if not site or site not in external_sites:
        # Randomly select a site if not specified or if the specified site is not in the list
        site = random.choice(external_sites)

    logging.info(f"SMF: Routing request to {site}")

    # Simulate routing by making a request to the selected site
    try:
        response = requests.get(site)
        return jsonify({"message": f"Routed to {site}", "status_code": response.status_code})
    except requests.exceptions.RequestException as e:
        logging.error(f"SMF: Error routing to {site}: {str(e)}")
        return jsonify({"error": f"Error routing to {site}: {str(e)}"}), 500

