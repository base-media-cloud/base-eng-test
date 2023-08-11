# Cloud Systems Engineering Tests

## Scope of Work
Deploy a simple python application to AWS that responds to HTTP POST requests and returns a JSON response.
All resources need to be provisioned using Terraform and state managed through Terraform Cloud.

High level objectives: 
- Configure a pipeline in Github actions and deploy the packaged python code. (CircleCi can be used if Github actions is not preferred)
- Authenticate with AWS (Applicants choice)
- Review and deploy the Terraform configuration to provision the required resources.
- Display proper Terraform state management through Terraform Cloud.
- Provide the API endpoint URL to the deployed application.

### Prerequisites
- Credentials to sandbox AWS account will be provided to you.
- Github (or other VCS provider supported by CircleCI) account
- CircleCI account (If Github is not preferred)
- Python3 (At least version 3.10)
- Pipenv
- AWS Boto3 (at least version 1.26.0)
- AWS CLI
- Terraform (At least version 1.5.0)
- Terraform Cloud Account (TFC provide a free tier)


### Deployment Success Criteria
Deployment is largely up to the applicant on how to execute this.
Below are the basic rquirements:
- The fundamental requirement is to successfully complete provisioning and deployment using Terraform. 
- Deployment should be achieved through a chosen pipeline, using best practices.
- Test and validate terraform configuration before applying.
- Correctly package and deploy the code to a Lambda function. The type of Lambda function is up to the applicant. (Zip archive, container, etc.)
- The function should be able to respond to HTTP POST requests and return a JSON response.

## References

### Github Actions
- Documentation: https://docs.github.com/en/actions

### CircleCI
- SignUp: https://circleci.com/signup/?return-to=https%3A%2F%2Fapp.circleci.com%2F
- Documentation: https://circleci.com/docs/getting-started/

### AWS
- Boto3
    - Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- AWS Lambda Powertools for Python
    - Documentation: https://awslabs.github.io/aws-lambda-powertools-python/2.9.0/

### Terraform
- Terraform Source
    - Documentation: https://developer.hashicorp.com/terraform/docs 
- Terraform Cloud
    - SignUp: https://app.terraform.io/public/signup/account?product_intent=terraform
    - Documentation: https://developer.hashicorp.com/terraform/cloud-docs

LICENSE
See [LICENSE](LICENSE.txt)
