import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Statically defined service profiles for AMF, SMF, and PCRF
registered_services = {
    "amf": {"service_endpoint": "http://service-amf.nf-amf.svc.cluster.local:83"}, 
    "smf": {"service_endpoint": "http://service-smf.nf-smf.svc.cluster.local:82"},
    "pcrf": {"service_endpoint": "http://service-pcrf.nf-pcrf.svc.cluster.local:84"} 
}

@app.route('/nrf/register', methods=['POST'])
def register_service():
    data = request.get_json()
    service_name = data.get("service_name")
    service_endpoint = data.get("service_endpoint")

    if not service_name or not service_endpoint:
        logging.error("NRF: Missing service name or endpoint in registration")
        return jsonify({"error": "Missing service name or endpoint"}), 400

    registered_services[service_name] = {"service_endpoint": service_endpoint}
    logging.info(f"NRF: Service {service_name} registered with endpoint {service_endpoint}")
    return jsonify({"message": f"Service {service_name} registered successfully"})

@app.route('/nrf/discover/<service_name>', methods=['GET'])
def discover_service(service_name):
    service_profile = registered_services.get(service_name)
    if service_profile:
        logging.info(f"NRF: Provided discovery information for {service_name}")
        return jsonify(service_profile)
    else:
        logging.error(f"NRF: Service {service_name} not found in registry")
        return jsonify({"error": f"Service {service_name} not found"}), 404

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
