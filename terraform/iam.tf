#This policy defines the EventBridge permissions on s3
resource "aws_iam_policy" "s3-event-policy" {

  name   = "s3-event-policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.aws-s3-buckets[0].arn}",
        "arn:aws:s3:::${aws_s3_bucket.aws-s3-buckets[0].arn}/*"
        
      ]
    }
  ]
}
EOF

}

#Configuring the role that our EventBridge will assume
resource "aws_iam_role" "event-bridge-role" {
  name = "event-bridge-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "events.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

#Attaching policies to the role
resource "aws_iam_role_policy_attachment" "s3-event-policy-role-attachment" {

  policy_arn = aws_iam_policy.s3-event-policy.arn
  role       = aws_iam_role.event-bridge-role.name

}

resource "aws_iam_role_policy_attachment" "sns-event-policy-role-attachment" {

  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess" ## This policy gives full access to SNS
  role       = aws_iam_role.event-bridge-role.name

}

#Creating a policy that allows SNS to publish the events it receives from EventBridge
resource "aws_sns_topic_policy" "sns-publish-event-policy" {

  arn = aws_sns_topic.sns-s3-topic.arn

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Id": "Allow-SNS-Publish-Event",
  "Statement": [
    {
      "Sid": "AllowPublish",
      "Effect": "Allow",
      "Principal": {
        "Service": "events.amazonaws.com"
      },
      "Action": "SNS:Publish",
      "Resource": "${aws_sns_topic.sns-s3-topic.arn}"
    }
  ]
}
EOF
}

#Creating a SQS policy that guarantees only messages sent from our 
#SNS topic will be published on the SQS queue
resource "aws_sqs_queue_policy" "sqs-receive-message-policy" {

  queue_url = aws_sqs_queue.sqs-lambda-queue.url

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Allow-SNS-SendMessage",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "sqs:SendMessage"
      ],
      "Resource": "${aws_sqs_queue.sqs-lambda-queue.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sns_topic.sns-s3-topic.arn}"
        }
      }
    }
  ]
}
EOF

}
