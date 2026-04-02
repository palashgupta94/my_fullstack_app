#!/bin/bash
set -e
exec > /var/log/user-data.log 2>&1

echo "=== Angular instance bootstrap ==="

apt update -y
apt install -y git nginx

curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
npm install -g @angular/cli

FLASK_IP="${flask_private_ip}"
echo "Flask IP: $FLASK_IP"

git clone https://github.com/palashgupta94/my_fullstack_app.git /app
cd /app/frontend

npm install
export NODE_OPTIONS="--max-old-space-size=512"
ng build --configuration=production

rm -rf /var/www/html/*
cp -r dist/*/ /var/www/html/

cat > /etc/nginx/sites-available/myapp << NGINXEOF
server {
    listen 80;
    server_name _;
    root /var/www/html;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api {
        proxy_pass http://$FLASK_IP:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
NGINXEOF

ln -sf /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/myapp
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
systemctl enable nginx

echo "=== Angular running, Flask at $FLASK_IP ==="
