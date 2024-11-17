# from config.DriverConfig import DriverConfig;
from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Changed from ChromeOptions to Options
import time


class DriverConfig:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")

        # self.service = Service(
        #     executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
        #     service_log_path="/tmp/chromedriver.log"
        # )
        
        # self.driver = webdriver.Chrome(options=self.options, service=self.service)
        self.driver = webdriver.Chrome(options=self.chrome_options)


