"""
THIS FILE IS FOR TESTING INTERACTIVE MODE ONLY
"""

from chromeless import Chromeless


def get_title(self, url):
    self.get(url)
    return self.title


def attaching_from_interactive_mode():
    chrome = Chromeless()
    try:
        chrome.attach(get_title)
        chrome.get_title("https://example.com/")
    except RuntimeError as e:
        if "Chromeless does not support interactive mode. Please run from files." in str(e):
            print("OK")
        else:
            raise e
    except OSError as e:
        import chromeless
        from packaging import version
        if version.parse(chromeless.__version__) > version.parse("0.7.15"):
            raise e
        if "could not get source code" in str(e):
            print("OK")
    except Exception:
        raise
    else:
        raise Exception("Expected exception not raised")


if __name__ == '__main__':
    attaching_from_interactive_mode()
