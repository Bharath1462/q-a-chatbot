variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-west-2"
}

variable "execution_role_arn" {
  description = "IAM execution role ARN for SageMaker"
  type        = string
}

variable "model_image" {
  description = "Docker image URI for the SageMaker model"
  type        = string
}

variable "model_data_url" {
  description = "S3 URI to the trained model artifacts"
  type        = string
}

variable "endpoint_name" {
  description = "Name of the SageMaker endpoint to be created"
  type        = string
}

variable "bucket_name" {
  description = "The name of the S3 bucket to create"
  type        = string
}
