from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ✅ Function to Load Netscape Cookies
def load_cookies():
    """Read cookies.txt in Netscape format & convert to a Cookie string."""
    try:
        with open("cookies.txt", "r") as f:
            cookies = []
            for line in f:
                if not line.startswith("#") and len(line.strip().split("\t")) >= 6:
                    parts = line.strip().split("\t")
                    cookie_name = parts[5]
                    cookie_value = parts[6] if len(parts) > 6 else ""
                    cookies.append(f"{cookie_name}={cookie_value}")
            return "; ".join(cookies)
    except FileNotFoundError:
        return None

# ✅ Health Check Route
@app.route("/")
def home():
    return jsonify({"message": "API is working!"})

# 🔍 **Bing Image Search**
@app.route("/search")
def search_images():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Provide a search query!"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": load_cookies()
    }

    bing_url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2"
    response = requests.get(bing_url, headers=headers)

    return jsonify({"images": response.text})  # ✅ Parsing needed for image URLs

# 🎨 **Bing AI Image Generation**
@app.route("/generate")
def generate_images():
    prompt = request.args.get("prompt")
    if not prompt:
        return jsonify({"error": "Provide an image prompt!"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": load_cookies()
    }

    # ✅ Step 1: Request Bing AI Image Generation Page
    bing_url = f"https://www.bing.com/images/create?q={prompt}&form=GENILP"
    response = requests.get(bing_url, headers=headers, allow_redirects=True)

    # ✅ Step 2: Follow Redirects & Extract the Real AI-Generated Image URL
    soup = BeautifulSoup(response.text, "html.parser")
    image_element = soup.find("img", class_="mimg")  # Look for main AI-generated image

    if image_element:
        image_url = image_element["src"]
        return jsonify({"generated_image": image_url})  # ✅ AI-generated image
    else:
        return jsonify({"error": "Failed to extract AI-generated image!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
