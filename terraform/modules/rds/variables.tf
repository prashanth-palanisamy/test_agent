variable "identifier" {
  type        = string
  description = "The identifier of the RDS instance"
}

variable "allocated_storage" {
  type        = number
  description = "The allocated storage for the RDS instance"
}

variable "engine" {
  type        = string
  description = "The engine for the RDS instance"
}

variable "engine_version" {
  type        = string
  description = "The engine version for the RDS instance"
}

variable "instance_class" {
  type        = string
  description = "The instance class for the RDS instance"
}

variable "username" {
  type        = string
  description = "The username for the RDS instance"
}

variable "password" {
  type        = string
  description = "The password for the RDS instance"
}

variable "db_subnet_group_name" {
  type        = string
  description = "The name of the DB subnet group"
}

variable "security_group_id" {
  type        = string
  description = "The ID of the security group"
}
