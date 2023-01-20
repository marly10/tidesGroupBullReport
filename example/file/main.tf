provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
    region = "us-east-1"
}

resource "aws_instance" "ec2_exampl" {
      ami = "${var.ami}"
      iam_instance_profile = "${var.iam_instance_profile}"
     instance_type ="${var.instance_type}"
     key_name = "${var.key_name}"
    tags = {
       Name = "Terraform_001"
    }
}



