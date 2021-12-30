terraform {
  required_version = ">= 1.0.11"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.70.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.2.0"
    }
    null = {
      source  = "hashicorp/null"
      version = ">= 3.1.0"
    }
  }
}