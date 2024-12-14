provider "aws" {
  region = "ap-south-1"  # Change to your desired region
}

# Create an S3 bucket
resource "aws_s3_bucket" "http_service_bucket" {
  bucket = "e9-http-service-bucket"  # Choose a unique bucket name
  
}

# Create EC2 instance for the HTTP service
resource "aws_instance" "http_service_instance" {
  ami           = "ami-053b12d3152c0cc71"  # Replace with the desired AMI
  instance_type = "t2.micro"  # Adjust instance type as needed

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
