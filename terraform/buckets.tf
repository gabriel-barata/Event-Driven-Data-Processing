resource "aws_s3_bucket" "aws-s3-buckets" {

  count         = length(var.bucket-names)
  bucket        = "${var.project-name}-${var.bucket-names[count.index]}-${var.account-id}"
  force_destroy = true

  tags = {

    Environment = "dev"

  }

}