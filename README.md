# chromeless

AWS lambda with selenium & python is powerful solution.
Let's access this benefit easily!

- Don't create lambda functions every time. Just create this once.
- Write the method.
- Selenium dynamically execute your script.

## Example

```python
# Write the method to a file. (NOT interactive mode.)
def get_title(self, url):
    self.get(url)
    return self.title

# Attach the method and then call it.
from chromeless import Chromeless
chrome = Chromeless()
chrome.attach(get_title)
print(chrome.get_title("https://google.com")) # Returns Google
```


You can also provide boto3 session object if you don't want to use default aws profile:
```python
from chromeless import Chromeless
from boto3.session import Session

session = Session(aws_access_key_id='<YOUR ACCESS KEY ID>',
                  aws_secret_access_key='<YOUR SECRET KEY>',
                  region_name='<REGION NAME>')
# or
session = Session(profile_name='<YOUR_PROFILE_NAME>')
chrome = Chromeless(boto3_session=session)
```

Or also you can just set appropriate environment vars works with boto3,
 so it will auto detect your choice e.g.:
```
# In mac or linux
export AWS_DEFAULT_REGION=<your aws region>

# In windows
set AWS_DEFAULT_REGION=<your aws region>
```

## Installing

- `git clone --depth 1 https://github.com/umihico/pythonista-chromeless.git chromeless && cd $_`
- `sls deploy --region YOUR_REGION`
- `pip install chromeless`

That's it! Now run the `example.py` and confirm your selenium works in lambda functions!

## Tips

- **Don't call selenium native methods directly.** Solution is wrapping.

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

- Multiple methods are also attachable.

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

- To screenshot

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
