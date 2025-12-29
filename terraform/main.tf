module "vpc" {
  source = "./modules/vpc"

  cidr_block        = var.vpc_cidr_block
  name              = var.vpc_name
  subnet_cidr_block = var.vpc_subnet_cidr_block
  availability_zone = var.vpc_availability_zone
}

module "ec2" {
  source = "./modules/ec2"

  ami           = var.ec2_ami
  instance_type = var.ec2_instance_type
  subnet_id     = module.vpc.subnet_id
  security_group_id = module.vpc.security_group_id
  key_name               = var.ec2_key_name
  name = var.ec2_name
}

module "rds" {
  source = "./modules/rds"

  identifier           = var.rds_identifier
  allocated_storage    = var.rds_allocated_storage
  engine               = var.rds_engine
  engine_version       = var.rds_engine_version
  instance_class       = var.rds_instance_class
  name                 = var.rds_name
  username             = var.rds_username
  password             = var.rds_password
  security_group_id = module.vpc.security_group_id
  subnet_id = module.vpc.subnet_id
}
