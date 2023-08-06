resource "aws_lambda_function" "event_handler" {
  function_name = ""
  handler       = "main.lambda_handler"
  package_type  = "Zip"
  runtime       = "python3.10"
  publish       = true
  architectures = [
    "x86_64"
  ]

  timeout = 60

  environment {
    variables = {
      QUEUE_URL = ""
      LOG_LEVEL = "INFO"
    }
  }

}

resource "aws_lambda_function" "object_mover" {
  function_name = ""
  handler       = "main.lambda_handler"
  package_type  = "Zip"
  runtime       = "python3.10"
  publish       = true
  architectures = [
    "x86_64"
  ]

  timeout = 60

  environment {
    variables = {
      SQS_QUEUE = ""
      LOG_LEVEL = "INFO"
      POWERTOOLS_SERVICE_NAME = "object_mover"
      ROLE_ARN  = ""
    }
  }

}