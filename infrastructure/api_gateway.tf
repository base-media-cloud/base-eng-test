resource "aws_apigatewayv2_api" "event_handler" {
  name          = "event-handler-${var.environment}"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "event_handler" {
  api_id             = aws_apigatewayv2_api.event_handler.id
  integration_type   = "AWS_PROXY"
  connection_type    = "INTERNET"
  integration_method = "POST"
  integration_uri    = aws_lambda_function.event_handler.invoke_arn
}

resource "aws_apigatewayv2_route" "event_handler" {
  api_id    = aws_apigatewayv2_api.event_handler.id
  route_key = "POST /event-handler"
  target    = "integrations/${aws_apigatewayv2_integration.event_handler.id}"
}

resource "aws_apigatewayv2_stage" "event_handler" {
  api_id      = aws_apigatewayv2_api.event_handler.id
  name        = var.environment
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode(
      {
        httpMethod     = "$context.httpMethod"
        ip             = "$context.identity.sourceIp"
        protocol       = "$context.protocol"
        requestId      = "$context.requestId"
        requestTime    = "$context.requestTime"
        responseLength = "$context.responseLength"
        routeKey       = "$context.routeKey"
        status         = "$context.status"
      }
    )
  }
}

resource "aws_lambda_permission" "event_handler" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.event_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.event_handler.execution_arn}/${var.environment}/POST/event-handler"
}

resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/api-gateway/event_handler-${var.environment}"
  retention_in_days = 60
}