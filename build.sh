#!/bin/bash
set -eo pipefail

circleci local execute --job pytest-local

cat <<EOF > .env
-e AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
-e AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
-e AWS_REGION=$(aws configure get region)
-e AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
-e AWS_DEFAULT_REGION=$(aws configure get region)
-e PYPI_USERNAME_DEV=$(aws ssm get-parameter --name PYPI_USERNAME_TEST --query 'Parameter.Value' --output text)
-e PYPI_PASSWORD_DEV=$(aws ssm get-parameter --name PYPI_PASSWORD_TEST --query 'Parameter.Value' --output text)
-e PYPI_USERNAME_PROD=$(aws ssm get-parameter --name PYPI_USERNAME_PROD --query 'Parameter.Value' --output text)
-e PYPI_PASSWORD_PROD=$(aws ssm get-parameter --name PYPI_PASSWORD_PROD --query 'Parameter.Value' --output text)
EOF

circleci local execute --job sls-dev $(cat .env)
circleci local execute --job pypi-dev $(cat .env)

STAGE=dev
cat <<EOF >> .env
-e API_URL_DEV=$(aws cloudformation describe-stacks --stack-name chromeless-$STAGE --query "Stacks[0].Outputs[?OutputKey=='ServiceEndpoint'].OutputValue" --output text)
-e API_KEY_DEV=$(aws apigateway get-api-keys --query 'items[?name==`chromeless-apikey-'$STAGE'`].value' --include-values --output text)
EOF

circleci local execute --job pytest-dev $(cat .env)
circleci local execute --job sls-prod $(cat .env)
circleci local execute --job pypi-prod $(cat .env)

STAGE=prod
cat <<EOF >> .env
-e API_URL_PROD=$(aws cloudformation describe-stacks --stack-name chromeless-$STAGE --query "Stacks[0].Outputs[?OutputKey=='ServiceEndpoint'].OutputValue" --output text)
-e API_KEY_PROD=$(aws apigateway get-api-keys --query 'items[?name==`chromeless-apikey-'$STAGE'`].value' --include-values --output text)
EOF

circleci local execute --job pytest-prod $(cat .env)