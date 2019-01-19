from lambda_function import lambda_handler
import sys
sys.path.append('..')
from pypi.chromeless.chromeless import Chromeless, dump_code


def get_title(self, url):
    self.get(url)
    return self.title


def test(func, arg, kwargs):
    data = dump_code(func, arg, kwargs)
    event = {
        "httpMethod": "POST",
        "body": data
    }
    response = lambda_handler(event, None)
    print(response)
    print(type(response))


if __name__ == '__main__':
    test(get_title, ("https://github.com",), {})
