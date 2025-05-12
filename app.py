from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ✅ Health Check Route
@app.route("/")
def home():
    return jsonify({"message": "API is working!"})

# 🔍 Bing Image Search API
@app.route("/search")
def search_images():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Provide a search query!"}), 400

    # ✅ Load cookies from file
    try:
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
    except:
        return jsonify({"error": "Cookies file not found or incorrect format!"}), 500

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items()])  # Convert JSON cookies to string format
    }

    bing_url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2"
    response = requests.get(bing_url, headers=headers)

    return jsonify({"images": response.text})  # ✅ You’ll need to properly parse images in the next step

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
