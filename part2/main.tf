terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state-bucket"
    key    = "part2/terraform.tfstate"
    region = "ap-south-1"
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = { Name = "${var.project_name}-vpc", Project = var.project_name }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-igw" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
  tags                    = { Name = "${var.project_name}-subnet" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = { Name = "${var.project_name}-rt" }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "flask_sg" {
  name   = "${var.project_name}-flask-sg"
  vpc_id = aws_vpc.main.id

  ingress { from_port = 22,   to_port = 22,   protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 5000, to_port = 5000, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0,    to_port = 0,    protocol = "-1",  cidr_blocks = ["0.0.0.0/0"] }

  tags = { Name = "${var.project_name}-flask-sg" }
}

resource "aws_security_group" "angular_sg" {
  name   = "${var.project_name}-angular-sg"
  vpc_id = aws_vpc.main.id

  ingress { from_port = 22, to_port = 22, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 80, to_port = 80, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0,  to_port = 0,  protocol = "-1",  cidr_blocks = ["0.0.0.0/0"] }

  tags = { Name = "${var.project_name}-angular-sg" }
}

resource "aws_security_group_rule" "flask_from_angular" {
  type                     = "ingress"
  from_port                = 5000
  to_port                  = 5000
  protocol                 = "tcp"
  security_group_id        = aws_security_group.flask_sg.id
  source_security_group_id = aws_security_group.angular_sg.id
  description              = "Allow Flask from Angular SG"
}

resource "aws_instance" "flask_server" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.flask_sg.id]
  user_data              = file("${path.module}/flask_user_data.sh")
  tags = { Name = "${var.project_name}-flask", Project = var.project_name, Role = "backend" }
}

resource "aws_instance" "angular_server" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.angular_sg.id]

  user_data = templatefile("${path.module}/angular_user_data.sh", {
    flask_private_ip = aws_instance.flask_server.private_ip
  })

  tags       = { Name = "${var.project_name}-angular", Project = var.project_name, Role = "frontend" }
  depends_on = [aws_instance.flask_server]
}
