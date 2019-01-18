rm -rf deploy_package.zip
sudo docker run -v "${PWD}":/var/task chromeless && aws lambda update-function-code  --publish --profile lambda_deployer --function-name chromeless --zip-file fileb://deploy_package.zip
