from chromeless import Chromeless as _Chromeless, dumps


class Chromeless(_Chromeless):
    def __invoke_local(self, dumped):
        print("__invoke_local")
        print(dumped)
        with open('/tmp/dumped.txt', 'w') as f:
            f.write(dumped)
        return dumps(("hoge", {"status": "succeess"}))


def get_title(self, url):
    self.get(url)
    return self.title


if __name__ == '__main__':
    chrome = Chromeless()
    chrome.attach(get_title)
    print(chrome.get_title("https://example.com"))
