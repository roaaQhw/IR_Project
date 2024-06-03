import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# URLs الخاصة بالخدمات الخلفية
ANTIQUE_SERVICE_URL = "http://localhost:5002/suggest_antique"
LIFESTYLE_SERVICE_URL = "http://localhost:5001/suggest_lifestyle"
LIFESTYLE_SEARCH_URL = "http://localhost:5003/search_lifestyle"
ANTIQUE_SEARCH_URL = "http://localhost:5004/search_antique"

@app.route('/suggest_antique', methods=['POST'])
def suggest_antique():
    response = requests.post(ANTIQUE_SERVICE_URL, json=request.json)
    return jsonify(response.json())

@app.route('/suggest_lifestyle', methods=['POST'])
def suggest_lifestyle():
    response = requests.post(LIFESTYLE_SERVICE_URL, json=request.json)
    return jsonify(response.json())

@app.route('/search_lifestyle', methods=['POST'])
def search_lifestyle():
    response = requests.post(LIFESTYLE_SEARCH_URL, json=request.json)
    return jsonify(response.json())


@app.route('/search_antique', methods=['POST'])
def search_antique():
    response = requests.post(ANTIQUE_SEARCH_URL, json=request.json)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
