resource "aws_s3_bucket" "attendance_bucket" {
  bucket = "attendance-management-demo-2026-new"

  tags = {
    Name        = "Attendance Management"
    Environment = "Dev"
    Project     = "Attendance Management System"
  }
}

resource "aws_vpc" "attendance_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "Attendance-VPC"
    Environment = "Dev"
    Project     = "Attendance Management System"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.attendance_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = true

  tags = {
    Name        = "Attendance-Public-Subnet"
    Environment = "Dev"
    Project     = "Attendance Management System"
  }
}

resource "aws_internet_gateway" "attendance_igw" {
  vpc_id = aws_vpc.attendance_vpc.id

  tags = {
    Name        = "Attendance-IGW"
    Environment = "Dev"
    Project     = "Attendance Management System"
  }
}


resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.attendance_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.attendance_igw.id
  }

  tags = {
    Name        = "Attendance-Public-RT"
    Environment = "Dev"
    Project     = "Attendance Management System"
  }
}

resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}


resource "aws_security_group" "attendance_sg" {
  name        = "attendance-security-group"
  description = "Security group for Attendance Management application"
  vpc_id      = aws_vpc.attendance_vpc.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Application"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "Attendance-SG"
    Environment = "Dev"
    Project     = "Attendance Management System"
  }
}


# Get the latest Amazon Linux 2023 AMI
data "aws_ssm_parameter" "amazon_linux_ami" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# EC2 Instance
resource "aws_instance" "attendance_server" {
  ami = data.aws_ssm_parameter.amazon_linux_ami.value

  instance_type = "t3.micro"

  subnet_id = aws_subnet.public_subnet.id

  vpc_security_group_ids = [
    aws_security_group.attendance_sg.id
  ]

  key_name = "attendance-key"

  associate_public_ip_address = true

  tags = {
    Name        = "Attendance-Server"
    Environment = "Dev"
    Project     = "Attendance Management System"
  }
}
