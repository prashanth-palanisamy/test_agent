output "vpc_id" {
  value       = aws_vpc.this.id
  description = "The ID of the VPC"
}

output "subnet_id" {
  value       = aws_subnet.this.id
  description = "The ID of the subnet"
}

output "security_group_id" {
  value       = aws_security_group.this.id
  description = "The ID of the security group"
}
