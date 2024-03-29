terraform {

  required_providers {

    aws = {

      source  = "hashicorp/aws"
      version = "~> 4.0"

    }
  }
}

#Configuring the terraform backend
terraform {

  backend "s3" {

    ## the bucket that you serve as backend for terraform
    ## it basically holds the .tfstate file 
    ## you'll need to change this file tpo run locally
    bucket = "terraform-backend-269012942764"
    
    key    = "spotify-data-platform.tfstate"
    region = "us-east-1"

  }
}

# Configure the AWS Provider
provider "aws" {

  region = "us-east-1"

}