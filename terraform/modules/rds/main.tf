resource "aws_db_instance" "this" {
  identifier           = var.identifier
  allocated_storage    = var.allocated_storage
  engine               = var.engine
  engine_version       = var.engine_version
  instance_class       = var.instance_class
  name                 = var.name
  username             = var.username
  password             = var.password
  vpc_security_group_ids = [var.security_group_id]
  db_subnet_group_name = aws_db_subnet_group.this.name
}

resource "aws_db_subnet_group" "this" {
  name       = var.name
  subnet_ids = [var.subnet_id]
}
