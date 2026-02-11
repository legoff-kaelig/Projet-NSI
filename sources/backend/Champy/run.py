from flask import Flask, jsonify, request
from flask_cors import CORS
from correspondance_champy import *

app = Flask(__name__)
CORS(app)

@app.route('/update', methods=['GET'])
def home():

    variable_received = request.args.get('plant_id')

    print("Received a request to /update")
    champiName = champy(variable_received)

    return jsonify({'name': champiName})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
