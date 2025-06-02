provider "aws" {
  region = var.region
}

module "api_gateway" {
  source = "./modules/api_gateway"
  lambda_function_arn = module.lambda.lambda_function_arn
}

module "lambda" {
  source = "./modules/lambda"

  sagemaker_endpoint_name = module.sagemaker.endpoint_name
  lambda_zip_path         = "C:/Users/BHUMIREDDY RAJAREDDY/terraform/llm-sagemaker-deploy/lambda_function/lambda_function.zip"
}


module "sagemaker" {
  source = "./modules/sagemaker"

  execution_role_arn = var.execution_role_arn
  model_image        = var.model_image
  model_data_url     = var.model_data_url
  endpoint_name      = var.endpoint_name
}

module "s3" {
  source      = "./modules/s3"
  bucket_name = var.bucket_name
}





