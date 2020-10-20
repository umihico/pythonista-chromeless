build:
	docker build -t umihico/chromelessenv .
	docker build -t umihico/chromelesstest -f Dockerfile_test .

bash:
	docker run --rm -it \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelessenv bash

release:
	@make pypi_stg
	@make build
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelessenv make sls
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelesstest make test_compatibility
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelesstest make test_stg
	@make pypi_prod
	@make build
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelesstest make test_prod
	docker push umihico/chromelessenv:latest # docker.io/umihico/chromelessenv

deploy:
	docker run --rm -it \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelessenv sls deploy

sls:
	# test locally
	pytest tests.py

	# deploy sls
	sls deploy
	$(eval API_URL := $(shell sls info -v | grep ServiceEndpoint | sed s/ServiceEndpoint\:\ //g))
	$(eval STAGE := $(shell sls info -v | grep stage | sed s/stage\:\ //g))
	$(eval API_KEY := $(shell sls info -v | grep chromeless-apikey | sed s/\ chromeless-apikey-$(STAGE)\:\ //g))
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py

test_compatibility:
	$(eval API_URL := $(shell sls info -v | grep ServiceEndpoint | sed s/ServiceEndpoint\:\ //g))
	$(eval STAGE := $(shell sls info -v | grep stage | sed s/stage\:\ //g))
	$(eval API_KEY := $(shell sls info -v | grep chromeless-apikey | sed s/\ chromeless-apikey-$(STAGE)\:\ //g))
	pip install 'chromeless==0.2.9'
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py
	pip install 'chromeless==0.3.0'
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py
	pip install 'chromeless==0.3.6'
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py

test_stg:
	$(eval API_URL := $(shell sls info -v | grep ServiceEndpoint | sed s/ServiceEndpoint\:\ //g))
	$(eval STAGE := $(shell sls info -v | grep stage | sed s/stage\:\ //g))
	$(eval API_KEY := $(shell sls info -v | grep chromeless-apikey | sed s/\ chromeless-apikey-$(STAGE)\:\ //g))
	python pip_install.py stg
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py

test_prod:
	$(eval API_URL := $(shell sls info -v | grep ServiceEndpoint | sed s/ServiceEndpoint\:\ //g))
	$(eval STAGE := $(shell sls info -v | grep stage | sed s/stage\:\ //g))
	$(eval API_KEY := $(shell sls info -v | grep chromeless-apikey | sed s/\ chromeless-apikey-$(STAGE)\:\ //g))
	python pip_install.py prod
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
