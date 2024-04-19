from flask import Flask, request, jsonify

from lib.db import DBHandler

app = Flask(__name__)


db =  DBHandler()


@app.route('/geolocate/<ip>', methods=['GET'])
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
def geolocate_multiple_ips():
    try:
        data = request.json
        results = db.resolve_ips(data['ips'])
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
