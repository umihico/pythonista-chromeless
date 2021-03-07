#!/bin/bash
set -euxo pipefail

if [ "$(pwd)" = "/latest" ]; then
  until $(python /local/chromeless/__version__.py); do sleep 5; done
fi

cp /tests.py ./
cp /example.py ./
pytest tests.py -ra
pytest example.py -ra
