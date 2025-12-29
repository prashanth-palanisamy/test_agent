variable "cidr_block" {
  type        = string
  description = "The CIDR block for the VPC"
}

variable "vpc_name" {
  type        = string
  description = "The name of the VPC"
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

variable "security_group_ingress_from_port" {
  type        = number
  description = "The from port for the security group ingress"
}

variable "security_group_ingress_to_port" {
  type        = number
  description = "The to port for the security group ingress"
}

variable "security_group_ingress_protocol" {
  type        = string
  description = "The protocol for the security group ingress"
}

variable "security_group_ingress_cidr_blocks" {
  type        = list(string)
  description = "The CIDR blocks for the security group ingress"
}

variable "ec2_ami" {
  type        = string
  description = "The ID of the AMI"
}

variable "ec2_instance_type" {
  type        = string
  description = "The type of instance"
}

variable "rds_identifier" {
  type        = string
  description = "The identifier of the RDS instance"
}

variable "rds_allocated_storage" {
  type        = number
  description = "The allocated storage for the RDS instance"
}

variable "rds_engine" {
  type        = string
  description = "The engine for the RDS instance"
}

variable "rds_engine_version" {
  type        = string
  description = "The engine version for the RDS instance"
}

variable "rds_instance_class" {
  type        = string
  description = "The instance class for the RDS instance"
}

variable "rds_username" {
  type        = string
  description = "The username for the RDS instance"
}

variable "rds_password" {
  type        = string
  description = "The password for the RDS instance"
}
