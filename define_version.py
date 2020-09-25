import requests
import os

stage = os.getenv('STAGE', 'test')
host = 'pypi.org' if stage == 'prod' else 'test.pypi.org'
try:
    json = requests.get(f'https://{host}/pypi/chromeless/json').json()
    version = json['info']['version']
except Exception:  # first deploy
    version = '0.0.0'
x100, x10, x = map(int, version.split('.'))
new_version = ".".join(str(x100 * 100 + x10 * 10 + x + 1).zfill(3))
with open("__version__.py", "w") as f:
    f.write(f"__version__ = '{new_version}'")
    print(stage, f"__version__ = '{new_version}'")
