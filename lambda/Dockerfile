FROM lambci/lambda:build-python3.6

ENV AWS_DEFAULT_REGION ap-northeast-1
ENV APP_DIR /var/task

ADD . .

CMD pip --quiet install -r requirements.txt -t $APP_DIR && \
  zip -q9 deploy_package.zip lambda_function.py && \
  zip -rq9 deploy_package.zip *
