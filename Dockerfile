FROM lambci/lambda:build-python3.7

RUN mkdir -p /app
RUN mkdir -p /opt/python/bin/

WORKDIR /opt
RUN curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
RUN unzip chromedriver.zip -d python/bin/
RUN curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
RUN unzip headless-chromium.zip -d python/bin/
RUN rm -rf chromedriver.zip headless-chromium.zip

RUN yum install -y gcc-c++ make
RUN curl -sL https://rpm.nodesource.com/setup_14.x | bash -
RUN yum install -y nodejs
RUN npm install -g serverless

RUN pip install selenium -t python
RUN zip -r /app/layer.zip python

WORKDIR /app

RUN pip install awscli
RUN pip install selenium
RUN pip install boto3
RUN pip install -U pytest
RUN pip install Pillow
RUN pip install requests
RUN pip install setuptools
RUN pip install wheel
RUN pip install twine

COPY Dockerfile /app/
COPY LICENSE /app/
COPY Makefile /app/
COPY README.md /app/
RUN mkdir -p /app/chromeless
COPY chromeless/*.py /app/chromeless/
COPY __version__.py /app/chromeless/
COPY serverless.yml /app/
COPY *.py /app/
COPY chromeless/picklelib.py /app/

CMD ["sls", "deploy"]
