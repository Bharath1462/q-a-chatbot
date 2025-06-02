variable "execution_role_arn" {
  description = "IAM role ARN that SageMaker uses to run the model"
  type        = string
}

variable "model_image" {
  description = "Docker image URI for the model"
  type        = string
}

variable "model_data_url" {
  description = "S3 location of the trained model tarball"
  type        = string
}

variable "endpoint_name" {
  description = "Name of the SageMaker endpoint"
  type        = string
}
