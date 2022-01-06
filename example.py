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


def test_example():
    chrome = Chromeless()
    chrome.attach(example)
    chrome.attach(second_method)
    result = chrome.example(demo_url)
    print(result)
    return result


def test_api():
    chrome = Chromeless(os.getenv('API_URL', "None"),
                        os.getenv('API_KEY', "None"))
    chrome.attach(example)
    chrome.attach(second_method)
    result = chrome.example(demo_url)
    print(result)
    return result


if __name__ == '__main__':
    test_example()
