from chromeless import Chromeless
from example import example, second_method, assert_response, demo_url, supposed_title
import os
from PIL import Image
import sys
import pyocr
import pyocr.builders


def test_example_locally():
    chrome = Chromeless()
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(demo_url)
    assert_response(title, png, divcnt)


def test_example_locally_named_arg():
    chrome = Chromeless()
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(url=demo_url)
    assert_response(title, png, divcnt)


def test_non_toplevel_func():
    def func(self, url):
        self.get(url)
        return self.title
    chrome = Chromeless()
    chrome.attach(func)
    assert supposed_title in chrome.func(demo_url).lower()


def test_error():
    chrome = Chromeless()
    from example import test_error
    test_error(chrome)


def test_language():
    chrome = Chromeless()

    def wrapper(self):
        self.get("http://example.selenium.jp/reserveApp/")
        return self.get_screenshot_as_png()

    chrome.attach(wrapper)
    png = chrome.wrapper()
    with open('./jpn.png', 'wb') as f:
        f.write(png)

    tool = pyocr.get_available_tools()[0]
    txt = tool.image_to_string(
        Image.open('./jpn.png'),
        lang='jpn',
        builder=pyocr.builders.TextBuilder()
    )
    assert "予約フォーム" in txt or "朝食バイキング" in txt
