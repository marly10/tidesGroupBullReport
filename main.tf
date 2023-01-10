provider "aws" {
  region                  = "us-east-1"
  profile                 = "default"
}

resource "aws_instance" "ec2_instance" {
    ami = "ami-08fdec01f5df9998f"
    subnet_id = "subnet-090cb74e9416cbcbd"
    instance_type = "t2.micro"
    key_name = "t_mac"
}