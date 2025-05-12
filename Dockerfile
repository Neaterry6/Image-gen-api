# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# ✅ Install Google Chrome (Needed for Selenium)
RUN apt-get update && apt-get install -y wget unzip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install

# ✅ Install Chrome WebDriver for Selenium
RUN wget -q -O /usr/local/bin/chromedriver "https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip"
RUN chmod +x /usr/local/bin/chromedriver

# ✅ Set ChromeDriver as environment variable
ENV PATH="/usr/local/bin:${PATH}"

# ✅ Copy the full app
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python3", "app.py"]
