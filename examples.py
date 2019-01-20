try:
    """developer in git env"""
    from apigateway_credentials import awsgateway_url, awsgateway_apikey
    from pypi.chromeless.chromeless import Chromeless
except Exception as e:
    """general user who downloaded this script"""
    # pip install chromeless
    from chromeless import Chromeless
    # replace credentials
    awsgateway_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    awsgateway_url = "https://XXXXXXXXXX.execute-api.us-west-2.amazonaws.com/default/chromeless"


def get_title(self, url):
    self.get(url)
    return self.title


def example_of_get_title():
    """basic example"""
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_title)
    result = chrome.get_title("https://google.com")
    print(result, type(result))
    # Google <class 'str'>


def get_list(self):
    self.get("https://stackoverflow.com/")
    question_titles = [e.text for e in self.find_elements_by_xpath(
        "//h3/a[@class='question-hyperlink']")]
    return question_titles


def example_of_get_list():
    """you can get any type if it's picklable. this is <class 'list'> example"""
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_list)
    result = chrome.get_list()
    print(result[:2], type(result))
    # ['JSoup: how to list links from a list?', 'How to Fix PHPSESSID issue in Symfony 3.4'] <class 'list'>


def get_title_letter_num(self, url):
    return len(self.get_title(url))


def example_of_get_title_letter_num():
    """
    you can call only one method,
    but you can bind multiple method and use them all by wrapping.
    """
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_title)
    chrome.attach_method(get_title_letter_num)
    result = chrome.get_title_letter_num("http://github.com")
    print(result, type(result))
    # 58 <class 'int'>


def get_screenshot(self, url, filename):
    self.get(url)
    self.save_screenshot(filename)


def example_of_get_screenshot():
    """
    just use the same local path argument as same as origin Chrome.save_screenshot(path).
    Chromeless will transfer from lambda to your local.
    """
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_screenshot)
    result = chrome.get_screenshot("https://github.com/umihico", "screenshot.png")
    print(result, type(result))
    # None <class 'NoneType'>


def example_of_default_method():
    """
    you can also run simple default method on Chrome
    """
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    result = chrome.get("http://aws.amazon.com")
    print(result, type(result))
    # None <class 'NoneType'>


if __name__ == '__main__':
    example_of_get_title()
    example_of_get_list()
    example_of_get_title_letter_num()
    example_of_get_screenshot()
    example_of_default_method()
