module "vpc" {
  source = "./modules/vpc"

  cidr_block                         = var.cidr_block
  name                               = var.vpc_name
  subnet_cidr_block                  = var.subnet_cidr_block
  availability_zone                  = var.availability_zone
  security_group_name                = var.security_group_name
  security_group_description         = var.security_group_description
  security_group_ingress_from_port   = var.security_group_ingress_from_port
  security_group_ingress_to_port     = var.security_group_ingress_to_port
  security_group_ingress_protocol    = var.security_group_ingress_protocol
  security_group_ingress_cidr_blocks = var.security_group_ingress_cidr_blocks
}

module "ec2" {
  source = "./modules/ec2"

  ami               = var.ec2_ami
  instance_type     = var.ec2_instance_type
  subnet_id         = module.vpc.subnet_id
  security_group_id = module.vpc.security_group_id
}

module "rds" {
  source = "./modules/rds"

  identifier           = var.rds_identifier
  allocated_storage    = var.rds_allocated_storage
  engine               = var.rds_engine
  engine_version       = var.rds_engine_version
  instance_class       = var.rds_instance_class
  username             = var.rds_username
  password             = var.rds_password
  db_subnet_group_name = aws_db_subnet_group.this.name
  security_group_id    = module.vpc.security_group_id
}

resource "aws_db_subnet_group" "this" {
  name       = "my_db_subnet_group"
  subnet_ids = [module.vpc.subnet_id]

  tags = {
    Name = "My DB subnet group"
  }
}
