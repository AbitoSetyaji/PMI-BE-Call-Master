#!/bin/bash
# ============================================
# PMI-BE-Call Deployment Script
# ============================================

set -e

echo "🚀 PMI Backend Deployment Script"
echo "================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Step 1: Create shared network if not exists
echo -e "${YELLOW}Step 1: Creating shared network...${NC}"
docker network create pmi-shared-network 2>/dev/null || echo "Network already exists"

# Step 2: Generate SSL certificates if not exists
if [ ! -f "./nginx/ssl/server.crt" ]; then
    echo -e "${YELLOW}Step 2: Generating SSL certificates...${NC}"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ./nginx/ssl/server.key \
        -out ./nginx/ssl/server.crt \
        -subj "/C=ID/ST=Jakarta/L=Jakarta/O=PMI/OU=IT/CN=148.230.100.61" \
        -addext "subjectAltName = IP:148.230.100.61"
    echo -e "${GREEN}SSL certificates generated!${NC}"
else
    echo -e "${GREEN}SSL certificates already exist${NC}"
fi

# Step 3: Copy .env.production to .env if needed
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Step 3: Copying .env.production to .env...${NC}"
    cp .env.production .env
    echo -e "${GREEN}.env file created!${NC}"
fi

# Step 4: Build and start containers
echo -e "${YELLOW}Step 4: Building and starting containers...${NC}"
docker-compose -f docker-compose.prod.yml up -d --build

# Step 5: Show status
echo -e "${GREEN}=================================${NC}"
echo -e "${GREEN}✅ Backend deployment complete!${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""
echo "Services:"
echo "  - MySQL:   Running on internal network"
echo "  - FastAPI: Running on internal network"
echo "  - Nginx:   https://148.230.100.61:501"
echo ""
echo "API Documentation: https://148.230.100.61:501/docs"
echo ""
echo "To check logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
