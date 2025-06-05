resource "aws_s3_bucket" "model_artifacts" {
  count = var.create_bucket ? 1 : 0
  bucket = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "block_public_access" {
  bucket                  = var.create_bucket ? aws_s3_bucket.model_artifacts[0].id : var.bucket_name
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "allow_sagemaker_access" {
  bucket = var.create_bucket ? aws_s3_bucket.model_artifacts[0].id : var.bucket_name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          AWS = "arn:aws:iam::133521243113:root"
        },
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],        Resource = [
          "arn:aws:s3:::${var.bucket_name}",
          "arn:aws:s3:::${var.bucket_name}/*"
        ]
      }
    ]
  })
}