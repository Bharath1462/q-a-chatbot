region             = "eu-west-2"
execution_role_arn = "arn:aws:iam::133521243113:role/sagemaker-execution-role-2"
model_image        ="133521243113.dkr.ecr.eu-west-2.amazonaws.com/ml-repo:latest"
model_data_url     = "s3://ml-artifacts-bucket-1/model.tar.gz"
endpoint_name      = "llm-inference-endpoint"
bucket_name        = "ml-artifacts-bucket-1"

