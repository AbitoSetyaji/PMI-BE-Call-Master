#!/bin/bash
# ============================================
# PMI Emergency Call System - Deployment Script
# Domain: pmikotasmg.site
# Server: 148.230.100.61
# ============================================

set -e

DOMAIN="pmikotasmg.site"
EMAIL="admin@pmikotasmg.site"
PROJECT_DIR="/opt/pmi"

echo "🚀 PMI Emergency Call System - Production Deployment"
echo "======================================================"

# Step 1: Create project directory
echo "📁 Step 1: Setting up directories..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Step 2: Create network if not exists
echo "📡 Step 2: Creating Docker network..."
docker network create pmi-network 2>/dev/null || echo "Network already exists"

# Step 3: Start backend services (MySQL + FastAPI)
echo "🔧 Step 3: Starting Backend Services..."
cd $PROJECT_DIR/PMI-BE-Call-Master

# Create volumes
docker volume create certbot_data 2>/dev/null || true
docker volume create certbot_www 2>/dev/null || true

# Start MySQL and Backend
docker-compose -f docker-compose.prod.yml up -d mysql
echo "⏳ Waiting for MySQL to be healthy..."
sleep 60

docker-compose -f docker-compose.prod.yml up -d backend
echo "⏳ Waiting for backend to be ready..."
sleep 30

# Step 4: Create temp nginx for SSL certificate
echo "🔐 Step 4: Setting up SSL Certificate..."
cat > /tmp/nginx-init.conf << 'EOF'
events {
    worker_connections 1024;
}
http {
    server {
        listen 80;
        server_name pmikotasmg.site www.pmikotasmg.site api.pmikotasmg.site;
        
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        location / {
            return 200 'PMI Emergency Call System - Setting up SSL...';
            add_header Content-Type text/plain;
        }
    }
}
EOF

# Stop existing nginx if running
docker stop pmi-nginx-init 2>/dev/null || true
docker rm pmi-nginx-init 2>/dev/null || true

# Start init nginx
docker run -d --name pmi-nginx-init \
    -p 80:80 \
    -v /tmp/nginx-init.conf:/etc/nginx/nginx.conf:ro \
    -v certbot_www:/var/www/certbot \
    --network pmi-network \
    nginx:alpine

sleep 5

# Step 5: Get SSL Certificate
echo "🔐 Step 5: Obtaining SSL Certificate from Let's Encrypt..."
docker run --rm \
    -v certbot_data:/etc/letsencrypt \
    -v certbot_www:/var/www/certbot \
    certbot/certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN \
    -d api.$DOMAIN

# Step 6: Stop init nginx and start full stack
echo "🔧 Step 6: Starting full nginx with SSL..."
docker stop pmi-nginx-init && docker rm pmi-nginx-init
rm /tmp/nginx-init.conf

docker-compose -f docker-compose.prod.yml up -d nginx certbot

# Step 7: Start frontend
echo "🖥️ Step 7: Starting Frontend..."
cd $PROJECT_DIR/PMI-FE-Call-Master
docker-compose -f docker-compose.prod.yml up -d --build

echo ""
echo "✅ Deployment Complete!"
echo "======================================================"
echo "🌐 Website: https://$DOMAIN"
echo "📚 API Docs: https://$DOMAIN/api/docs"
echo ""
echo "📋 Check status: docker ps"
echo "📋 View logs: docker-compose logs -f"
