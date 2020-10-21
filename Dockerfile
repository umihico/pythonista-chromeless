FROM lambci/lambda:build-python3.7

RUN mkdir -p /app
RUN mkdir -p /opt/python/bin/
RUN mkdir -p /tmp/downloads

WORKDIR /opt
RUN curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > /tmp/downloads/chromedriver.zip
RUN unzip /tmp/downloads/chromedriver.zip -d python/bin/
RUN curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > /tmp/downloads/headless-chromium.zip
RUN unzip /tmp/downloads/headless-chromium.zip -d python/bin/

RUN yum install -y gcc-c++ make
RUN curl -sL https://rpm.nodesource.com/setup_14.x | bash -
RUN yum install -y nodejs
RUN npm install -g serverless

RUN pip install selenium -t python
RUN zip -r /app/layer.zip python

RUN pip install awscli
RUN pip install selenium
RUN pip install boto3
RUN pip install -U pytest
RUN pip install Pillow
RUN pip install requests

RUN mkdir -p /opt/fonts
RUN mkdir -p /tmp/downloads/fonts
# Download your language
RUN curl -SL https://fonts.google.com/download?family=Noto%20Sans%20JP > /tmp/downloads/Noto_Sans_JP.zip
RUN unzip /tmp/downloads/Noto*.zip -d /tmp/downloads/fonts/
# Copy font files here
RUN mv /tmp/downloads/fonts/NotoSansJP-Regular.otf fonts/
COPY fonts.conf fonts/
RUN zip -r /app/fontlayer.zip fonts

WORKDIR /app
COPY Dockerfile /app/
COPY LICENSE /app/
COPY Makefile /app/
COPY README.md /app/
RUN mkdir -p /app/chromeless
COPY chromeless/*.py /app/chromeless/
RUN mkdir -p /app/versions
COPY versions/*.py /app/versions/
COPY serverless.yml /app/
COPY *.py /app/
COPY test/tests.py /app/
COPY chromeless/picklelib.py /app/

RUN rm -rf /tmp/downloads

CMD ["sls", "deploy"]
