from apigateway_credentials import awsgateway_url, awsgateway_apikey
from pypi.chromeless.chromeless import Chromeless


def get_title(self, url):
    self.get(url)
    return self.title


def get_list(self):
    self.get("https://stackoverflow.com/")
    question_titles = [e.text for e in self.find_elements_by_xpath(
        "//h3/a[@class='question-hyperlink']")]
    return question_titles


def run_examples():
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)

    chrome.attach_method(get_title)
    result = chrome.get_title("https://google.com")
    print(result, type(result))
    # Google <class 'str'>

    chrome.attach_method(get_list)
    result = chrome.get_list()
    print(result[:2], type(result))
    # ['JSoup: how to list links from a list?', 'How to Fix PHPSESSID issue in Symfony 3.4'] <class 'list'>


if __name__ == '__main__':
    run_examples()
