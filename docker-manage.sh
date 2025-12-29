#!/bin/bash

# PMI Emergency Call System - Docker Management Script
# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  PMI Emergency Call System - Docker  ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Function to start services
start_services() {
    echo -e "${YELLOW}🚀 Starting PMI Emergency Call System...${NC}"
    docker-compose up -d --build
    echo ""
    echo -e "${GREEN}✅ Services started successfully!${NC}"
    echo -e "${BLUE}📝 View logs with: docker-compose logs -f${NC}"
    echo -e "${BLUE}🌐 API available at: http://localhost:8000${NC}"
    echo -e "${BLUE}📚 API Docs at: http://localhost:8000/docs${NC}"
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Services stopped${NC}"
}

# Function to restart services
restart_services() {
    echo -e "${YELLOW}🔄 Restarting services...${NC}"
    docker-compose restart
    echo -e "${GREEN}✅ Services restarted${NC}"
}

# Function to view logs
view_logs() {
    echo -e "${YELLOW}📋 Viewing logs (Press Ctrl+C to exit)...${NC}"
    docker-compose logs -f
}

# Function to check status
check_status() {
    echo -e "${YELLOW}📊 Service Status:${NC}"
    docker-compose ps
}

# Function to reset everything
reset_all() {
    echo -e "${RED}⚠️  WARNING: This will delete ALL data!${NC}"
    read -p "Are you sure you want to continue? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        echo -e "${YELLOW}🗑️  Removing all containers and volumes...${NC}"
        docker-compose down -v
        echo -e "${GREEN}✅ Everything has been reset${NC}"
    else
        echo -e "${BLUE}Cancelled${NC}"
    fi
}

# Function to access MySQL
access_mysql() {
    echo -e "${YELLOW}🔌 Connecting to MySQL...${NC}"
    docker-compose exec mysql mysql -u pmi_user -ppmi_password pmi_emergency
}

# Function to run migrations
run_migrations() {
    echo -e "${YELLOW}🔄 Running database migrations...${NC}"
    docker-compose exec app alembic upgrade head
    echo -e "${GREEN}✅ Migrations completed${NC}"
}

# Function to init transport system
init_transport() {
    echo -e "${YELLOW}🔄 Initializing transport system...${NC}"
    docker-compose exec app python init_transport_system.py
    echo -e "${GREEN}✅ Transport system initialized${NC}"
}

# Function to show credentials
show_credentials() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Default User Credentials${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${GREEN}👤 Admin User:${NC}"
    echo "   Email: admin@pmi.org"
    echo "   Password: admin123"
    echo ""
    echo -e "${GREEN}🚗 Driver User:${NC}"
    echo "   Email: driver@pmi.org"
    echo "   Password: driver123"
    echo ""
    echo -e "${GREEN}📝 Reporter User:${NC}"
    echo "   Email: reporter@pmi.org"
    echo "   Password: reporter123"
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Database Credentials${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "   Host: localhost"
    echo "   Port: 3306"
    echo "   Database: pmi_emergency"
    echo "   User: pmi_user"
    echo "   Password: pmi_password"
    echo ""
}

# Main menu
show_menu() {
    echo ""
    echo -e "${YELLOW}Please select an option:${NC}"
    echo "1. Start services"
    echo "2. Stop services"
    echo "3. Restart services"
    echo "4. View logs"
    echo "5. Check status"
    echo "6. Access MySQL shell"
    echo "7. Run migrations"
    echo "8. Initialize transport system"
    echo "9. Show credentials"
    echo "10. Reset all (⚠️  deletes all data)"
    echo "0. Exit"
    echo ""
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice: " choice
    echo ""
    
    case $choice in
        1) start_services ;;
        2) stop_services ;;
        3) restart_services ;;
        4) view_logs ;;
        5) check_status ;;
        6) access_mysql ;;
        7) run_migrations ;;
        8) init_transport ;;
        9) show_credentials ;;
        10) reset_all ;;
        0) 
            echo -e "${BLUE}👋 Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid option. Please try again.${NC}"
            ;;
    esac
done
