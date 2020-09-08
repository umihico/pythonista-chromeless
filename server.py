import types
from selenium import webdriver
from picklelib import loads, dumps  # imports in Dockerfile
import json


def handler(event=None, context=None):
    if 'dumped' in event:
        dumped = event['dumped']
        return ChromelessServer().recieve(dumped)
    else:
        dumped = json.loads(event['body'])['dumped']
        return {
            'statusCode': 200,
            'body': json.dumps({'result': ChromelessServer().recieve(dumped)}),
            "headers": {
                'Content-Type': "application/json",
                'Access-Control-Allow-Origin': '*',
            }
        }


class ChromelessServer():
    def gen_chrome(self, options):
        if options is None:
            options = get_default_options()
        options.binary_location = "/opt/python/bin/headless-chromium"
        return webdriver.Chrome(
            "/opt/python/bin/chromedriver", options=options)

    def recieve(self, dumped):
        name, code, arg, kw, options = loads(dumped)
        chrome = self.gen_chrome(options)
        exec(code)
        func = locals()[name]
        setattr(chrome, name, types.MethodType(func, chrome))
        try:
            return dumps(getattr(chrome, name)(*arg, **kw))
        except Exception:
            raise
        finally:
            chrome.quit()


def get_default_options():
    options = webdriver.ChromeOptions()
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
