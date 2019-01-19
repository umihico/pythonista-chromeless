from selenium.webdriver import Chrome, ChromeOptions
import json
import traceback
from pprint import pprint
from load_code import load_code


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


def lambda_handler(event, context):
    try:
        if event["httpMethod"] == "POST":
            # print(event["body"])
            method, arg, kwargs = load_code(event["body"])
        else:
            raise Exception(f"httpMethod is {event['httpMethod']}, not 'POST'")
        Chrome.method = method
        chrome = gen_chrome()
        result = chrome.method(*arg, **kwargs)
        statusCode = 200
    except Exception as e:
        statusCode = 501
        result = traceback.format_exc()
        print(result)
    finally:
        try:
            chrome.quit()
        except Exception as e:
            pass
    return {
        'statusCode': statusCode,
        'body': str(result)
    }
