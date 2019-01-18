from gateway_credentials import url, apikey
from chromeless import Chromeless


def get_title(self, url):
    self.get(url)
    return self.title


def get_top_questions(self):
    self.get("https://stackoverflow.com/")
    question_titles = [e.text for e in self.find_elements_by_xpath(
        "//h3/a[@class='question-hyperlink']")]
    return question_titles


def test():
    chrome = Chromeless(url, apikey)
    chrome.attach_method(get_title)
    print(chrome.get_title("https://google.com"))
    chrome = Chromeless(url, apikey)
    chrome.attach_method(get_top_questions)
    print(chrome.get_top_questions())


if __name__ == '__main__':
    test()
