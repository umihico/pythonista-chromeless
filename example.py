import random
from chromeless import Chromeless
import os

example_urls_with_title = [
    ('https://google.com', 'google'),
    ('https://nvidia.com', 'nvidia'),
    ('https://facebook.com', 'facebook'),
    ('https://apple.com', 'apple'),
    ('https://github.com', 'github'),
]

demo_url, supposed_title = random.choice(example_urls_with_title)


def example(self, url):
    self.url = url
    title = self.second_method()
    png = self.get_screenshot_as_png()
    divcnt = len(self.find_elements_by_xpath("//div"))
    return title, png, divcnt


def second_method(self):
    self.get(self.url)
    return self.title


def test_example():
    chrome = Chromeless()
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(demo_url)
    assert_response(title, png, divcnt)


def test_api():
    chrome = Chromeless(os.environ['API_URL'], os.environ['API_KEY'])
    chrome.attach(example)
    chrome.attach(second_method)
    title, png, divcnt = chrome.example(demo_url)
    assert_response(title, png, divcnt)


def assert_response(title, png, divcnt):
    assert supposed_title in title.lower()
    with open('./img.png', 'wb') as f:
        f.write(png)
    from PIL import Image
    width, height = Image.open('./img.png').size
    assert width > 0 and height > 0
    assert divcnt > 0


if __name__ == '__main__':
    test_example()
