FROM public.ecr.aws/lambda/python:3.7

RUN mkdir -p /opt/bin/ && \
    mkdir -p /opt/fonts/ && \
    mkdir -p /tmp/downloads/fonts && \
    curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > /tmp/downloads/chromedriver.zip && \
    curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > /tmp/downloads/headless-chromium.zip && \
    curl -SL https://fonts.google.com/download?family=Noto%20Sans%20JP > /tmp/downloads/Noto_Sans_JP.zip && \
    unzip /tmp/downloads/chromedriver.zip -d /opt/bin/ && \
    unzip /tmp/downloads/headless-chromium.zip -d /opt/bin/ && \
    unzip /tmp/downloads/Noto*.zip -d /tmp/downloads/fonts/ && \
    mv /tmp/downloads/fonts/NotoSansJP-Regular.otf /opt/fonts/ && \
    rm -rf /tmp/downloads

COPY sls/requirements.txt ./
RUN pip install -r requirements.txt

COPY sls/server.py ./
COPY chromeless/picklelib.py ./
COPY sls/fonts.conf /opt/fonts/
COPY sls/versions/ ./versions/
CMD ["server.handler"]
