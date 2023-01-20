variable "name"{
      type = string
  default = ""
}
variable "ami" {
  type = string
  default = ""
}
variable "iam_instance_profile" {
  type = string
  default = ""
}
variable "instance_type" {
  type = string
  default = ""
}
variable "key_name" {
  type = string
  default = ""
}
variable "access_key" {
  type = string
  default = ""
}
variable "secret_key" {
  type = string
  default = ""
}




resource "aws_instance" "ec2_exampl" {
      ami = "${var.ami}"
      iam_instance_profile = "${var.iam_instance_profile}"
     instance_type ="${var.instance_type}"
     key_name = "${var.key_name}"
    tags = {
        Name = "${var.name}"
    }
}
