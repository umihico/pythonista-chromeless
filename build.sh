#!/bin/bash
set -euxo pipefail

PKG_NAME=chromeless
DIR_NAME=$PKG_NAME
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
AWS_REGION=$(aws configure get region)

echo "TEST LOCALLY"
DOCKER_BUILDKIT=1 docker build -t chromeless .
docker-compose -f sls/docker-compose.yml up --exit-code-from pytest --abort-on-container-exit

echo "DEPLOY STAGING LAMBDA"
sls deploy --stage stg --region $AWS_REGION

echo "DEPLOY STAGING PYPI"
docker build . -t pypienv_chromeless -f pypi/Dockerfile
touch chromeless/__version__.py
PYPI_USERNAME_TEST=$(aws ssm get-parameter --name PYPI_USERNAME_TEST --query 'Parameter.Value' --output text)
PYPI_PASSWORD_TEST=$(aws ssm get-parameter --name PYPI_PASSWORD_TEST --query 'Parameter.Value' --output text)
docker run --rm \
	--mount type=bind,source=$(pwd)/chromeless/__version__.py,target=/app/chromeless/__version__.py \
	-e PKG_NAME=$PKG_NAME \
  -e DIR_NAME=$DIR_NAME \
  -e PYPI_USERNAME=$PYPI_USERNAME_TEST \
  -e PYPI_PASSWORD=$PYPI_PASSWORD_TEST \
  -e REPOSITORY=testpypi \
  -e STAGE=stg \
	pypienv_chromeless

echo "TEST STAGING"
STAGE=stg
STACK_NAME=chromeless-$STAGE
API_URL=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ServiceEndpoint'].OutputValue" --output text)
API_KEY=$(aws apigateway get-api-keys --query 'items[?name==`chromeless-apikey-'$STAGE'`].value' --include-values --output text)
CHROMELESS_SERVER_FUNCTION_NAME=chromeless-server-stg \
  AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  AWS_REGION=$AWS_REGION \
  API_URL=$API_URL \
  API_KEY=$API_KEY \
  docker-compose -f pytest/docker-compose.yml up

echo "DEPLOY PRODUCTION LAMBDA"
sls deploy --region $AWS_REGION

echo "DEPLOY PRODUCTION PYPI"
docker build . -t pypienv_chromeless -f pypi/Dockerfile
touch chromeless/__version__.py
PYPI_USERNAME_PROD=$(aws ssm get-parameter --name PYPI_USERNAME_PROD --query 'Parameter.Value' --output text)
PYPI_PASSWORD_PROD=$(aws ssm get-parameter --name PYPI_PASSWORD_PROD --query 'Parameter.Value' --output text)
docker run --rm \
	--mount type=bind,source=$(pwd)/chromeless/__version__.py,target=/app/chromeless/__version__.py \
	-e PKG_NAME=$PKG_NAME \
  -e DIR_NAME=$DIR_NAME \
  -e PYPI_USERNAME=$PYPI_USERNAME_PROD \
  -e PYPI_PASSWORD=$PYPI_PASSWORD_PROD \
  -e REPOSITORY=pypi \
  -e STAGE=prod \
	pypienv_chromeless

echo "TEST PRODUCTION"
STAGE=prod
STACK_NAME=chromeless-$STAGE
API_URL=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='ServiceEndpoint'].OutputValue" --output text)
API_KEY=$(aws apigateway get-api-keys --query 'items[?name==`chromeless-apikey-'$STAGE'`].value' --include-values --output text)
CHROMELESS_SERVER_FUNCTION_NAME=chromeless-server-prod \
  AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  AWS_REGION=$AWS_REGION \
  API_URL=$API_URL \
  API_KEY=$API_KEY \
  docker-compose -f pytest/docker-compose.yml up
