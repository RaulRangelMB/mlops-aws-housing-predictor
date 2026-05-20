output "live_api_url" {
  description = "Endpoint for a housing prediction model"
  value       = aws_lambda_function_url.api_endpoint.function_url
}