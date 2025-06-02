variable "sagemaker_endpoint_name" {
  description = "Name of the SageMaker endpoint to invoke"
  type        = string
}

variable "lambda_zip_path" {
  description = "Local path to the zipped Lambda deployment package"
  type        = string
}
