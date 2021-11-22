FROM python:3.7-buster

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt install -y tesseract-ocr tesseract-ocr-jpn

COPY pytest/requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir /0.2.9 && pip install 'chromeless==0.2.9' -t /0.2.9/ && \
    mkdir /0.3.0 && pip install 'chromeless==0.3.0' -t /0.3.0/ && \
    mkdir /0.3.6 && pip install 'chromeless==0.3.6' -t /0.3.6/ && \
    mkdir /0.4.7 && pip install 'chromeless==0.4.7' -t /0.4.7/ && \
    mkdir /0.4.8 && pip install 'chromeless==0.4.8' -t /0.4.8/

COPY chromeless /latest/chromeless
COPY example.py /
COPY pytest/tests.py /
COPY pytest/docker-entrypoint.sh /
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
