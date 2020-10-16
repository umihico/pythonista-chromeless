import os
import shutil
import types
from selenium import webdriver
from picklelib import loads, dumps  # imports in Dockerfile
import json
import marshal
import textwrap
from versions import ChromelessServerVerNone
from versions import ChromelessServerVer1
import traceback
from tempfile import TemporaryDirectory
import os
os.environ['FONTCONFIG_PATH'] = '/opt/fonts'


def remove_tmpfiles():
    for filename in os.listdir('/tmp'):
        file_path = os.path.join('/tmp', filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def handler(event=None, context=None):
    remove_tmpfiles()
    if 'dumped' in event:
        dumped = event['dumped']
        return invoke(dumped)
    else:
        dumped = json.loads(event['body'])['dumped']
        return {
            'statusCode': 200,
            'body': json.dumps({'result': invoke(dumped)}),
            "headers": {
                'Content-Type': "application/json",
                'Access-Control-Allow-Origin': '*',
            }
        }


def invoke(dumped):
    arg = loads(dumped)
    print(arg)
    required_version = arg['REQUIRED_SERVER_VERSION'] if isinstance(
        arg, dict) else None
    ChormelessServerClass = {
        2: ChromelessServer,  # latest
        1: ChromelessServerVer1,
        None: ChromelessServerVerNone,
    }[required_version]
    if required_version is None:
        arg = dumps(arg)  # dump again
    return ChormelessServerClass().recieve(arg)


class ChromelessServer():
    SERVER_VERSION = 2

    def gen_chrome(self, options, dirname):
        if options is None:
            options = get_default_options(dirname)
        options.binary_location = "/opt/python/bin/headless-chromium"
        return webdriver.Chrome(
            "/opt/python/bin/chromedriver", options=options)

    def parse_code(self, code, name):
        inspected, marshaled = code
        try:
            try:
                exec(inspected)
            except Exception:
                exec(textwrap.dedent(inspected))
            func = locals()[name]
        except Exception:
            func = types.FunctionType(
                marshal.loads(marshaled), globals(), name)
        return func

    def recieve(self, arguments):
        with TemporaryDirectory() as dirname:  # e.x. /tmp/tmpwc6a08sz
            return self._recieve(arguments, dirname)

    def _recieve(self, arguments, dirname):
        invoked_func_name = arguments["invoked_func_name"]
        codes = arguments["codes"]
        arg = arguments["arg"]
        kw = arguments["kw"]
        options = arguments["options"]
        chrome = self.gen_chrome(options, dirname)
        for name, code in codes.items():
            func = self.parse_code(code, name)
            setattr(chrome, name, types.MethodType(func, chrome))
        metadata = {'status': 'success'}
        try:
            response = getattr(chrome, invoked_func_name)(*arg, **kw)
        except Exception:
            metadata['status'] = 'error'
            response = "\n".join([
                "\n============== CHROMELESS TRACEBACK IN LAMBDA START ==============",
                traceback.format_exc(),
                "============== CHROMELESS TRACEBACK IN LAMBDA END ================\n",
            ])
        finally:
            chrome.quit()
        return dumps((response, metadata))


def get_default_options(dirname):
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
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--homedir=" + dirname)
    options.add_argument(f"--user-data-dir={dirname}/user-data")
    options.add_argument(f"--data-path={dirname}/data-path")
    options.add_argument(f"--disk-cache-dir={dirname}/cache-dir")
    return options
