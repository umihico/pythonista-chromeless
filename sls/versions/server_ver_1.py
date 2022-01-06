from tempfile import mkdtemp
import types
from selenium import webdriver
from picklelib import dumps  # imports in Dockerfile
import marshal
import textwrap


class ChromelessServer():
    SERVER_VERSION = 1

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

    def recieve(self, arguments):
        invoked_func_name = arguments["invoked_func_name"]
        codes = arguments["codes"]
        arg = arguments["arg"]
        kw = arguments["kw"]
        options = arguments["options"]
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
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--homedir=/tmp")
    options.add_argument(f"--homedir={mkdtemp()}")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    return options
