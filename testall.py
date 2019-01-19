from apigateway_credentials import awsgateway_url, awsgateway_apikey
import examples
from pypi.chromeless.chromeless import Chromeless
import unittest


def gen_attached_chrome(func):
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(func)
    return chrome


class TestStringMethods(unittest.TestCase):
    def test_get_title(self):
        chrome = gen_attached_chrome(examples.get_title)
        title = chrome.get_title("https://google.com")
        self.assertTrue(type(title) is str)
        self.assertTrue("Google" in title)

    def test_get_as_list(self):
        chrome = gen_attached_chrome(examples.get_as_list)
        top_questions = chrome.get_as_list()
        self.assertTrue(type(top_questions) is list)
        self.assertTrue(len(top_questions) > 0)


if __name__ == '__main__':
    unittest.main()
