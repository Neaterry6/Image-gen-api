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
        # ✅ Open Bing Image Creator
        driver.get("https://www.bing.com/images/create")

        # ✅ Locate the input box and type the prompt
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(prompt)
        search_box.send_keys(Keys.RETURN)

        # ✅ Wait for Bing to generate the image (adjust if needed)
        time.sleep(10)

        # ✅ Extract the AI-generated image URL
        image_element = driver.find_element(By.CLASS_NAME, "mimg")  # Locate the correct image
        image_url = image_element.get_attribute("src")

        driver.quit()  # ✅ Close browser after scraping

        return jsonify({"generated_image": image_url})
    
    except Exception as e:
        driver.quit()  # ✅ Close browser in case of error
        return jsonify({"error": f"Failed to generate image! {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
