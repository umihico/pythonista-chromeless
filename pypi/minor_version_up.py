
from os.path import dirname, join
import requests
json = requests.get(f'https://test.pypi.org/pypi/chromeless/json').json()
version = json['info']['version']
x100, x10, x = version.split('.')
new_version = ".".join([x100, x10, str(int(x)+1)])
with open(join(dirname(dirname(__file__)), "chromeless/__version__.py"), "w") as f:
    f.write(f"__version__ = '{new_version}'")
