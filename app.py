from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

# ✅ Configure Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ✅ Run without opening a window
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = "/usr/bin/google-chrome"  # ✅ Ensure correct Chrome path

    service = Service("/usr/local/bin/chromedriver")  # ✅ Ensure correct WebDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# 🎨 **Bing AI Image Generation (Automated)**
@app.route("/generate")
def generate_images():
    prompt = request.args.get("prompt")
    if not prompt:
        return jsonify({"error": "Provide an image prompt!"}), 400

    driver = setup_driver()
    
    try:
        # ✅ Open Bing AI Image Creator
        driver.get("https://www.bing.com/images/create")

        # ✅ Locate the input box and type the prompt
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(prompt)
        search_box.send_keys(Keys.RETURN)

        # 🔥 **Wait Longer for AI to Generate Image**
        time.sleep(20)  # Increased from 10 to 20 seconds

        # ✅ Extract the correct AI-generated image
        images = driver.find_elements(By.TAG_NAME, "img")  # Get all images on the page
        for img in images:
            if "bing.com" in img.get_attribute("src"):  # ✅ Ensure it's from Bing AI
                image_url = img.get_attribute("src")
                driver.quit()  # ✅ Close browser
                return jsonify({"generated_image": image_url})

        driver.quit()  
        return jsonify({"error": "Failed to find AI-generated image. Try a different prompt!"})

    except Exception as e:
        driver.quit()  
        return jsonify({"error": f"Error generating image: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
