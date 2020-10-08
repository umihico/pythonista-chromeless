from chromeless import Chromeless
from example import example, second_method, assert_response, demo_url, supposed_title


def test_example_normally():
    from selenium import webdriver
    from server import get_default_options
    import types
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as dirname:  # e.x. /tmp/tmpwc6a08sz
        options = get_default_options(dirname)
        options.binary_location = "/opt/python/bin/headless-chromium"
        chrome = webdriver.Chrome(
            "/opt/python/bin/chromedriver", options=options)
        setattr(chrome, "example", types.MethodType(example, chrome))
        setattr(chrome, "second_method",
                types.MethodType(second_method, chrome))
        title, png, divcnt = chrome.example(demo_url)
    assert_response(title, png, divcnt)


def test_example_locally():
    chrome = Chromeless(function_name="local")
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(demo_url)
    assert_response(title, png, divcnt)


def test_example_locally_named_arg():
    chrome = Chromeless(function_name="local")
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(url=demo_url)
    assert_response(title, png, divcnt)


def test_non_toplevel_func():
    def func(self, url):
        self.get(url)
        return self.title
    chrome = Chromeless(function_name="local")
    chrome.attach(func)
    assert supposed_title in chrome.func(demo_url).lower()


def test_error():
    chrome = Chromeless(function_name="local")
    from example import test_error
    test_error(chrome)


if __name__ == '__main__':
    test_error()
