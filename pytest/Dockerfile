ARG LOCAL_PYTHON_VERSION
FROM python:${LOCAL_PYTHON_VERSION}-buster

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt install -y tesseract-ocr tesseract-ocr-jpn

ENV PIP_INDEX_URL=http://host.docker.internal:18080/simple
ENV PIP_EXTRA_INDEX_URL=http://host.docker.internal:8080/simple
ENV PIP_TRUSTED_HOST="host.docker.internal"

WORKDIR /work

COPY pytest/requirements.txt ./
RUN pip install -r requirements.txt

COPY example.py pytest/tests.py ./

ARG CACHEBUST=1
ARG LOCAL_CHROMELESS_PYPI_VERSION
RUN pip install chromeless==${LOCAL_CHROMELESS_PYPI_VERSION}

CMD [ "pytest", "example.py", "tests.py", "-ra" ]
