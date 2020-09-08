deploy:
	docker build -t umihico/chromelessenv .
	docker run \
		-e AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key) \
		-e AWS_DEFAULT_REGION=$(shell aws configure get region) \
		umihico/chromelessenv make deploy_
	docker push umihico/chromelessenv:latest # docker.io/umihico/chromelessenv

deploy_:
	# test locally
	pytest tests.py

	# deploy sls
	sls deploy
	$(eval API_URL := $(shell sls info -v | grep ServiceEndpoint | sed s/ServiceEndpoint\:\ //g))
	$(eval STAGE := $(shell sls info -v | grep stage | sed s/stage\:\ //g))
	$(eval API_KEY := $(shell sls info -v | grep chromeless-apikey | sed s/\ chromeless-apikey-$(STAGE)\:\ //g))
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py

	# upload as staging pypi package
	mkdir -p /app/test
	cp /app/example.py /app/test/
	cd /app/test/
	python setup.py bdist_wheel
	twine upload --repository testpypi dist/* \
	-u $(shell aws ssm get-parameter --name PYPI_USERNAME_TEST --query 'Parameter.Value' --output text) \
	-p $(shell aws ssm get-parameter --name PYPI_PASSWORD_TEST --query 'Parameter.Value' --output text)
	sleep 60 # wait test.pypi.org update repository
	pip install --index-url https://test.pypi.org/simple/ chromeless
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py

	# upload as production pypi package
	STAGE=prod python setup.py bdist_wheel
	twine upload dist/* \
	-u $(shell aws ssm get-parameter --name PYPI_USERNAME_PROD --query 'Parameter.Value' --output text) \
	-p $(shell aws ssm get-parameter --name PYPI_PASSWORD_PROD --query 'Parameter.Value' --output text)
	sleep 60 # wait pypi.org update repository
	pip install --upgrade --force-reinstall chromeless
	API_URL=$(API_URL) API_KEY=$(API_KEY) pytest example.py
