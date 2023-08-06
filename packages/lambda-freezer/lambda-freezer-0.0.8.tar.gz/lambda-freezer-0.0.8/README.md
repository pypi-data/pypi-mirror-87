# lambda_freezer

Goals:
 - Make it easy to deploy one or many services under the same Amazon API Gateway.
 - Make it easy to deploy a stage in an immutable way.

### Deploy a specific stage
The main aim of this module is to help your Amazon API Gateway work in such a way that each stage is immutable.
This is achieved by using the versioning and aliasing features of Lambda function, as well as stage variables.
The gist is this:
 - When deploying a stage, each underlying Lambda function is frozen to a specific version.
 - When calling the resouces for that particular stage, the "frozen" versioning of Lambda functions will be called (indirectly via an alias).

For more information of how that is achieved "manually" in more details:
https://aws.amazon.com/blogs/compute/using-api-gateway-stage-variables-to-manage-lambda-functions/
```sh
Python 3.6.9 (default, Nov  7 2019, 10:44:02)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import lambda_freezer
>>> REST_API_ID = "r5ltm5nqr6"
>>> REGION = "us-east-1"
>>> APILIB_DEFAULT_ALIAS_NAME = "uat"
>>> DOMAIN_NAME = "api-library.puno.io" # this guy is optional
>>> deploy(REST_API_ID, REGION, "0.0.1", "some description", APILIB_DEFAULT_ALIAS_NAME, DOMAIN_NAME)
```

### Flow (super opinionated)
- use serverless framework and configure like something below.
```yml
 - provider:
      name: aws
      runtime: python3.6
      stage: latest # IMPORTANT - this need to match -> APILIB_DEFAULT_ALIAS_NAME
      versionFunctions: false # versioning would be done only upon deploying/"freezing" to a stage
      apiGateway: # make sure you point to a common api gateway
        restApiId:
          'Fn::ImportValue': 'OUTPUT-ApiGatewayRestApiId-REPLACE-WITH-OWN'
        restApiRootResourceId:
          'Fn::ImportValue': 'OUTPUT-ApiGatewayRestApiRootResourceId-REPLACE-WITH-OWN'
```
- To push your functions and make sure the api gateway integration gets changed. *(We want that every function integrations' are such that the api gateway can only call a specific version of any lambda functions via an alias, using a stage variable).*
```sh
serverless deploy
```
```sh
Python 3.6.9 (default, Nov  7 2019, 10:44:02)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import lambda_freezer
>>> REST_API_ID = "r5ltm5nqr6"
>>> REGION = "us-east-1"
>>> APILIB_DEFAULT_ALIAS_NAME = "uat"
>>> DOMAIN_NAME = "api-library.puno.io" # this guy is optional
>>> run_after_default_deployment(REST_API_ID, REGION, APILIB_DEFAULT_ALIAS_NAME, DOMAIN_NAME)
```
- When you like a specific version of your functions, just "freeze" them using the deploy cmd described above.
