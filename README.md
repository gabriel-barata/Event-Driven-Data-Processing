# Event Driven Data Processing
An entirely serverless event driven data pipeline built on AWS cloud for high scalability and flexibility

## Solution Architecture
<p align="left">
  <img src="https://raw.githubusercontent.com/gabriel-barata/images/master/event-driven-data-pipeline/diagram.drawio.png" alt="Texto Alternativo" width="720">
</p>
### Components
+ **Amazon S3 (Simple Storage Service)**: Amazon S3 its a object storage service high scalable and durable. Our architecture uses s3 as a data repository.
+ **Amazon EventBridge**: EventBridge is a serverless service that uses events to connect application components together. Our architecture uses EventBridge to capture an specific event and send it to a target.
+ **Amazon SNS (Simple Notification Service)**: Amazon SNS is a managed service that provides message delivery from publishers to subscribers. In our architecture Amazon SNS is configured to receive events from EventBridge and them foward it to its subscribers. It is an important point in our project, as it brings great flexibility to the pipeline. Add further workloads to this initial project becomes a way easier, since any new pipeline can be docked to the SNS topic.
+ **Amazon SQS (Simple Queue Service)**: Amazon SQS is a serverless queue service. In our architecture it's configured as a SNS subscriber, everytime a new message is received SQS puts it on a queue. Amazon SQS brings scalability to our project and guarantees that every message received will be processed by the Lambda Function.
+ **Amazon Lambda**: AWS Lambda is a serverless compute service. In our architecture a lambda function was configured to consume the SQS queue and process it's messages.

### Pipeline Explanation
1. A new file is droped on the "dl-bronzw-layer" s3 bucket.
2. The rule defined on EventBridge is triggered, creates an event and send it to the SNS topic.
3. The SNS topic foward the received message to the SQS queue.
4. The lambda function is triggered everytime a new message comes to SQS.
5. The Lambda reads the file on the s3 bucket, convert it to parquet and saves it on the "dl-staging-layer" s3 bucket.

## Resources

+ The policies used on this solution was created wiht [aws policy generator](https://awspolicygen.s3.amazonaws.com/policygen.html)'s help.
+ The [policy](https://docs.aws.amazon.com/pt_br/aws-managed-policy/latest/reference/AmazonSNSFullAccess.html) used for SNS full acess.
+ The oficial Terraform [docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) for AWS provider.
