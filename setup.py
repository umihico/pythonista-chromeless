import requests
import setuptools
import os


def get_incremented_version():
    stage = os.getenv('STAGE', 'test')
    host = 'pypi.org' if stage == 'prod' else 'test.pypi.org'
    try:
        json = requests.get(f'https://{host}/pypi/chromeless/json').json()
        version = json['info']['version']
    except Exception:  # first deploy
        version = '0.0.0'
    x100, x10, x = map(int, version.split('.'))
    new_version = ".".join(str(x100 * 100 + x10 * 10 + x + 1).zfill(3))
    return new_version


requirements = [
    'requests',
    'boto3',
]

with open("README.md", "r") as f:
    long_description = f.read()
setuptools.setup(
    name="chromeless",
    version=get_incremented_version(),
    author="umihico",
    author_email="umihico@users.noreply.github.com",
    description="Serverless selenium which dynamically execute any given code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/umihico/pythonista-chromeless",
    packages=['chromeless'],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
