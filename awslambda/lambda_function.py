from selenium.webdriver import Chrome, ChromeOptions
import json
import traceback
from pprint import pprint
from codedumper import load_code


def gen_chrome():
    options = ChromeOptions()
    options.binary_location = "./bin/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")
    chrome = Chrome("./bin/chromedriver", chrome_options=options)
    return chrome


def gen_method_of_returning_google_title():
    def method(self):
        self.get("https://www.google.co.jp")
        title = self.title
        self.quit()
        print(title)
        return title
    return method


def lambda_handler(event, context):
    # pprint(event)
    if event["httpMethod"] == "POST":
        load_code = event["body"]
        method = load_code(funcname, byte_func)
    else:
        method = gen_method_of_returning_google_title()
    Chrome.method = method
    chrome = gen_chrome()
    try:
        result = chrome.method()
        statusCode = 200
    except Exception as e:
        statusCode = 501
        result = traceback.format_exc()
    return {
        'statusCode': statusCode,
        'body': json.dumps(result)
    }
