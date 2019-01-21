import unittest
import sys
import selenium
from selenium.webdriver import ChromeOptions
from lambda_function import lambda_handler
sys.path.insert(0, '..')
import examples
from pypi.chromeless.chromeless import Chromeless, _unpickle_result, _dump_codes, _exact_result_and_save_screenshots
from selenium.webdriver import Chrome


def request(func, *arg, **kwargs):
    examples_funcs = [
        examples.get_title,
        examples.get_list,
        examples.get_title_letter_num,
        examples.get_screenshot,
        examples.cause_NoSuchElementException,
    ]
    called_name_as_method = func.__name__
    stored_funcs = {func.__name__: func for func in examples_funcs}
    # print(called_name_as_method, arg, kwargs)
    chrome_options = kwargs.get("chrome_options", None)
    if chrome_options:
        del kwargs['chrome_options']
    data = _dump_codes(called_name_as_method, arg, kwargs, stored_funcs, chrome_options)
    event = {
        "httpMethod": "POST",
        "body": data
    }
    d = lambda_handler(event, None)
    statusCode = d['statusCode']
    response = _exact_result_and_save_screenshots(_unpickle_result(d['body']))
    return response


class TestLambda(unittest.TestCase):
    def test_get_title(self):
        title = request(examples.get_title, "https://google.com")
        self.assertTrue(type(title) is str)
        self.assertTrue("Google" in title)

    def test_get_list(self):
        top_questions = request(examples.get_list)
        self.assertTrue(type(top_questions) is list)
        self.assertTrue(len(top_questions) > 0)

    def test_get_title_letter_num(self):
        letter_num = request(examples.get_title_letter_num, "http://github.com")
        self.assertTrue(type(letter_num) is int)
        self.assertTrue(letter_num > 0)

    def test_get(self):
        result = request(Chrome.get, "http://aws.amazon.com")
        self.assertTrue(result is None)

    def test_get_screenshot(self):
        result = request(Chrome.get_screenshot, "https://github.com/umihico", "screenshot.png")

    def test_cause_NoSuchElementException(self):
        result = request(examples.cause_NoSuchElementException)
        # print(type(result))
        with self.assertRaises(selenium.common.exceptions.NoSuchElementException):
            raise result

    def test_chrome_options(self):
        chrome_options = ChromeOptions()
        chrome_options.binary_location = "./bin/headless-chromium"
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
        title = request(examples.get_title, "https://google.com", chrome_options=chrome_options)
        self.assertTrue(type(title) is str)
        self.assertTrue("Google" in title)

    def test_empty_chrome_options(self):
        chrome_options = ChromeOptions()
        chrome_options.binary_location = "./bin/headless-chromium"
        title = request(examples.get_title, "https://google.com", chrome_options=chrome_options)
        # works without chrome_options
        self.assertTrue(type(title) is str)
        self.assertTrue("Google" in title)


if __name__ == '__main__':
    unittest.main(failfast=True)
