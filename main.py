import os
from flask import Flask, request, jsonify
from waitress import serve
import logging
import sys
from functools import wraps
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root_dir, 'lib'))
from lib.db import DBHandler

app = Flask(__name__)
db = DBHandler()


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def log_requests(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        status_code = response[1] if isinstance(response, tuple) else 200
        logging.info(f"Received {request.method} request for {request.path} from {request.remote_addr}, Status: {status_code}")
        return response
    return wrapper

@app.route('/geolocate/<ip>', methods=['GET'])
@log_requests
def geolocate_single_ip(ip):
    try:
        result = db.resolve_ip(ip)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'IP not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/geolocate', methods=['POST'])
@log_requests
def geolocate_multiple_ips():
    try:
        data = request.json
        results = db.resolve_ips(data['ips'])
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
