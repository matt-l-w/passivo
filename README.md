<!--
title: 'Passivo: log your project time in Slack'
description: 'This serverless slack app allows you to log time on projects without going through the pain of agresso.'
layout: Doc
framework: v1
platform: AWS
language: Python
authorLink: 'https://github.com/matt-l-w'
authorName: 'Matthew Williams'
-->
# Passivo

This serverless app is designed to be used a slack app, allowing a simple log of time for each user on their various projects.

## Structure

This service has a separate directory for all the log operations. For each operation exactly one file exists e.g. `logs/create.py`.

The service uses the secret key assigned to your slack app in order to authenticate requests.  This can be found my going to the
(API section of slack)[api.slack.com/apps/], selecting your app and clicking on the 'Basic Information' section.
The secret key will need to be provided at deployment time using the env var `SLACK_SIGNING_SECRET`.

## Setup

```bash
npm install -g serverless
```

## Test

There are currently only unit tests.  These can be found within each directory.  Run the whole suite with

```bash
python3 -m unittest
```

## Deploy

In order to deploy the endpoint, ensure the following environment variables are set up:
- SLACK_SIGNING_KEY

Then simply run

```bash
serverless deploy
```

The expected result should be similar to:

```bash
Serverless: Packaging service…
Serverless: Uploading CloudFormation file to S3…
Serverless: Uploading service .zip file to S3…
Serverless: Updating Stack…
Serverless: Checking Stack update progress…
Serverless: Stack update finished…

Service Information
service: passivo
stage: dev
region: eu-west-2
api keys:
  None
endpoints:
  POST - https://45wf34z5yf.execute-api.eu-west-2.amazonaws.com/dev/logs
  GET - https://45wf34z5yf.execute-api.eu-west-2.amazonaws.com/dev/logs
functions:
  passivo-dev-list: arn:aws:lambda:eu-west-2:488110005556:function:serverless-rest-api-with-dynamodb-dev-list
  passivo-dev-create: arn:aws:lambda:eu-west-2:488110005556:function:serverless-rest-api-with-dynamodb-dev-create
```

### Production

To change the stage for deployment, simply pass the `--stage production` flag to `serverless deploy`.

Other flags can be passed.  See [this article](https://serverless.com/framework/docs/providers/aws/guide/deploying/).

## Scaling

### AWS Lambda

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).

### DynamoDB

When you create a table, you specify how much provisioned throughput capacity you want to reserve for reads and writes. DynamoDB will reserve the necessary resources to meet your throughput needs while ensuring consistent, low-latency performance. You can change the provisioned throughput and increasing or decreasing capacity as needed.

This is can be done via settings in the `serverless.yml`.

```yaml
  ProvisionedThroughput:
    ReadCapacityUnits: 1
    WriteCapacityUnits: 1
```
