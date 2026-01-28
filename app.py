from flask import Flask, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder=".")

OLLAMA_URL = "http://localhost:11434/api/generate"

sales_data = [
    {"product":"Laptop","revenue":1200},
    {"product":"Phone","revenue":800},
    {"product":"Tablet","revenue":600},
    {"product":"Laptop","revenue":1000}
]

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/insights")
def insights():
    summary = ""

    for item in sales_data:
        summary += f"{item['product']} sold for {item['revenue']}. "

    prompt = f"""
Analyze this sales data and provide:

1. Total revenue
2. Top product
3. Sales trend
4. Business recommendation

Data:
{summary}
"""

    payload = {
        "model":"llama3",
        "prompt":prompt,
        "stream":False
    }

    response = requests.post(OLLAMA_URL,json=payload)
    return jsonify({"insights":response.json().get("response","")})

if __name__=="__main__":
    app.run(debug=True)
