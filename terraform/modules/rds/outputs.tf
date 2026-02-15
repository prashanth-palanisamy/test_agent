output "db_instance_id" {
  value       = aws_db_instance.this.id
  description = "The ID of the DB instance"
}
