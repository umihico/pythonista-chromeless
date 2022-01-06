FROM python:3.8-buster

RUN pip install setuptools wheel twine requests
WORKDIR /work
COPY README.md pypi/setup.py chromeless/__version__.py ./
COPY chromeless ./chromeless
RUN python setup.py bdist_wheel
