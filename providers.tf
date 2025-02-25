terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.5"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.1"
    }
    template = {
      source  = "hashicorp/template"
      version = "~> 2.1"
    }
  }
}