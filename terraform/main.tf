module "vpc" {
  source = "./modules/vpc"

  cidr_block                 = var.cidr_block
  tags                       = var.tags
  subnet_cidr_block          = var.subnet_cidr_block
  availability_zone          = var.availability_zone
  security_group_name        = var.security_group_name
  security_group_description = var.security_group_description
}

module "ec2" {
  source = "./modules/ec2"

  ami               = var.ec2_ami
  instance_type     = var.ec2_instance_type
  subnet_id         = module.vpc.subnet_id
  security_group_id = module.vpc.security_group_id
  key_name          = var.ec2_key_name
}

module "rds" {
  source = "./modules/rds"

  identifier        = var.rds_identifier
  allocated_storage = var.rds_allocated_storage
  engine            = var.rds_engine
  engine_version    = var.rds_engine_version
  instance_class    = var.rds_instance_class
  username          = var.rds_username
  password          = var.rds_password
  security_group_id = module.vpc.security_group_id
}
