resource "aws_lambda_function" "event_handler" {
  function_name = "${var.function_name}_${var.environment}"
  role          = aws_iam_role.event_handler_execution_role.arn
  handler       = var.function_handler
  package_type  = var.package_type
  filename      = var.filename
  runtime       = var.runtime
  publish       = var.publish
  architectures = var.architectures

  timeout = var.timeout

  environment {
    variables = {
      POWERTOOLS_SERVICE_NAME = var.powertools_service_name
      LOG_LEVEL               = var.log_level
    }
  }
}

resource "aws_cloudwatch_log_group" "event_handler" {
  name              = "/aws/lambda/${var.function_name}_${var.environment}"
  retention_in_days = 60
}
