# Getting Started with AWS Account

## Installation

1. Install AWS CLI by executing the following at command line:

    `pip install awscli`
    
2. Copy your `credential` file into `~/.aws`

## Verify Installation

1. Issue the command `aws s3 ls`. The output should resemble the following:

    `2020-04-05 13:37:36 infectionsim-pipeline-data`

You are now ready to run the model using the `--send-to-cloud` feature. See the [pipeline README](README_PIPELINE.md) for further instructions.
