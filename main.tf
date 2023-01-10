provider "aws" {
    profile = "poc_admin"
    region = "us-east-1"
}

resource "aws_instance" "ec2_exampl" {
      ami = "ami-08fdec01f5df9998f"
    instance_type = "t2.micro" 
     key_name = "t_mac"
    tags = {
        Name = "Terraform_0122d1"
    }
}
