from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load SIP data
def load_sip_data():
    with open("sip_growth_data.json", "r") as json_file:
        return json.load(json_file)

@app.route('/get_sip_data', methods=['GET'])
def get_sip_data():
    data = load_sip_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
