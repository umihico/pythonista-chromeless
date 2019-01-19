from lambda_function import lambda_handler
import sys
sys.path.append('..')
from pypi.chromeless.chromeless import Chromeless, dump_code, unpickle_result


def get_title(self, url):
    self.get(url)
    return self.title


def get_as_list(self):
    self.get("https://stackoverflow.com/")
    question_titles = [e.text for e in self.find_elements_by_xpath(
        "//h3/a[@class='question-hyperlink']")]
    return question_titles


def request(func, arg, kwargs):
    print(func.__name__, arg, kwargs)
    data = dump_code(func, arg, kwargs)
    event = {
        "httpMethod": "POST",
        "body": data
    }
    d = lambda_handler(event, None)
    statusCode = d['statusCode']
    response = unpickle_result(d['body'])
    print("statusCode", statusCode)
    print(response)
    print(type(response))


def test():
    request(get_title, ("https://github.com",), {})
    request(get_as_list, (), {})


if __name__ == '__main__':
    test()
