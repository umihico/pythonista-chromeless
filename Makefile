build:
	docker build -t umihico/chromelessenv .

build_test:
	docker build -t umihico/chromelesstest -f test/Dockerfile .

bash:
	docker run --rm -it \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelessenv bash

release:
	@make build
	@make test_local
	@make deploy
	@make pypi_stg
	@make build_test
	@make test_stg
	@make pypi_prod
	@make build_test
	@make test_prod
	docker push umihico/chromelessenv:latest # docker.io/umihico/chromelessenv

deploy:
	docker run --rm -it \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelessenv sls deploy

test_local:
	docker run --rm -it \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelessenv pytest tests.py

test_stg:
	@make test_common STAGE=stg
test_prod:
	@make test_common STAGE=prod

test_common:
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelesstest make _test_common

_test_common:
	sh pipinstall.sh
	$(eval API_URL := $(shell sls info -v | grep ServiceEndpoint | sed s/ServiceEndpoint\:\ //g))
	$(eval STAGE := $(shell sls info -v | grep stage | sed s/stage\:\ //g))
	$(eval API_KEY := $(shell sls info -v | grep chromeless-apikey | sed s/\ chromeless-apikey-$(STAGE)\:\ //g))
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py
	pip install 'chromeless==0.2.9'
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py
	pip install 'chromeless==0.3.0'
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py
	pip install 'chromeless==0.3.6'
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py

pypi_common:
	docker build . -t umihico/pypienv_$(dir_name) -f pypi/Dockerfile
	touch $(dir_name)/__version__.py
	docker run --rm \
		--mount type=bind,source=$(shell pwd)/$(dir_name)/__version__.py,target=/app/$(dir_name)/__version__.py \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/pypienv_$(dir_name) make _pypi_$(stage) pip_name=chromeless dir_name=$(dir_name)

_pypi_common:
	PKG_NAME=$(pip_name) DIR_NAME=$(dir_name) STAGE=$(stage) python define_version.py
	PKG_NAME=$(pip_name) DIR_NAME=$(dir_name) STAGE=$(stage) python setup.py bdist_wheel

pypi_stg:
	@make pypi_common stage=stg dir_name=chromeless

_pypi_stg:
	@make _pypi_common stage=stg pip_name=$(pip_name)
	PKG_NAME=$(pip_name) twine upload --repository testpypi dist/* \
	-u $(shell aws ssm get-parameter --name PYPI_USERNAME_TEST --query 'Parameter.Value' --output text) \
	-p $(shell aws ssm get-parameter --name PYPI_PASSWORD_TEST --query 'Parameter.Value' --output text)
	PKG_NAME=$(pip_name) python pip_install.py stg

pypi_prod:
	@make pypi_common stage=prod dir_name=chromeless

_pypi_prod:
	@make _pypi_common stage=prod
	PKG_NAME=$(pip_name) twine upload dist/* \
	-u $(shell aws ssm get-parameter --name PYPI_USERNAME_PROD --query 'Parameter.Value' --output text) \
	-p $(shell aws ssm get-parameter --name PYPI_PASSWORD_PROD --query 'Parameter.Value' --output text)
	PKG_NAME=$(pip_name) python pip_install.py prod
