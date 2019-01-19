from selenium.webdriver import Chrome, ChromeOptions
import json
import traceback
from pprint import pprint
from server_pickler import load_methods, pickle_result


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
            called_name_as_method, arg, kwargs, funcs = load_methods(event["body"])
        else:
            raise Exception(f"httpMethod is {event['httpMethod']}, not 'POST'")
        for name, func in funcs.items():
            setattr(Chrome, name, func)
        chrome = gen_chrome()
        # setattr(self, func.__name__, types.MethodType(method, self))
        method = getattr(chrome, called_name_as_method)
        result = method(*arg, **kwargs)
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
        'body': pickle_result(result)
    }
