#!/bin/bash
set -e
exec > /var/log/user-data.log 2>&1

echo "=== Bootstrap start ==="

apt update -y
apt install -y python3 python3-pip git nginx

curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

npm install -g @angular/cli

git clone https://github.com/palashgupta94/my_fullstack_app.git /app
cd /app

cd /app/backend
pip3 install -r requirements.txt

cat > /etc/systemd/system/flask.service << 'EOF'
[Unit]
Description=Flask Backend
After=network.target

[Service]
User=root
WorkingDirectory=/app/backend
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=5
Environment=MONGODB_ATLAS_URI=mongodb://localhost:27017
Environment=MONGODB_DB_NAME=mydatabase
Environment=MONGODB_COLLECTION_NAME=mycollection

[Install]
WantedBy=multi-user.target
EOF

cd /app/frontend
npm install
export NODE_OPTIONS="--max-old-space-size=512"
ng build --configuration=production

rm -rf /var/www/html/*
cp -r dist/*/ /var/www/html/

cat > /etc/nginx/sites-available/myapp << 'EOF'
server {
    listen 80;
    server_name _;
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

ln -sf /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/myapp
rm -f /etc/nginx/sites-enabled/default

systemctl daemon-reload
systemctl enable flask nginx
systemctl start flask
systemctl restart nginx

echo "=== Bootstrap complete ==="
