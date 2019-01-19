from gateway_credentials import url, apikey
from chromeless import Chromeless


def get_title(self, url):
    self.get(url)
    return self.title


def test_get_title():
    chrome = Chromeless(url, apikey)
    chrome.attach_method(get_title)
    title = chrome.get_title("https://google.com")
    print(title)
    return bool("Google" in title)


if __name__ == '__main__':
    test_get_title()
