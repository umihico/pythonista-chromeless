from apigateway_credentials import awsgateway_url, awsgateway_apikey
from pypi.chromeless.chromeless import Chromeless


def get_title(self, url):
    """basic example"""
    self.get(url)
    return self.title


def get_list(self):
    """returning <class 'list'> example"""
    self.get("https://stackoverflow.com/")
    question_titles = [e.text for e in self.find_elements_by_xpath(
        "//h3/a[@class='question-hyperlink']")]
    return question_titles


def get_title_letter_num(self, url):
    """binding multiple method example"""
    return len(self.get_title(url))


def get_screenshot(self, url, filename):
    """screenshot test"""
    self.get(url)
    self.save_screenshot(filename)


def run_examples():

    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_title)
    result = chrome.get_title("https://google.com")
    print(result, type(result))
    # Google <class 'str'>

    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_list)
    result = chrome.get_list()
    print(result[:2], type(result))
    # ['JSoup: how to list links from a list?', 'How to Fix PHPSESSID issue in Symfony 3.4'] <class 'list'>

    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_title)
    chrome.attach_method(get_title_letter_num)
    result = chrome.get_title_letter_num("http://github.com")
    print(result, type(result))
    # 58 <class 'int'>

    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    result = chrome.get("http://aws.amazon.com")
    print(result, type(result))
    # None <class 'NoneType'>

    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_screenshot)
    result = chrome.get_screenshot("https://github.com/umihico", "screenshot.png")
    print(result, type(result))
    # None <class 'NoneType'>


if __name__ == '__main__':
    run_examples()
