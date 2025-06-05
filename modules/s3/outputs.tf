output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = var.bucket_name
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = var.create_bucket ? aws_s3_bucket.model_artifacts[0].arn : "arn:aws:s3:::${var.bucket_name}"
}