build:
	docker build -t umihico/chromelessenv .
	docker build -t umihico/chromelesstest -f Dockerfile_test .

deploy:
	python define_version.py
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
		umihico/chromelessenv make deploy_pypi_stg
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelesstest make test_stg
	STAGE=prod python define_version.py
	@make build
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelessenv make deploy_pypi_prod
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelesstest make test_prod
	docker push umihico/chromelessenv:latest # docker.io/umihico/chromelessenv

sls:
	# test locally
	pytest tests.py

	# deploy sls
	sls deploy
	$(eval API_URL := $(shell sls info -v | grep ServiceEndpoint | sed s/ServiceEndpoint\:\ //g))
	$(eval STAGE := $(shell sls info -v | grep stage | sed s/stage\:\ //g))
	$(eval API_KEY := $(shell sls info -v | grep chromeless-apikey | sed s/\ chromeless-apikey-$(STAGE)\:\ //g))
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py

deploy_pypi_stg:
	python setup.py bdist_wheel
	twine upload --repository testpypi dist/* \
	-u $(shell aws ssm get-parameter --name PYPI_USERNAME_TEST --query 'Parameter.Value' --output text) \
	-p $(shell aws ssm get-parameter --name PYPI_PASSWORD_TEST --query 'Parameter.Value' --output text)

deploy_pypi_prod:
	STAGE=prod python setup.py bdist_wheel
	twine upload dist/* \
	-u $(shell aws ssm get-parameter --name PYPI_USERNAME_PROD --query 'Parameter.Value' --output text) \
	-p $(shell aws ssm get-parameter --name PYPI_PASSWORD_PROD --query 'Parameter.Value' --output text)

test_compatibility:
	$(eval API_URL := $(shell sls info -v | grep ServiceEndpoint | sed s/ServiceEndpoint\:\ //g))
	$(eval STAGE := $(shell sls info -v | grep stage | sed s/stage\:\ //g))
	$(eval API_KEY := $(shell sls info -v | grep chromeless-apikey | sed s/\ chromeless-apikey-$(STAGE)\:\ //g))
	pip install 'chromeless==0.2.9'
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py
	pip install 'chromeless==0.3.0'
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
