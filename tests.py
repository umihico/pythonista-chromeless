from chromeless import Chromeless
from example import example, assert_response, demo_url, supposed_title


def test_example_normally():
    from selenium import webdriver
    from server import get_default_options
    import types
    options = get_default_options()
    options.binary_location = "/opt/python/bin/headless-chromium"
    chrome = webdriver.Chrome(
        "/opt/python/bin/chromedriver", options=options)
    setattr(chrome, "example", types.MethodType(example, chrome))
    title, png, divcnt = chrome.example(demo_url)
    assert_response(title, png, divcnt)


def test_example_locally():
    chrome = Chromeless(function_name="local")
    chrome.attach(example)
    title, png, divcnt = chrome.example(demo_url)
    assert_response(title, png, divcnt)


def test_non_toplevel_func():
    def func(self, url):
        self.get(url)
        return self.title
    chrome = Chromeless(function_name="local")
    chrome.attach(func)
    assert supposed_title in chrome.func(demo_url).lower()


if __name__ == '__main__':
    test_non_toplevel_func()
