import examples
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
import unittest
from apigateway_credentials import awsgateway_url, awsgateway_apikey
from pypi.chromeless.chromeless import Chromeless, LambdaAlreadyTriggeredException
import os


def test_chrome_options():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--homedir=/tmp")
    return chrome_options


def gen_attached_chrome(func, chrome_options=None):
    chrome_options = chrome_options or test_chrome_options()
    chrome = Chromeless(awsgateway_url, awsgateway_apikey, chrome_options=chrome_options)
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
        chrome = gen_attached_chrome(examples.get_screenshot)
        path = "screenshot.png"
        result = chrome.get_screenshot("https://github.com/umihico", path)
        self.assertTrue(result is None)
        self.assertTrue(os.path.exists(path))

    def test_trigger_twice(self):
        chrome = gen_attached_chrome(examples.get_title)
        chrome.get_title("http://github.com")
        with self.assertRaises(LambdaAlreadyTriggeredException):
            chrome.get_title("https://google.com")

    def test_cause_NoSuchElementException(self):
        chrome = gen_attached_chrome(examples.cause_NoSuchElementException)
        with self.assertRaises(NoSuchElementException):
            chrome.cause_NoSuchElementException()

    def test_get_screenshot_with_changed_windowsize(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        # default is "--window-size=1280x1696"
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--log-level=0")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--homedir=/tmp")
        chrome = gen_attached_chrome(examples.get_screenshot, chrome_options=chrome_options)
        path = "screenshot.png"
        result = chrome.get_screenshot("https://github.com/umihico", path)
        self.assertTrue(result is None)
        self.assertTrue(os.path.exists(path))


if __name__ == '__main__':
    unittest.main(failfast=True)
