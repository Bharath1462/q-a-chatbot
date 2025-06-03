region             = "us-east-1"
execution_role_arn = "arn:aws:iam::133521243113:role/sagemaker-execution-role"
model_image        ="133521243113.dkr.ecr.us-east-1.amazonaws.com/qa-repo:latest"
model_data_url     = "s3://mode-artifacts-bucket-1/model.tar.gz"
endpoint_name      = "llm-inference-endpoint"
bucket_name        = "mode-artifacts-bucket-1"

