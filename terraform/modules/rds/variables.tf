variable "identifier" {
  type        = string
  description = "Identifier for RDS instance"
}

variable "allocated_storage" {
  type        = number
  description = "Allocated storage for RDS instance"
}

variable "engine" {
  type        = string
  description = "Engine for RDS instance"
}

variable "engine_version" {
  type        = string
  description = "Engine version for RDS instance"
}

variable "instance_class" {
  type        = string
  description = "Instance class for RDS instance"
}

variable "name" {
  type        = string
  description = "Name for RDS instance"
}

variable "username" {
  type        = string
  description = "Username for RDS instance"
}

variable "password" {
  type        = string
  description = "Password for RDS instance"
}

variable "security_group_id" {
  type        = string
  description = "Security group ID for RDS instance"
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID for RDS instance"
}
