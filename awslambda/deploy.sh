rm -rf deploy_package.zip
git_branch_name=$(git symbolic-ref --short HEAD)
sudo docker run -v "${PWD}":/var/task chromeless
aws s3 cp deploy_package.zip s3://s3.umihi.co/deploy_package.zip
aws lambda update-function-code  --publish --profile lambda_deployer --function-name chromeless-${git_branch_name} --s3-bucket s3.umihi.co --s3-key deploy_package.zip
# aws lambda update-function-code  --publish --profile lambda_deployer --function-name chromeless-${git_branch_name} --zip-file fileb://deploy_package.zip
