# chromeless
AWS lambda with selenium & python is powerful solution.  
Let's access this benefit easily!

+ Don't create lambda functions every time. Just create this once.
+ Write the method.
+ Selenium dynamically execute your script.

## Example
```python
# Write the method.
def get_title(self, url):
    self.get(url)
    return self.title

# Attach the method and then call it.
from chromeless import Chromeless
chrome = Chromeless()
chrome.attach(get_title)
print(chrome.get_title("https://google.com")) # Returns Google
```

## Installing
  + `docker run -e AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) -e AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key) -e AWS_DEFAULT_REGION=$(aws configure get region) umihico/chromelessenv`
  + `pip install chromeless`

That's it! Now run the `example.py` and confirm that it works!

## Tips
+ **Don't call selenium native methods directly.** Solution is wrapping.

```python
# BAD EXAMPLE
chrome = Chromeless()
chrome.get("https://google.com") # Not a attached method. AttributeError will be raised.
chrome.title # Same. AttributeError.

# SOLUTION
def wrapper(self, url):
    self.get(url)
    return self.title

chrome = Chromeless()
chrome.attach(wrapper)
print(chrome.wrapper("https://google.com")) # prints 'Google'.
print(chrome.wrapper("https://microsoft.com")) # But you can execute as many times as you want.
print(chrome.wrapper("https://apple.com")) # Arguments are adjustable each time.
```

+ Multiple methods are also attachable.

```python
def login(self):
    self.get("https://example.com/login")
    self.find_element_by_id("username").send_keys("umihico")
    self.find_element_by_id("password").send_keys("password")
    self.find_element_by_name("submit").click()

def test1(self):
    self.login()
    self.get("https://example.com/")

def test2(self):
    self.login()
    self.get("https://example.com/logout")

chrome = Chromeless()
chrome.attach(login) # You can attach multiple methods too.
chrome.attach(test1) # It means you can also refactor the common code.
chrome.attach(test2)
print(chrome.test1())
print(chrome.test2())
```

+ To screenshot

```python
# BAD EXAMPLE
def bad_wrapper(self):
  self.get("https://google.com")
  self.save_screenshot("screenshot.png")
  # There's no sense in saving files in AWS Lambda.

# SOLUTION
def good_wrapper(self):
  self.get("https://google.com")
  return self.get_screenshot_as_png()
  # return image in binary format.

chrome = Chromeless()
chrome.attach(good_wrapper)
png = chrome.good_wrapper()
# then write then image down locally.
with open("screenshot.png", 'wb') as f:
    f.write(png)

```

### [License](https://github.com/umihico/pythonista-chromeless/blob/master/LICENSE)
The project is licensed under the MIT license.
