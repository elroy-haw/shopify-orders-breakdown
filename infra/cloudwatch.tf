resource "aws_cloudwatch_event_rule" "orders_processor_cwe_rule" {
  name                = "orders-processor-rule"
  schedule_expression = var.schedule
  role_arn            = aws_iam_role.orders_processor_cwe_role.arn
}

resource "aws_cloudwatch_event_target" "orders_processor_cwe_target" {
  rule = aws_cloudwatch_event_rule.orders_processor_cwe_rule.name
  arn  = aws_lambda_function.orders_processor_lambda.arn
}

resource "aws_iam_role" "orders_processor_cwe_role" {
  name               = "orders-processor-cwe-role"
  assume_role_policy = data.aws_iam_policy_document.cwe_assume_role_policy.json
}

data "aws_iam_policy_document" "cwe_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "orders_processor_cwe_policy" {
  role   = aws_iam_role.orders_processor_cwe_role.name
  policy = data.aws_iam_policy_document.orders_processor_cwe_policy.json
}

data "aws_iam_policy_document" "orders_processor_cwe_policy" {
  statement {
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [aws_lambda_function.orders_processor_lambda.arn]
  }
}
