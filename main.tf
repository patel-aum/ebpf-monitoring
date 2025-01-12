terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.82.2"
    }
  }
}

provider "aws" {
  region = "ap-south-1" 
}

resource "aws_instance" "monitoring-host" {
  ami                    = "ami-078264b8ba71bc45e"
  instance_type          = "t2.medium"
  security_groups = ["launch-wizard-20"]
  key_name             = "key" 
  tags = {
    Name = "monitoring"
  }
}

resource "aws_instance" "server1" {
  ami                    = "ami-078264b8ba71bc45e"
  instance_type          = "t2.small"
  security_groups = ["launch-wizard-20"]
  key_name             = "key"            
  tags = {
    Name = "server1"
  }
}

output "monitoring_host_ip" {
  value = aws_instance.monitoring-host.public_ip
}
output "server1_host_ip" {
  value = aws_instance.server1.public_ip
}

