terraform {
  required_version = ">= 1.5.3"

  cloud {
    organization = "eng-test" # Replace with your organization name

    workspaces {
      name = "eng-test" # Replace with your workspace name
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
}

provider "aws" {
}