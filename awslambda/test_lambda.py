import unittest
import sys
from lambda_function import lambda_handler
sys.path.insert(0, '..')
import examples
sys.path.append('../pypi/chromeless')
from chromeless import Chromeless, unpickle_result, dump_codes
from selenium.webdriver import Chrome


def request(func, *arg, **kwargs):
    examples_funcs = [
        examples.get_title,
        examples.get_list,
        examples.get_title_letter_num
    ]
    called_name_as_method = func.__name__
    stored_funcs = {func.__name__: func for func in examples_funcs}
    # print(called_name_as_method, arg, kwargs)
    data = dump_codes(called_name_as_method, arg, kwargs, stored_funcs)
    event = {
        "httpMethod": "POST",
        "body": data
    }
    d = lambda_handler(event, None)
    statusCode = d['statusCode']
    if statusCode != 200:
        raise Exception(d['body'])
    response = unpickle_result(d['body'])
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


if __name__ == '__main__':
    unittest.main()
