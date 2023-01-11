provider "aws" {
shared_credentials_file = "~/.aws/credentials"
    region = "us-east-1"
}

resource "aws_instance" "ec2_exampl" {
      ami = "ami-08fdec01f5df9998f"
      iam_instance_profile = "gha_poc"
     instance_type = "t2.micro" 
     key_name = "t_mac"
    tags = {
        Name = "Terraform_001"
    }
}
