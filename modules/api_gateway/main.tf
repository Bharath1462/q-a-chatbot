resource "aws_apigatewayv2_api" "llm_api" {
  name          = "llm-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.llm_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = var.lambda_function_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.llm_api.id
  route_key = "POST /invoke"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.llm_api.id
  name        = "$default"
  auto_deploy = true
}
