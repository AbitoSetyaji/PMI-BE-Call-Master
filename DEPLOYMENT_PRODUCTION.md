# 🚀 Panduan Deployment PMI Emergency Call System
**Domain:** pmikotasmg.site

---

## 📋 Prasyarat di VPS

```bash
# Install Docker & Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Pastikan port terbuka
# Port 80 (HTTP), 443 (HTTPS)
```

---

## 📁 Struktur di VPS

```
/opt/pmi/
├── PMI-BE-Call-Master/   # Backend + Nginx + SSL
└── PMI-FE-Call-Master/   # Frontend
```

---

## 🔧 Langkah Deployment

### Step 1: Upload ke VPS
```bash
# Dari lokal Windows (Git Bash/PowerShell)
scp -r F:\KP\posko\PMI-BE-Call-Master root@IP_VPS:/opt/pmi/
scp -r F:\KP\posko\PMI-FE-Call-Master root@IP_VPS:/opt/pmi/
```

### Step 2: SSH ke VPS dan Deploy
```bash
ssh root@IP_VPS
cd /opt/pmi/PMI-BE-Call-Master

# Buat file .env
cat > .env << EOF
MYSQL_ROOT_PASSWORD=your_secure_password
MYSQL_PASSWORD=your_db_password
JWT_SECRET_KEY=your_jwt_secret_key_min_32_chars
EOF

# Jalankan deployment
chmod +x deploy-production.sh
./deploy-production.sh
```

---

## 🌐 Hasil Akhir

| URL | Fungsi |
|-----|--------|
| https://pmikotasmg.site | Website Utama |
| https://pmikotasmg.site/api/docs | API Documentation |

---

## 🔍 Troubleshooting

```bash
# Cek status container
docker ps

# Lihat logs backend
docker logs pmi-be-app -f

# Lihat logs nginx
docker logs pmi-nginx -f

# Restart semua
docker-compose -f docker-compose.prod.yml restart
```

---

## 📱 Mobile App

API URL sudah dikonfigurasi ke:
```
https://pmikotasmg.site/api
```

Jalankan mobile app:
```bash
cd PMI-Mobile-Master
npm start
```
