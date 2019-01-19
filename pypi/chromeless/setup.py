from setuptools import setup, find_packages
import requests
import os
from ppickle import dump, load
package_info_filename = "package_info.ppickle"
package_info = load(package_info_filename)
USERNAME = package_info["USERNAME"]
REPONAME = package_info["REPONAME"] or os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
GITHUB_API_URL = package_info["GITHUB_API_URL"] or f"https://api.github.com/repos/{USERNAME}/{REPONAME}"
URL = package_info["URL"] or f'https://github.com/{USERNAME}/{REPONAME}'
AUTHOR_EMAIL = package_info["AUTHOR_EMAIL"] or f'{USERNAME}@users.noreply.github.com'
README_PATH = package_info["README_PATH"] or 'README.md'
requirements = [
    "requests",
]


def get_description():
    description = requests.get(GITHUB_API_URL).json()['description']
    return description


def get_topic():
    topics = requests.get(GITHUB_API_URL + "/topics", headers={
        "Accept": "application/vnd.github.mercy-preview+json", }).json()['names']
    return ' '.join(topics)


def increment_version():
    raw_version = package_info['version'] or '0.0.0'
    int_version = int(raw_version.replace('.', ''))  # 3
    int_version += 1
    new_version = '.'.join(str(int_version).zfill(3))  # 0.0.4
    package_info['version'] = new_version
    dump(package_info_filename, package_info)
    with open('version.txt', 'w') as f:
        f.write(new_version)
    return new_version


def get_long_description():
    with open(README_PATH, 'r', encoding='utf-8') as f:
        long_description = f.read()


description = get_description()
keywords = get_topic()
version = increment_version()
long_description = get_long_description()
setup(
    name=REPONAME,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author=USERNAME,
    author_email=AUTHOR_EMAIL,
    license='MIT',
    keywords=keywords,
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
