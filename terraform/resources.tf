#Creating the resource for AWS s3 buckets
resource "aws_s3_bucket" "aws-s3-buckets" {

  count         = length(var.bucket-names)
  bucket        = "${var.project-name}-${var.bucket-names[count.index]}-${var.account-id}"
  force_destroy = true

  tags = {

    Environment = "dev"

  }

}

#Creating the EventBridge rule that is triggered everytime a new file is droped on the bronze bucket
resource "aws_cloudwatch_event_rule" "s3-event-rule" {

    name = "s3-event-rule"
    description = "this rule creates an event everytime that a new file is droped on the referenced s3 bucket"

    event_pattern = <<EOF
{
  "source": ["aws.s3"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["s3.amazonaws.com"],
    "eventName": ["PutObject"],
    "requestParameters": {
      "bucketName": ["${aws_s3_bucket.aws-s3-buckets[0].name}"]
    }
  }
}
EOF

    role_arn = aws_iam_role.event-bridge-role.arn
}

#Creating the SNS topic
resource "aws_sns_topic" "sns-s3-topic" {

    name = "sns-s3-topic"
  
}

#Creating the event target that will be our SNS topic
resource "aws_cloudwatch_event_target" "sns-event-target" {

    rule = aws_cloudwatch_event_rule.s3-event-rule.name
    target_id = "s3-event-target"
    arn = aws_sns_topic.sns-s3-topic.arn
  
}