variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name for all resource naming"
  type        = string
  default     = "my-fullstack-app-docker"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "public_subnet_a_cidr" {
  type    = string
  default = "10.0.1.0/24"
}

variable "public_subnet_b_cidr" {
  type    = string
  default = "10.0.2.0/24"
}

variable "desired_count" {
  description = "Number of ECS tasks per service"
  type        = number
  default     = 1
}

variable "backend_image" {
  description = "ECR image URI for Flask backend"
  type        = string
  default     = ""
}

variable "frontend_image" {
  description = "ECR image URI for Angular frontend"
  type        = string
  default     = ""
}
