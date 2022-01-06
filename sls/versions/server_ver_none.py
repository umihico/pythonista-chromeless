import types
from selenium import webdriver
from picklelib import loads, dumps  # imports in Dockerfile
import marshal
import textwrap


class ChromelessServer():
    def gen_chrome(self, options):
        if options is None:
            options = get_default_options()
        options.binary_location = "/opt/chrome/chrome"
        return webdriver.Chrome(
            "/opt/chromedriver", options=options)

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

    def recieve(self, dumped):
        invoked_func_name, codes, arg, kw, options = loads(dumped)
        chrome = self.gen_chrome(options)
        for name, code in codes.items():
            func = self.parse_code(code, name)
            setattr(chrome, name, types.MethodType(func, chrome))
        try:
            return dumps(getattr(chrome, invoked_func_name)(*arg, **kw))
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
