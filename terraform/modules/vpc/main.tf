resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  tags = {
    Name = var.name
  }
}

resource "aws_subnet" "this" {
  cidr_block = var.subnet_cidr_block
  vpc_id     = aws_vpc.this.id
  availability_zone = var.availability_zone
}

resource "aws_security_group" "this" {
  name        = var.security_group_name
  description = var.security_group_description
  vpc_id      = aws_vpc.this.id

  ingress {
    from_port   = var.security_group_ingress_from_port
    to_port     = var.security_group_ingress_to_port
    protocol    = var.security_group_ingress_protocol
    cidr_blocks = var.security_group_ingress_cidr_blocks
  }
}
