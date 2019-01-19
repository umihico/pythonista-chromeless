from pypi.chromeless.chromeless import Chromeless


def get_title(self, url):
    self.get(url)
    return self.title


def get_as_list(self):
    self.get("https://stackoverflow.com/")
    question_titles = [e.text for e in self.find_elements_by_xpath(
        "//h3/a[@class='question-hyperlink']")]
    return question_titles
