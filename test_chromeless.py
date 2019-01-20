import examples
import unittest
from apigateway_credentials import awsgateway_url, awsgateway_apikey
from pypi.chromeless.chromeless import Chromeless
import os


def gen_attached_chrome(func):
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(func)
    return chrome


class TestChromeless(unittest.TestCase):
    def test_get_title(self):
        chrome = gen_attached_chrome(examples.get_title)
        title = chrome.get_title("https://google.com")
        self.assertTrue(type(title) is str)
        self.assertTrue("Google" in title)

    def test_get_list(self):
        chrome = gen_attached_chrome(examples.get_list)
        top_questions = chrome.get_list()
        self.assertTrue(type(top_questions) is list)
        self.assertTrue(len(top_questions) > 0)

    def test_get_title_letter_num(self):
        chrome = gen_attached_chrome(examples.get_title_letter_num)
        chrome.attach_method(examples.get_title)
        letter_num = chrome.get_title_letter_num("http://github.com")
        self.assertTrue(type(letter_num) is int)
        self.assertTrue(letter_num > 0)

    def test_get(self):
        chrome = Chromeless(awsgateway_url, awsgateway_apikey)
        result = chrome.get("http://aws.amazon.com")
        self.assertTrue(result is None)

    def test_get_screenshot(self):
        chrome = Chromeless(awsgateway_url, awsgateway_apikey)
        chrome.attach_method(examples.get_screenshot)
        path = "screenshot.png"
        result = chrome.get_screenshot("https://github.com/umihico", path)
        self.assertTrue(result is None)
        self.assertTrue(os.path.exists(path))


if __name__ == '__main__':
    unittest.main()
