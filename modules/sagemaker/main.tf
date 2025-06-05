resource "aws_iam_role" "sagemaker_exec" {
  name = "sagemaker-execution-role-2"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = ["sagemaker.amazonaws.com"]
        },
        Action = ["sts:AssumeRole"]
      }
    ]
  })
}

# Attach full SageMaker access
resource "aws_iam_role_policy_attachment" "sagemaker_access" {
  role       = aws_iam_role.sagemaker_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

# Attach S3 and CloudWatch access
resource "aws_iam_policy" "sagemaker_s3_cloudwatch_access" {
  name = "sagemaker-s3-cloudwatch-access"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::ml-artifacts-bucket-1",
          "arn:aws:s3:::ml-artifacts-bucket-1/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "cloudwatch:PutMetricData",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_s3_cloudwatch_access" {
  role       = aws_iam_role.sagemaker_exec.name
  policy_arn = aws_iam_policy.sagemaker_s3_cloudwatch_access.arn
}

# SageMaker Model using container + model data
resource "aws_sagemaker_model" "llm_model" {
  name               = "llm-model"
  execution_role_arn = aws_iam_role.sagemaker_exec.arn

  primary_container {
    image          = var.model_image
    model_data_url = var.model_data_url
    environment = {
      SAGEMAKER_PROGRAM          = "serve.py"
      SAGEMAKER_SUBMIT_DIRECTORY = "${var.model_data_url}/code"
    }
  }
}

# Endpoint Configuration
resource "aws_sagemaker_endpoint_configuration" "llm_config" {
  name = "llm-endpoint-config"

  production_variants {
    variant_name           = "AllTraffic"
    model_name             = aws_sagemaker_model.llm_model.name
    initial_instance_count = 1
    instance_type          = "ml.g4dn.xlarge"  # Upgraded for LLMs
  }
}

# SageMaker Endpoint
resource "aws_sagemaker_endpoint" "llm_endpoint" {
  name                 = var.endpoint_name
  endpoint_config_name = aws_sagemaker_endpoint_configuration.llm_config.name
}
