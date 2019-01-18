from gateway_credentials import url, apikey
from serverlesschrome import ServerlessChrome


def get_title(self, url):
    self.get(url)
    return self.title


def test():
    schrome = ServerlessChrome(url, apikey)
    schrome.attach_method(get_title)
    print(schrome.get_title("https://google.com"))


if __name__ == '__main__':
    test()
