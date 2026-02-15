variable "identifier" {
  type        = string
  description = "The identifier of the DB instance"
}

variable "allocated_storage" {
  type        = number
  description = "The amount of storage to allocate for the DB instance"
}

variable "engine" {
  type        = string
  description = "The database engine to use"
}

variable "engine_version" {
  type        = string
  description = "The version of the database engine to use"
}

variable "instance_class" {
  type        = string
  description = "The instance class to use for the DB instance"
}

variable "username" {
  type        = string
  description = "The username for the DB instance"
}

variable "password" {
  type        = string
  sensitive   = true
  description = "The password for the DB instance"
}

variable "security_group_id" {
  type        = string
  description = "The ID of the security group"
}
