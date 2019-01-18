# from trigger import trigger
import types
from selenium.webdriver import Chrome
import marshal


def method(self):
    self.get("https://www.google.co.jp")
    title = self.title
    self.quit()
    print(title)
    return title


def dump_code(func):
    byte_func = marshal.dumps(func.__code__)
    funcname = func.__name__
    return funcname, byte_func


def load_code(funcname, byte_func):
    code = marshal.loads(byte_func)
    func = types.FunctionType(code, globals(), funcname)
    return func


def test_local_binding(sended_method):
    Chrome.sended_method = sended_method
    chrome = Chrome()
    print(chrome.sended_method())


def main():
    funcname, byte_func = dump_code(method)
    sended_method = load_code(funcname, byte_func)
    test_local_binding(sended_method)
    # trigger(method="POST", data={'methodname': funcname, 'bytecode': byte_func})


if __name__ == '__main__':
    main()
