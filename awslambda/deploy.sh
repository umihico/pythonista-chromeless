sudo docker run -v "${PWD}":/var/task serverless_plain_lambda && aws lambda update-function-code  --publish --profile lambda_deployer --function-name serverless-plain-selenium --zip-file fileb://deploy_package.zip
rm -rf deploy_package.zip
