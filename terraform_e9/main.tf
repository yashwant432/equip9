provider "aws" {
  region = "ap-south-1"  # region
}

# Create an S3 bucket
resource "aws_s3_bucket" "http_service_bucket" {
  bucket = "e9-http-service-bucket"  # S3 bucket name
  #acl    = "private"  # Recommended ACL for privacy
}

# Create a security group for the EC2 instance
resource "aws_security_group" "http_service_sg" {
  name        = "http_service_sg"
  description = "Allow inbound HTTP traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow public HTTP access
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH (for debugging/management)
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all outbound traffic
  }
}

# IAM Role to access S3
resource "aws_iam_role" "ec2_role" {
  name = "EC2RoleForS3Access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [ {
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

# Attach policy to allow EC2 access to S3
resource "aws_iam_role_policy" "ec2_s3_policy" {
  name = "EC2S3AccessPolicy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action   = "s3:ListBucket"
      Effect   = "Allow"
      Resource = "arn:aws:s3:::${aws_s3_bucket.http_service_bucket.bucket}"
    }]
  })
}

# Create IAM Instance Profile for EC2
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "EC2InstanceProfileForS3Access"
  role = aws_iam_role.ec2_role.name
}

# Create EC2 instance for the HTTP service
resource "aws_instance" "http_service_instance" {
  ami           = "ami-09b0a86a2c84101e1"  # Ubuntu AMI 
  instance_type = "t2.micro"  

  key_name = "ubuntuserver"  # SSH key name for accessing the instance

  # Attach security group and IAM instance profile
  security_groups       = [aws_security_group.http_service_sg.name]
  iam_instance_profile  = aws_iam_instance_profile.ec2_instance_profile.name

  # User data to install dependencies and run the HTTP service
  user_data = <<-EOF
    #!/bin/bash
    apt update -y
    apt install -y python3 python3-pip git
    pip3 install flask boto3
    cd /home/ubuntu
    git clone https://github.com/yashwant432/equip9.git
    cd equip9/http_code
    nohup python3 equip_app.py &  # Run the Flask app in the background
  EOF

  # Optionally add tags to the instance
  tags = {
    Name = "HTTP-Service-Instance"
  }
}

# Output the public IP of the EC2 instance
output "instance_ip" {
  value = aws_instance.http_service_instance.public_ip
}

# Output the instance name
output "instance_name" {
  value = aws_instance.http_service_instance.tags["Name"]
}

# Output the S3 bucket name
output "s3_bucket_name" {
  value = aws_s3_bucket.http_service_bucket.bucket
}
