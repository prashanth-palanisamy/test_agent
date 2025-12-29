variable "vpc_cidr_block" {
  type        = string
  description = "CIDR block for VPC"
}

variable "vpc_name" {
  type        = string
  description = "Name for VPC"
}

variable "vpc_subnet_cidr_block" {
  type        = string
  description = "CIDR block for subnet"
}

variable "vpc_availability_zone" {
  type        = string
  description = "Availability zone for subnet"
}

variable "ec2_ami" {
  type        = string
  description = "AMI for EC2 instance"
}

variable "ec2_instance_type" {
  type        = string
  description = "Instance type for EC2 instance"
}

variable "ec2_key_name" {
  type        = string
  description = "Key name for EC2 instance"
}

variable "ec2_name" {
  type        = string
  description = "Name for EC2 instance"
}

variable "rds_identifier" {
  type        = string
  description = "Identifier for RDS instance"
}

variable "rds_allocated_storage" {
  type        = number
  description = "Allocated storage for RDS instance"
}

variable "rds_engine" {
  type        = string
  description = "Engine for RDS instance"
}

variable "rds_engine_version" {
  type        = string
  description = "Engine version for RDS instance"
}

variable "rds_instance_class" {
  type        = string
  description = "Instance class for RDS instance"
}

variable "rds_name" {
  type        = string
  description = "Name for RDS instance"
}

variable "rds_username" {
  type        = string
  description = "Username for RDS instance"
}

variable "rds_password" {
  type        = string
  description = "Password for RDS instance"
}
