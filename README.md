# Event Driven Data Processing
An entirely serverless event driven data pipeline built on AWS cloud for high scalability and flexibility. The core objective of this project was to build a simple and short but effective and robust pipeline for automated data processing.

To feed this project a small Python app was created, to make requests on the Spotify API and ingest the obtained data on a AWS S3 bucket. The entire event driven pipeline was built on AWS cloud with serverless services.

## Solution's Architecture
<p align="left">
  <img src="https://github.com/gabriel-barata/images/blob/master/event-driven-data-pipeline/diagram.png" alt="App Diagram">
</p>

### Components
+ **Terraform**: Terraform is an open-source infrastructure-as-code (IaC) tool developed by HashiCorp. It enables you to define and provision infrastructure resources across various cloud providers and other infrastructure platforms in a declarative way. All AWS services used in this pipeline was deployed with Terraform.
+ **Amazon S3 (Simple Storage Service)**: Amazon S3 its a object storage service high scalable and durable. Our architecture uses s3 as a data repository, being sort of a Data Lake prototype. In further projects i'll bring a better structred Data Lake.
+ **Amazon EventBridge**: EventBridge is a serverless service that uses events to connect application components together. Our architecture uses EventBridge to capture an specific event and send it to a target.
+ **Amazon SNS (Simple Notification Service)**: Amazon SNS is a managed motification service that provides message delivery from publishers to subscribers. In our architecture Amazon SNS is configured to receive events from EventBridge and them foward it to its subscribers. It is an important point in our project, as it brings great flexibility to the pipeline. Add further workloads to this initial project becomes a way easier, since any new pipeline can be docked to the SNS topic.
+ **Amazon SQS (Simple Queue Service)**: Amazon SQS is a serverless queue service. In our architecture it's configured as a SNS subscriber, everytime a new message is received SQS puts it on a queue. Amazon SQS brings scalability to our project and guarantees that every message received will be processed by the Lambda Function, it helps us surpass some of the Lambda's limitations about concurrent executions.
+ **Amazon Lambda**: AWS Lambda is a serverless compute service. In our architecture a lambda function was configured to consume the SQS queue and process it's messages, reading the file from the s3 bucket, validating it and then converting it and writing on the next layer.

### The Benefits of This Architecture
+ **Serverless**: In a cloud context, "serverless" refers to a cloud computing model where the cloud provider manages the infrastructure and resources required to run and scale applications. No need to manage or provision servers explicitily, just deploy code.
+ **Flexibility**: It's an exetremely flexible solution. If another developer or team wants to, for whatever reason, do some job on this same bucket and new come files, it would just have to subscribe his workload to the SNS topic.
+ **Scalability**: Lambda automatically scales up based on incoming events, so we should no ahve have problems if multiple files are droped on the s3 bucket at once. And with the SQS queue we can surpass the Lambda limitations on concurrent executions. That is, one file or a thousand of files, it doesnt matter, all should be processed without big problems.

### Pipeline Explanation
1. A new file is droped on the "dl-bronze-layer" s3 bucket.
2. The rule defined on EventBridge is triggered, creates an event and send it's metadata, like the file name, to the SNS topic.
3. The SNS topic foward the received message to it's subscribers, like the SQS queue.
4. The lambda function consume the SQS queue, and triggers everytime a new message comes into.
5. The Lambda reads the file on the s3 bucket, valid it and convert to parquet and saves it on the "dl-staging-layer" s3 bucket.

## Local Deployment
Couple instructions for local deployment
### Requirements
+ [Python](https://www.python.org/downloads/) 3.7 or more
+ [git](https://git-scm.com/downloads) installed
+ an [AWS](https://aws.amazon.com/) account with admin privileges
+ [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed and configured
+ [Terraform](https://developer.hashicorp.com/terraform/downloads) installed

Open the terminal and run the following commands to setup the project
```
# clone this repo to your machine
git clone -b master https://github.com/gabriel-barata/Event-Driven-Data-Processing

# navigate to the repo's folder
cd Event-Driven-Data-Processing

# give the necessary permissions to our setup file
chmod +x setup.sh

# setup the environment
./setup.sh deploy

# at this point you can check at your AWS account to see services up
# run the python app to feed the S3 bucket
./setup.sh run
```
After usage you can destroy resources running

`./setup.sh destroy`

## Resources

+ The policies used on this solution was created with [aws policy generator](https://awspolicygen.s3.amazonaws.com/policygen.html)'s help.
+ The [policy](https://docs.aws.amazon.com/pt_br/aws-managed-policy/latest/reference/AmazonSNSFullAccess.html) used for SNS full acess.
+ The oficial Terraform [docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) for AWS provider.
+ AWS Lambda [developer's guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html).

## Contact
<a href="https://www.linkedin.com/in/gabriel-barata/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="gabriel-barata" height="30" width="40" /></a>
