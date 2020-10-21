FROM python:3

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install nodejs
RUN npm install -g serverless

RUN pip install -U pytest
RUN pip install Pillow

RUN pip install chromeless==0.2.9
RUN pip install chromeless==0.3.0
RUN pip install chromeless==0.3.6

COPY example.py .
COPY chromeless/__version__.py .
COPY test/pipinstall.sh .
COPY Makefile .
COPY serverless.yml .
