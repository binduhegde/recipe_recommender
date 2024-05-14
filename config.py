from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium import webdriver

#user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

# Options
options = ChromeOptions()
# options.add_experimental_option('detach', True)
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Service
service = Service(executable_path="/Users/bindu/dev/drivers/chromedriver")

# Driver
chrome_driver = webdriver.Chrome(service=service, options=options)
