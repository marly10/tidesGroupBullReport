provider "aws" {}

resource "aws_instance" "ec2_example" {
      ami = "ami-08fdec01f5df9998f"
    instance_type = "t2.micro" 
     key_name = "t_mac"
    tags = {
        Name = "Terraform_1101"
    }
}
