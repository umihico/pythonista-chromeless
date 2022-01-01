ARG LOCAL_PYTHON_VERSION
FROM python:${LOCAL_PYTHON_VERSION}-buster

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt install -y tesseract-ocr tesseract-ocr-jpn

WORKDIR /work

COPY pytest/requirements.txt ./
RUN pip install -r requirements.txt

COPY example.py pytest/tests.py ./

ENV PIP_INDEX_URL=http://pypiserver:8080/simple
ENV PIP_EXTRA_INDEX_URL=http://pypi-cache-server:8080/simple
ENV PIP_TRUSTED_HOST="pypi-cache-server pypiserver"

ARG CACHEBUST=1
ARG LOCAL_CHROMELESS_PYPI_VERSION
RUN echo pip install chromeless==${LOCAL_CHROMELESS_PYPI_VERSION} > ./docker-entrypoint.sh && \
    echo pytest example.py tests.py -ra >> ./docker-entrypoint.sh && \
    chmod +x ./docker-entrypoint.sh

CMD [ "sh", "docker-entrypoint.sh" ]
