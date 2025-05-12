# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the full app, including cookies & Selenium driver
COPY . .

# ✅ Install Chrome WebDriver for Selenium
RUN apt-get update && apt-get install -y wget
RUN wget -q -O /usr/local/bin/chromedriver https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && chmod +x /usr/local/bin/chromedriver

# ✅ Set ChromeDriver as environment variable
ENV PATH="/usr/local/bin:${PATH}"

# Expose the default Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]
