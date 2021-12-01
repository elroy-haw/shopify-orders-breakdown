locals {
  lambda_package_name = "lambda_package.zip"
}

resource "null_resource" "zip_files" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = join(" && ", [
      "rm -f ${local.lambda_package_name}",
      "cd ../venv/lib/python3.9/site-packages",
      "zip -r9q $${OLDPWD}/${local.lambda_package_name} .",
      "cd $${OLDPWD}",
      "cd ..",
      "zip -rgq $OLDPWD/lambda_package.zip . -x '*pycache*' -x 'infra*' -x 'venv*' -x '.*' -x '*.md' -x '*.txt'"
    ])
  }
}

resource "aws_lambda_function" "orders_processor_lambda" {
  function_name    = "orders-processor"
  handler          = "main.lambda_handler"
  role             = aws_iam_role.orders_processor_lambda_role.arn
  runtime          = "python3.9"
  filename         = local.lambda_package_name
  source_code_hash = filebase64sha256(local.lambda_package_name)
  timeout          = 60

  environment {
    variables = {
      CONFIG_FILENAME = "config/local.json"
    }
  }

  depends_on = [null_resource.zip_files]
}

resource "aws_iam_role" "orders_processor_lambda_role" {
  name               = "orders-processor-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "orders_processor_lambda_policy" {
  role   = aws_iam_role.orders_processor_lambda_role.id
  policy = data.aws_iam_policy_document.orders_processor_lambda_policy.json
}

data "aws_iam_policy_document" "orders_processor_lambda_policy" {
  statement {
    effect  = "Allow"
    actions = ["ses:SendRawEmail"]
    resources = [
      aws_ses_email_identity.sender.arn,
      aws_ses_email_identity.receiver.arn
    ]
  }
}

resource "aws_iam_role_policy_attachment" "basic_exec_attach" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.orders_processor_lambda_role.name
}

resource "aws_lambda_permission" "allow_cwe" {
  function_name = aws_lambda_function.orders_processor_lambda.function_name
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.orders_processor_cwe_rule.arn
}