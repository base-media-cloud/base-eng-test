data "aws_iam_policy_document" "event_handler" {
  statement {
    sid = "EventHandlerPolicy"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "${aws_cloudwatch_log_group.event_handler.arn}*",
    ]
  }
}

resource "aws_iam_role" "event_handler_execution_role" {
  name = "event_handler_execution_role_${var.environment}"
  path = "/service-role/"
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "lambda.amazonaws.com"
          }
        },
      ]
      Version = "2012-10-17"
    }
  )

  max_session_duration = 3600
}

resource "aws_iam_role_policy" "event_handler" {
  name   = "${var.function_name}_${var.environment}"
  role   = aws_iam_role.event_handler_execution_role.id
  policy = data.aws_iam_policy_document.event_handler.json
}