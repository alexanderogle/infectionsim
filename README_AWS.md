# Getting Started with AWS Account

## Installation

1. Install AWS CLI by executing the following at command line:

    `pip install awscli`
    
2. Copy your `credentials` file into `~/.aws`

## Verify Installation

1. Issue the command `aws s3 ls`. The output should resemble the following:

    `2020-04-05 13:37:36 infectionsim-pipeline-data`

You are now ready to run the model using the `--send-to-cloud` feature. See the [pipeline README](README_PIPELINE.md) for further instructions.

## Access AWS Console

1. Go to Infection Sim's [AWS console](https://infection-sim.signin.aws.amazon.com/console).
2. Log in with your username and password in your `aws_credentials.csv` file.
