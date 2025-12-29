variable "ami" {
  type        = string
  description = "AMI for EC2 instance"
}

variable "instance_type" {
  type        = string
  description = "Instance type for EC2 instance"
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID for EC2 instance"
}

variable "security_group_id" {
  type        = string
  description = "Security group ID for EC2 instance"
}

variable "key_name" {
  type        = string
  description = "Key name for EC2 instance"
}

variable "name" {
  type        = string
  description = "Name for EC2 instance"
}
