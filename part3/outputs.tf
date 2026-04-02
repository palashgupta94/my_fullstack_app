output "alb_dns_name" {
  description = "ALB DNS name — application access point"
  value       = aws_lb.main.dns_name
}

output "app_url" {
  description = "Angular frontend URL via ALB"
  value       = "http://${aws_lb.main.dns_name}"
}

output "api_url" {
  description = "Flask backend API URL via ALB"
  value       = "http://${aws_lb.main.dns_name}/api"
}

output "backend_ecr_url" {
  description = "Flask backend ECR repository URL"
  value       = aws_ecr_repository.backend.repository_url
}

output "frontend_ecr_url" {
  description = "Angular frontend ECR repository URL"
  value       = aws_ecr_repository.frontend.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}
