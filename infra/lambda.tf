locals {
  lambda_package_name = "lambda_package.zip"
  file_hashes = merge(
    { for fname in fileset("../src", "**/*.py") : fname => filebase64sha256(format("../src/%s", fname)) },
    {
      (var.config_filepath) = filebase64sha256(format("../%s", var.config_filepath))
      "requirements.txt"    = filebase64sha256("../requirements.txt")
    }
  )
}

data "archive_file" "lambda_package" {
  type        = "zip"
  source_dir  = "tmp"
  output_path = local.lambda_package_name

  depends_on = [null_resource.prepare_files]
}

resource "null_resource" "prepare_files" {
  triggers = local.file_hashes

  provisioner "local-exec" {
    command = "./scripts/prepare_files.sh ${dirname(var.config_filepath)}"
  }
}

resource "aws_lambda_function" "orders_processor_lambda" {
  function_name    = "orders-processor"
  handler          = "main.lambda_handler"
  role             = aws_iam_role.orders_processor_lambda_role.arn
  runtime          = "python3.9"
  filename         = local.lambda_package_name
  source_code_hash = data.archive_file.lambda_package.output_base64sha256
  timeout          = 300

  environment {
    variables = {
      CONFIG_FILENAME = var.config_filepath
    }
  }
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