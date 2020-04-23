import types
import marshal
import pickle
import base64
import zlib
import json
import traceback
from screenshot_handler import ScreenshotHandler
from selenium.webdriver import Chrome, ChromeOptions
import os


def _test_selenium(event, context):
    chrome = gen_chrome()
    chrome.get('https://www.google.com/')
    title = chrome.title
    print(title)
    chrome.quit()
    return {
        'statusCode': 200,
        'body': json.dumps({'title': title})
    }


def load_methods(base64str_data):
    b = base64.b64decode(base64str_data.encode())
    called_name_as_method, arg, kwargs, dumped_funcs, chrome_options = pickle.loads(
        zlib.decompress(b))
    funcs = {}
    for name, dumped in dumped_funcs.items():
        func = types.FunctionType(marshal.loads(dumped), globals(), name)
        funcs[name] = func
    return called_name_as_method, arg, kwargs, funcs, chrome_options


def pickle_result(result):
    return base64.b64encode(zlib.compress(pickle.dumps(result))).decode()


def gen_chrome(options=None):
    options = options or gen_default_chrome_options()
    options.binary_location = "bin/headless-chromium"  # required
    chrome = Chrome("bin/chromedriver", chrome_options=options)
    return chrome


def lambda_handler(event, context):
    try:
        called_name_as_method, arg, kwargs, funcs, chrome_options = load_methods(
            event["body"])
        for name, func in funcs.items():
            setattr(Chrome, name, func)
        chrome = gen_chrome(chrome_options)
        screenshothandler = ScreenshotHandler(chrome)
        # setattr(self, func.__name__, types.MethodType(method, self))
        method = getattr(chrome, called_name_as_method)
        result = method(*arg, **kwargs)
        result = screenshothandler.wrap_with_screenshots(result)
        return {
            'statusCode': 200,
            'body': json.dumps(pickle_result(result))
        }
    except Exception:
        return {
            'statusCode': 500,
            'body': json.dumps(traceback.format_exc())
        }
        raise
    finally:
        try:
            chrome.quit()
        except Exception:
            pass


def gen_default_chrome_options():
    options = ChromeOptions()
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
    return options
