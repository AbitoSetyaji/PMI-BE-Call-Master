# PMI Emergency Call System - Backend

Backend API for PMI (Palang Merah Indonesia) Emergency Call System built with FastAPI.

## Project Structure

```
PMI-BE-Call-Master/
├── alembic/        # Database migrations
├── core/           # Configuration & security
├── db/             # Database session
├── docker/         # Docker configs
│   ├── nginx/      # Nginx configuration
│   ├── init-db/    # MySQL initialization
│   └── *.sh        # Deployment scripts
├── models/         # SQLAlchemy models
├── routes/         # API endpoints
├── schemas/        # Pydantic schemas
├── scripts/        # Utility scripts
├── services/       # Business logic
├── utils/          # Helper functions
├── main.py         # Application entry
└── requirements.txt
```

## Quick Start (Development)

```bash
docker-compose up -d
```

## Production Deployment

### Prerequisites
- VPS with Docker & Docker Compose installed
- Domain pointing to VPS IP (148.230.100.61)

### Deployment Steps

1. **Upload to VPS:**
```bash
scp -r PMI-BE-Call-Master/ root@148.230.100.61:/opt/pmi/
scp -r PMI-FE-Call-Master/ root@148.230.100.61:/opt/pmi/
```

2. **SSH to VPS:**
```bash
ssh root@148.230.100.61
```

3. **Copy environment file:**
```bash
cd /opt/pmi/PMI-BE-Call-Master
cp .env.production .env
```

4. **Run deployment script:**
```bash
chmod +x docker/deploy-production.sh
./docker/deploy-production.sh
```

## API Docs
- Development: http://localhost:8000/docs
- Production: https://pmikotasmg.site/api/docs

## Default Credentials
- Admin: admin@pmi.id / admin123
- Driver: driver1@pmi.id / driver123
- Reporter: reporter@pmi.id / reporter123

## Production URLs
- Website: https://pmikotasmg.site
- API: https://api.pmikotasmg.site
- Server IP: http://148.230.100.61
