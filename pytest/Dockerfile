ARG LOCAL_PYTHON_VERSION
FROM python:${LOCAL_PYTHON_VERSION}-buster

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt install -y tesseract-ocr tesseract-ocr-jpn

WORKDIR /work

COPY pytest/requirements.txt ./
RUN pip install -r requirements.txt

COPY example.py pytest/tests.py pytest/interactive-test.py ./

ENV PIP_INDEX_URL=http://pypi-cache-server:8080/simple
ENV PIP_TRUSTED_HOST="pypi-cache-server pypiserver"

ARG CACHEBUST=1
ARG LOCAL_CHROMELESS_PYPI_VERSION
RUN echo "set -xve" > ./docker-entrypoint.sh && \
    echo "pip install chromeless==$LOCAL_CHROMELESS_PYPI_VERSION" >> ./docker-entrypoint.sh && \
    echo "cat interactive-test.py | python | grep -q OK || exit 1" >> ./docker-entrypoint.sh && \
    echo "pytest tests.py -ra" >> ./docker-entrypoint.sh && \
    chmod +x ./docker-entrypoint.sh

CMD [ "sh", "docker-entrypoint.sh" ]
