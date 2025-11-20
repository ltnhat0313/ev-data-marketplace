#  EV Data Analytics Marketplace  
**Chợ Dữ Liệu Phân Tích Xe Điện – Microservices Architecture**

##  Giới thiệu  
EV Data Analytics Marketplace là nền tảng kết nối **Nhà cung cấp dữ liệu (Provider)** và **Người tiêu dùng dữ liệu (Consumer)** trong lĩnh vực xe điện.  
Hệ thống được xây dựng theo **kiến trúc Microservices**, sử dụng **Docker**, **Traefik Gateway**, và tích hợp **AI Analytics**.

**Tính năng chính:**  
-  Dashboard quản trị, thống kê doanh thu  
-  AI Service: gợi ý dataset, dự báo nhu cầu (Prophet/Scikit-learn)  
-  Marketplace: upload dataset, giao dịch  
-  Bảo mật: JWT, 2FA, RBAC  

---

##  Kiến trúc hệ thống  

| Service | Công nghệ | Vai trò | Internal Port |
|--------|-----------|----------|----------------|
| **Traefik Gateway** | Traefik | Routing, Load balancing | 80 / 8080 |
| **Auth Service** | Python (FastAPI) | Đăng ký, đăng nhập, JWT, 2FA | 8000 |
| **Marketplace Service** | Python (FastAPI) | Quản lý dataset, giao dịch | 8000 |
| **AI Service** | Python (FastAPI) | Gợi ý, dự báo, mô hình AI | 8000 |
| **Dashboard UI** | Python (Jinja2) | Giao diện quản trị | 8000 |
| **Landing Page** | Java (Spring Boot) | Trang giới thiệu | 8080 |
| **Database** | MySQL 8 | Lưu trữ dữ liệu | 3306 |

---

##  Cấu trúc thư mục

```
ev-data-marketplace/
│
├── docker-compose.yml
├── mysql-init/
│   └── init.sql
│
├── frontends/
│   ├── dashboard-ui/
│   └── landing-page/
│
├── services/
│   ├── auth-service/
│   ├── marketplace-service/
│   ├── ai-service/
│   └── ai-utils.py
│
└── test_backend_Le_Thanh_Nhat.py
```

---

##  Hướng dẫn cài đặt & chạy

### 1️⃣ Yêu cầu  
- Docker + Docker Compose  
- (Tùy chọn) Python 3.11 để chạy test backend  

---

### 2️⃣ Clone dự án và khởi chạy hệ thống

```
git clone https://github.com/ltnhat0313/ev-data-marketplace.git
cd ev-data-marketplace
docker-compose up --build
```

---

### 3️⃣ Truy cập ứng dụng  

| Thành phần | URL |
|-----------|------|
| Landing Page | http://localhost |
| Dashboard UI | http://localhost/ui/login |
| Traefik Dashboard | http://localhost:8080 |
| Auth API Docs | http://localhost/api/auth/docs |
| Marketplace API Docs | http://localhost/api/datasets/docs |

---

##  Tài khoản demo

| Role | Email | Mật khẩu | Quyền hạn |
|------|--------|------------|-------------|
| Admin | admin@evdata.com | 123456 | Toàn quyền |
| Provider | provider@evdata.com | 123456 | Upload dataset |
| Consumer | consumer@evdata.com | 123456 | Mua/Tải dataset |

---

##  Kiểm thử Backend tự động

```
pip install requests
python test_backend_Le_Thanh_Nhat.py
```

---

##  Cấu hình môi trường (.env)

```
# Database
MYSQL_ROOT_PASSWORD=161105
DATABASE_URL=mysql+pymysql://root:161105@mysqldb:3306/market_db

# Security
SECRET_KEY=bi_mat_khong_the_bat_mi_123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# System Paths
UPLOAD_DIR=/app/uploads
MODEL_DIR=/app/models
```
