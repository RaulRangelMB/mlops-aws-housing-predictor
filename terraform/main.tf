data "aws_caller_identity" "current" {}

resource "aws_iam_role" "lambda_exec_role" {
  name = "housing_lambda_exec_role_tf"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "housing_api" {
  function_name = "predict-housing-price-tf"
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  
  image_uri     = "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-north-1.amazonaws.com/housing-predictor:latest"
  
  memory_size   = 512
  timeout       = 30

  depends_on = [aws_iam_role_policy_attachment.lambda_basic_execution]
}

resource "aws_lambda_function_url" "api_endpoint" {
  function_name      = aws_lambda_function.housing_api.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = ["*"]
    allow_methods = ["POST"]
  }
}

resource "aws_lambda_permission" "allow_public_url_invoke" {
  statement_id           = "FunctionURLAllowPublicAccess"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.housing_api.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}