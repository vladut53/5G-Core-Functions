import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/pcrf/register', methods=['POST'])
def register_pcrf():
    data = request.get_json()
    pcrf_name = data.get("pcrf_name")
    pcrf_endpoint = data.get("pcrf_endpoint")

    if not pcrf_name or not pcrf_endpoint:
        logging.error("PCRF: Missing PCRF name or endpoint in registration")
        return jsonify({"error": "Missing PCRF name or endpoint"}), 400

    logging.info(f"PCRF: PCRF {pcrf_name} registered with endpoint {pcrf_endpoint}")
    return jsonify({"message": f"PCRF {pcrf_name} registered successfully"})

@app.route('/pcrf/decision', methods=['POST'])
def make_decision():
    data = request.get_json()
    user_id = data.get("user_id")
    imsi = data.get("imsi")

    # Dummy logic: Allow access to SMF only if user's IMSI starts with "123"
    can_access_smf = imsi.startswith("123")

    logging.info(f"PCRF: Decision for user {user_id}: Can access SMF? {can_access_smf}")
    return jsonify({"can_access_smf": can_access_smf})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=84)
