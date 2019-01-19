rm -rf deploy_package.zip
git_branch_name=$(git symbolic-ref --short HEAD)
sudo docker run -v "${PWD}":/var/task chromeless && aws lambda update-function-code  --publish --profile lambda_deployer --function-name chromeless-${git_branch_name} --zip-file fileb://deploy_package.zip
