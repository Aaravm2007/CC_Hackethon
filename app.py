from flask import Flask, render_template, request, jsonify
import requests
from ai_matcher import *
app = Flask(__name__)

FASTAPI_URL = "http://127.0.0.1:8000"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def find_match():
    try:
        founder_id = request.json.get("founder_id")
        if not founder_id:
            return jsonify({"error": "Founder ID is required"}), 400
        
        response = requests.get(f"{FASTAPI_URL}/match/{founder_id}")
        data = response.json()

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
