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

  name        = "${var.project-name}-s3-event-rule"
  description = "this rule creates an event everytime that a new file is droped on the referenced s3 bucket"

  event_pattern = <<EOF
{
  "source": ["aws.s3"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["s3.amazonaws.com"],
    "eventName": ["PutObject"],
    "requestParameters": {
      "bucketName": ["${aws_s3_bucket.aws-s3-buckets[0].id}"]
    }
  }
}
EOF

  role_arn = aws_iam_role.event-bridge-role.arn
}

#Creating the SNS topic
resource "aws_sns_topic" "sns-s3-topic" {

  name = "${var.project-name}-sns-s3-topic"

}

#Creating the event target that will be our SNS topic
resource "aws_cloudwatch_event_target" "sns-event-target" {

  rule      = aws_cloudwatch_event_rule.s3-event-rule.name
  target_id = "${var.project-name}-s3-event-target"
  arn       = aws_sns_topic.sns-s3-topic.arn

}

#Creating the SQS queue
resource "aws_sqs_queue" "sqs-lambda-queue" {

    name = "${var.project-name}-sqs-lambda-queue"
    message_retention_seconds = 43200
    delay_seconds = 0 # the time in seconds that the delivery of all messages in the queue will be delayed
    fifo_queue = false # for this project we're using a standard queue

    tags = {
      
      Environment = "Dev"

    }

}

#Providing a resource for subscribing SQS queue to the SNS topic
resource "aws_sns_topic_subscription" "sqs-subscription-sns" {

    topic_arn = aws_sns_topic.sns-s3-topic.arn
    protocol = "sqs"
    endpoint = aws_sqs_queue.sqs-lambda-queue.arn
  
}