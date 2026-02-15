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

variable "ec2_ami" {
  type        = string
  description = "The ID of the AMI"
}

variable "ec2_instance_type" {
  type        = string
  description = "The type of instance to start"
}

variable "ec2_key_name" {
  type        = string
  description = "The name of the key to use for the instance"
}

variable "rds_identifier" {
  type        = string
  description = "The identifier of the DB instance"
}

variable "rds_allocated_storage" {
  type        = number
  description = "The amount of storage to allocate for the DB instance"
}

variable "rds_engine" {
  type        = string
  description = "The database engine to use"
}

variable "rds_engine_version" {
  type        = string
  description = "The version of the database engine to use"
}

variable "rds_instance_class" {
  type        = string
  description = "The instance class to use for the DB instance"
}

variable "rds_username" {
  type        = string
  description = "The username for the DB instance"
}

variable "rds_password" {
  type        = string
  sensitive   = true
  description = "The password for the DB instance"
}
