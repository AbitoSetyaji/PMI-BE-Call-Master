#!/bin/bash
# ============================================
# PMI Emergency Call System - Deployment Script
# Domain: pmikotasmg.site
# ============================================

set -e

DOMAIN="pmikotasmg.site"
EMAIL="admin@pmikotasmg.site"  # Change to your email

echo "🚀 PMI Emergency Call System - Deployment"
echo "=========================================="

# Step 1: Create network if not exists
echo "📡 Step 1: Creating Docker network..."
docker network create pmi-network 2>/dev/null || echo "Network already exists"

# Step 2: Start backend services first (without nginx)
echo "🔧 Step 2: Starting Backend (MySQL + FastAPI)..."
cd /opt/pmi/PMI-BE-Call-Master

# Create temporary nginx config for HTTP only (for certbot)
cat > nginx/nginx-init.conf << 'EOF'
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

# Step 3: Start with init nginx config
echo "🔧 Step 3: Starting services with temp nginx..."
docker-compose -f docker-compose.prod.yml up -d mysql backend

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 30

# Step 4: Start nginx with init config
docker run -d --name pmi-nginx-init \
    -p 80:80 \
    -v $(pwd)/nginx/nginx-init.conf:/etc/nginx/nginx.conf:ro \
    -v certbot_www:/var/www/certbot \
    --network pmi-network \
    nginx:alpine

# Step 5: Get SSL Certificate
echo "🔐 Step 4: Obtaining SSL Certificate from Let's Encrypt..."
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

# Step 6: Stop init nginx and start full nginx
echo "🔧 Step 5: Restarting with full nginx config..."
docker stop pmi-nginx-init && docker rm pmi-nginx-init
rm nginx/nginx-init.conf

docker-compose -f docker-compose.prod.yml up -d nginx certbot

# Step 7: Start frontend
echo "🖥️ Step 6: Starting Frontend..."
cd /opt/pmi/PMI-FE-Call-Master
docker-compose -f docker-compose.prod.yml up -d --build

echo ""
echo "✅ Deployment Complete!"
echo "=========================================="
echo "🌐 Website: https://$DOMAIN"
echo "📚 API Docs: https://$DOMAIN/api/docs"
echo ""
echo "📋 Check status: docker ps"
echo "📋 View logs: docker-compose logs -f"
