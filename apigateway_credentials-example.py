from subprocess import check_output
current_branch_name = check_output(
    "git symbolic-ref --short HEAD".split(" ")).decode().split('\n')[0]

awsgateway_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
awsgateway_url = "https://XXXXXXXXXX.execute-api.us-west-2.amazonaws.com/default/chromeless-" + current_branch_name
