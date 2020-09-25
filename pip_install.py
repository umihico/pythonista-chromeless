import subprocess
import sys
from __version__ import __version__
import time

stage = "prod" if sys.argv[1] == "prod" else 'stg'
chunks = [sys.executable, "-m", "pip",
          "install", f'chromeless=={__version__}']
if stage == "stg":
    chunks.insert(4, "https://test.pypi.org/simple/")
    chunks.insert(4, "--index-url")

print(*chunks)

for i in range(100):
    try:
        subprocess.check_call(chunks)
    except Exception as e:
        print(e)
        time.sleep(10)
    else:
        break
