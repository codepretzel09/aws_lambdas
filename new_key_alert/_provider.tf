terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  shared_config_files      = ["/path/to/config"]
  shared_credentials_files = ["/path/to/credentials"]
  profile                  = "some-profile"
}
