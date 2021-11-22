#!/bin/bash
set -euxo pipefail

cp /tests.py ./
cp /example.py ./
pytest tests.py -ra
pytest example.py -ra
