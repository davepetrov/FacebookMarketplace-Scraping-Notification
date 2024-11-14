# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# def get_chrome_driver():
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--single-process')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--window-size=1280x1696')
#     chrome_options.add_argument('--user-data-dir=/tmp/chrome-user-data')
#     chrome_options.add_argument('--remote-debugging-port=9222')
#     chrome_options.binary_location = '/opt/chrome'

#     service = Service('/opt/chromedriver')
    
#     driver = webdriver.Chrome(
#         service=service,
#         options=chrome_options
#     )
#     return driver


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import ChromeType

class DriverConfig:
    def get_chrome_driver():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--user-data-dir=/tmp/chrome-user-data')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.binary_location = '/opt/chrome/chrome'

        service = Service('/opt/chromedriver')
        
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        return driver