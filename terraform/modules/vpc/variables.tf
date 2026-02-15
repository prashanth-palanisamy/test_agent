variable "cidr_block" {
  type        = string
  description = "The CIDR block for the VPC"
}

variable "tags" {
  type        = map(string)
  description = "A map of tags to add to the VPC"
}

variable "subnet_cidr_block" {
  type        = string
  description = "The CIDR block for the subnet"
}

variable "availability_zone" {
  type        = string
  description = "The availability zone for the subnet"
}

variable "security_group_name" {
  type        = string
  description = "The name of the security group"
}

variable "security_group_description" {
  type        = string
  description = "The description of the security group"
}
