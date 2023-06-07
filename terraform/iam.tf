#This policy defines the EventBridge rule permissions on s3
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
        "arn:aws:s3:::${aws_s3_bucket.aws-s3-buckets[0].arn}"/*"
        
      ]
    }
  ]
}
EOF

}

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

resource "aws_iam_role_policy_attachment" "s3-event-policy-role-attachment" {

    policy_arn = aws_iam_policy.s3-event-policy.arn
    role = aws_iam_role.event-bridge-role.name
  
}