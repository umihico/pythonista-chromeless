FROM lambci/lambda:build-python3.6

ENV AWS_DEFAULT_REGION ap-northeast-1
ENV HOME /var/task

COPY . /var/task/

CMD pip --quiet install -r requirements.txt -t $HOME && \
    zip -rq9 deploy_package.zip ./
