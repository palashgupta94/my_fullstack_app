output "flask_public_ip"   { value = aws_instance.flask_server.public_ip }
output "flask_private_ip"  { value = aws_instance.flask_server.private_ip }
output "angular_public_ip" { value = aws_instance.angular_server.public_ip }
output "flask_url"         { value = "http://${aws_instance.flask_server.public_ip}:5000" }
output "angular_url"       { value = "http://${aws_instance.angular_server.public_ip}" }
output "vpc_id"            { value = aws_vpc.main.id }
