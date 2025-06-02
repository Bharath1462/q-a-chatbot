output "lambda_function_name" {
  value = aws_lambda_function.invoke_llm.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.invoke_llm.arn
}
