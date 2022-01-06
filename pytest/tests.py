import os
from chromeless import Chromeless
import chromeless
from example import example, second_method, demo_url, supposed_title, test_example as _test_example, test_api as _test_api
from PIL import Image
import pyocr
import pyocr.builders
from boto3.session import Session
from packaging import version
chromeless_version = chromeless.__version__ if hasattr(
    chromeless, '__version__') else '0.0.1'


def assert_response(title, png, divcnt):
    assert supposed_title in title.lower()
    with open('./img.png', 'wb') as f:
        f.write(png)
    width, height = Image.open('./img.png').size
    assert width > 0 and height > 0
    assert divcnt > 0


def test_example():
    assert_response(*_test_example())


def test_api():
    assert_response(*_test_api())


if version.parse(chromeless_version) >= version.parse("0.9.0") and os.getenv('CHROMELESS_SERVER_FUNCTION_NAME', "") != "local":
    def test_example_with_session_arg():
        session = Session()  # valid default session
        chrome = Chromeless(boto3_session=session)
        chrome.attach(example)
        chrome.attach(second_method)
        title, png, divcnt = chrome.example(demo_url)
        assert_response(title, png, divcnt)  # should work

        session = Session(aws_access_key_id='FOO',
                          aws_secret_access_key='BAR',
                          region_name='ap-northeast-1')  # invalid session
        chrome = Chromeless(boto3_session=session)
        chrome.attach(example)
        chrome.attach(second_method)
        try:
            chrome.example(demo_url)  # shouldn't work
        except Exception as e:
            assert str(e).startswith("Invalid session or AWS credentials")
        else:
            raise Exception("No expected exception")


def test_example_locally_named_arg():
    chrome = Chromeless()
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(url=demo_url)
    assert_response(title, png, divcnt)


def test_non_toplevel_func():
    def child_func(self, url):
        self.get(url)
        return self.title
    chrome = Chromeless()
    chrome.attach(child_func)
    assert supposed_title in chrome.child_func(demo_url).lower()


def test_reserved_method_name_attached():
    def func(self, url):
        self.get(url)
        return self.title
    chrome = Chromeless()
    chrome.attach(func)
    try:
        chrome.func(demo_url).lower()
    except Exception:
        import traceback
        detail = traceback.format_exc()
        REQUIRED_SERVER_VERSION = chrome.REQUIRED_SERVER_VERSION if hasattr(
            chrome, "REQUIRED_SERVER_VERSION") else None
        if REQUIRED_SERVER_VERSION == 1 or REQUIRED_SERVER_VERSION is None:
            assert "return pickle.loads(zlib.decompress(base64.b64decode(obj.encode())))" in detail
        else:
            assert "CHROMELESS TRACEBACK IN LAMBDA START" in detail
            assert "'func' might be reserved variable name in chromeless. Please retry after re-naming." in detail
            assert "CHROMELESS TRACEBACK IN LAMBDA END" in detail


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


def test_error(chrome=None):
    def method(self, url):
        self.get(url)
        self.find_element_by_xpath("//invalid")

    chrome = Chromeless() if chrome is None else chrome
    chrome.attach(method)
    try:
        chrome.method(demo_url)
    except Exception:
        import traceback
        detail = traceback.format_exc()
        REQUIRED_SERVER_VERSION = chrome.REQUIRED_SERVER_VERSION if hasattr(
            chrome, "REQUIRED_SERVER_VERSION") else None
        if REQUIRED_SERVER_VERSION == 1 or REQUIRED_SERVER_VERSION is None:
            assert "return pickle.loads(zlib.decompress(base64.b64decode(obj.encode())))" in detail
        else:
            assert "CHROMELESS TRACEBACK IN LAMBDA START" in detail
            assert "NoSuchElementException" in detail
            assert "CHROMELESS TRACEBACK IN LAMBDA END" in detail
    else:
        assert False
