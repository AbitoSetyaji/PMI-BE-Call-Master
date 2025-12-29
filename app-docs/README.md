# PMI Emergency Call System - Documentation

Selamat datang di dokumentasi lengkap untuk PMI Emergency Call System (Sistem Tanggap Darurat Palang Merah Indonesia).

## 📚 Daftar Dokumentasi

Folder ini berisi tiga dokumentasi utama yang menjelaskan sistem secara komprehensif:

### 1. [API Documentation](./API_DOCUMENTATION.md)

**Apa yang ada di dalamnya:**

- Dokumentasi lengkap semua API endpoints
- Request dan response format
- Contoh penggunaan untuk setiap endpoint
- Authentication dan authorization
- Error handling
- Status codes

**Untuk siapa:**

- Frontend developers
- Mobile app developers
- API consumers
- Integration partners

**Kapan menggunakannya:**

- Saat mengintegrasikan dengan sistem
- Saat membuat client aplikasi
- Saat melakukan testing API
- Sebagai referensi endpoint

---

### 2. [Flow Documentation](./FLOW_DOCUMENTATION.md)

**Apa yang ada di dalamnya:**

- Alur kerja sistem end-to-end
- Business process flows
- User journey diagrams
- System architecture flow
- Status transition flows
- Request-response lifecycle

**Untuk siapa:**

- Product managers
- Business analysts
- System architects
- Developers (untuk memahami big picture)
- Stakeholders

**Kapan menggunakannya:**

- Saat memahami bagaimana sistem bekerja
- Saat merancang fitur baru
- Saat melakukan analisis bisnis
- Saat onboarding team member baru

---

### 3. [Technical Documentation](./TECH_DOCUMENTATION.md)

**Apa yang ada di dalamnya:**

- Technology stack details
- Project structure explanation
- Database schema dan ERD
- Core components breakdown
- Security implementation
- Development setup guide
- Deployment guide
- Best practices
- Troubleshooting

**Untuk siapa:**

- Backend developers
- DevOps engineers
- Database administrators
- Technical leads
- System administrators

**Kapan menggunakannya:**

- Saat setup development environment
- Saat melakukan deployment
- Saat debugging issues
- Saat melakukan maintenance
- Sebagai referensi teknis

---

## 🚀 Quick Start Guide

### Untuk Frontend/Mobile Developer

1. Baca [API Documentation](./API_DOCUMENTATION.md) untuk memahami endpoints
2. Lihat [Flow Documentation](./FLOW_DOCUMENTATION.md) untuk user journey
3. Mulai integrasi dengan authentication endpoints
4. Gunakan Postman/cURL untuk testing

### Untuk Backend Developer

1. Baca [Technical Documentation](./TECH_DOCUMENTATION.md) untuk setup
2. Follow development setup guide
3. Pelajari project structure
4. Lihat [Flow Documentation](./FLOW_DOCUMENTATION.md) untuk business logic

### Untuk Product Manager/Business Analyst

1. Mulai dengan [Flow Documentation](./FLOW_DOCUMENTATION.md)
2. Pahami complete user journey
3. Review status transitions dan workflows
4. Gunakan diagrams untuk presentasi

### Untuk DevOps Engineer

1. Baca [Technical Documentation](./TECH_DOCUMENTATION.md)
2. Focus pada Deployment Guide section
3. Review security implementation
4. Setup monitoring dan logging

---

## 📋 System Overview

**PMI Emergency Call System** adalah backend API untuk mengelola:

- 🚨 Laporan darurat (Emergency Reports)
- 🚑 Kendaraan darurat (Emergency Vehicles)
- 👤 Pengguna dan pengemudi (Users & Drivers)
- 📍 Pelacakan lokasi pengemudi (Driver Location Tracking)
- 📝 Penugasan kendaraan (Vehicle Assignments)
- 📊 Logging aktivitas (Activity Logs)

### Key Features

- ✅ RESTful API dengan FastAPI
- ✅ JWT Authentication
- ✅ Role-based access control (Admin, Driver, Reporter)
- ✅ Real-time driver location tracking
- ✅ Comprehensive assignment management
- ✅ Standardized response format
- ✅ Database migrations dengan Alembic
- ✅ Async operations dengan SQLAlchemy

---

## 🏗️ Architecture Overview

```
┌─────────────┐
│   Clients   │ (Web App, Mobile App)
└──────┬──────┘
       │
       │ HTTPS/REST API
       │
┌──────▼──────────────────────┐
│   FastAPI Application       │
│   - Authentication          │
│   - Business Logic          │
│   - Data Validation         │
└──────┬──────────────────────┘
       │
       │ SQLAlchemy ORM
       │
┌──────▼──────────────────────┐
│   MySQL Database            │
│   - Users                   │
│   - Vehicles                │
│   - Reports                 │
│   - Assignments             │
│   - Locations               │
└─────────────────────────────┘
```

---

## 🔗 Quick Links

### Base Information

- **Base URL**: `http://localhost:8000`
- **API Version**: 1.0.0
- **API Docs (Swagger)**: `http://localhost:8000/docs`
- **API Docs (ReDoc)**: `http://localhost:8000/redoc`

### Main Endpoints

- Authentication: `/api/auth/*`
- Users: `/api/users/*`
- Vehicles: `/api/vehicles/*`
- Vehicle Types: `/api/vehicle-types/*`
- Reports: `/api/reports/*`
- Assignments: `/api/assignments/*`
- Driver Locations: `/api/driver-locations/*`

### Health Check

```bash
GET http://localhost:8000/health
```

---

## 📞 Support

Jika Anda memiliki pertanyaan atau memerlukan bantuan:

1. **Technical Issues**: Check [Technical Documentation](./TECH_DOCUMENTATION.md) troubleshooting section
2. **API Questions**: Refer to [API Documentation](./API_DOCUMENTATION.md)
3. **Business Process**: See [Flow Documentation](./FLOW_DOCUMENTATION.md)
4. **Bug Reports**: Create issue di repository
5. **Feature Requests**: Diskusikan dengan product team

---

## 📝 Documentation Updates

Dokumentasi ini diperbarui secara berkala. Untuk update terbaru:

- Check commit history
- Review changelog
- Watch repository untuk notifications

**Last Updated**: November 3, 2025  
**Version**: 1.0.0

---

## 🎯 Next Steps

Pilih dokumentasi yang sesuai dengan kebutuhan Anda dan mulai explore sistem!

- 📖 [API Documentation](./API_DOCUMENTATION.md) - Untuk integrasi API
- 🔄 [Flow Documentation](./FLOW_DOCUMENTATION.md) - Untuk memahami alur kerja
- ⚙️ [Technical Documentation](./TECH_DOCUMENTATION.md) - Untuk development dan deployment

Happy coding! 🚀
