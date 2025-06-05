variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "create_bucket" {
  description = "Set to false if bucket already exists, true to create new bucket"
  type        = bool
  default     = true
}

variable "model_file_path" {
  description = "Local path to the model.tar.gz file to upload"
  type        = string
  default     = null
}
