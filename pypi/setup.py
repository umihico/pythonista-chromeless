import setuptools
from __version__ import __version__

requirements = [
    'requests',
    'boto3',
]

with open("README.md", "r") as f:
    long_description = f.read()
setuptools.setup(
    name="chromeless",
    version=__version__,
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
