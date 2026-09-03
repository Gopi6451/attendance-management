output "ec2_instance_id" {
  description = "ID of the Attendance EC2 instance"
  value       = aws_instance.attendance_server.id
}

output "ec2_public_ip" {
  description = "Public IP of the Attendance EC2 instance"
  value       = aws_instance.attendance_server.public_ip
}

output "vpc_id" {
  description = "ID of the Attendance VPC"
  value       = aws_vpc.attendance_vpc.id
}

output "subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public_subnet.id
}

output "s3_bucket_name" {
  description = "Name of the Attendance S3 bucket"
  value       = aws_s3_bucket.attendance_bucket.bucket
}