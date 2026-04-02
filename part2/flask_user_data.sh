#!/bin/bash
set -e
exec > /var/log/user-data.log 2>&1

echo "=== Flask instance bootstrap ==="

apt update -y
apt install -y python3 python3-pip git

git clone https://github.com/palashgupta94/my_fullstack_app.git /app
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

mkdir -p /data
systemctl daemon-reload
systemctl enable flask
systemctl start flask

echo "=== Flask running on port 5000 ==="
