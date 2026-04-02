output "instance_public_ip" {
  value = aws_instance.app_server.public_ip
}

output "app_url" {
  description = "Angular frontend via Nginx"
  value       = "http://${aws_instance.app_server.public_ip}"
}

output "flask_url" {
  description = "Flask backend direct"
  value       = "http://${aws_instance.app_server.public_ip}:5000"
}
