from chromeless import Chromeless
import os

demo_url, supposed_title = "https://example.com/", "example domain"


def example(self, url):
    self.url = url
    title = self.second_method()
    png = self.get_screenshot_as_png()
    divcnt = len(self.find_elements_by_xpath("//div"))
    return title, png, divcnt


def second_method(self):
    self.get(self.url)
    return self.title


def test_example_with_session(**session_kw):
    """
    example usage:
        test_example_with_session(aws_access_key_id='<YOUR ACCESS KEY ID>',
         aws_secret_access_key='<YOUR SECRET KEY>',
         region_name='<REGION NAME>')
    """
    from boto3.session import Session
    session = Session(**session_kw)
    chrome = Chromeless(boto_session=session)
    test_example(chrome)


def test_example(chrome=None):
    chrome = chrome or Chromeless()
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(demo_url)
    assert_response(title, png, divcnt)


def test_api():
    chrome = Chromeless(os.getenv('API_URL', "None"),
                        os.getenv('API_KEY', "None"))
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(demo_url)
    print(title, demo_url)
    assert_response(title, png, divcnt)


def assert_response(title, png, divcnt):
    assert supposed_title in title.lower()
    with open('./img.png', 'wb') as f:
        f.write(png)
    from PIL import Image
    width, height = Image.open('./img.png').size
    assert width > 0 and height > 0
    assert divcnt > 0


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


if __name__ == '__main__':
    test_example()