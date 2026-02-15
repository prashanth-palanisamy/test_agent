variable "ami" {
  type        = string
  description = "The ID of the AMI"
}

variable "instance_type" {
  type        = string
  description = "The type of instance to start"
}

variable "subnet_id" {
  type        = string
  description = "The ID of the subnet"
}

variable "security_group_id" {
  type        = string
  description = "The ID of the security group"
}

variable "key_name" {
  type        = string
  description = "The name of the key to use for the instance"
}
