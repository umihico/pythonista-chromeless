from selenium.webdriver import Chrome


def save_screenshot(self, filename):
    png = self.get_screenshot_as_png()
    self.screenshothandler.append(filename, png)


Chrome.save_screenshot = save_screenshot


class ScreenshotHandler():
    def __init__(self, chrome):
        self.chrome = chrome
        chrome.screenshothandler = self
        self.screenshots = []

    def append(self, filename, png):
        self.screenshots.append((filename, png))

    def wrap_with_screenshots(self, result):
        return {
            'screenshots': self.screenshots,
            'origin_result': result,
        }
