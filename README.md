# ⚡ EV Data Analytics Marketplace
### Chợ Dữ Liệu Phân Tích Xe Điện

---

## 🚀 Giới thiệu Dự Án

**EV Data Analytics Marketplace** là nền tảng giúp kết nối **Nhà Cung Cấp Dữ Liệu (Data Provider)** và **Người Tiêu Dùng Dữ Liệu (Data Consumer)** trong lĩnh vực xe điện (EV).  
Người dùng có thể **đăng tải, mua bán, thuê và phân tích dữ liệu EV** như:

- Hành vi lái xe  
- Hiệu suất pin  
- Tần suất sạc  
- Giao dịch năng lượng (V2G)

---

## 🎯 Mục tiêu chính

- Xây dựng hệ thống có **3 vai trò chính**:
  - 🧑‍💻 **Data Consumer** – Người dùng dữ liệu  
  - 🏭 **Data Provider** – Nhà cung cấp dữ liệu  
  - 👨‍🔧 **Admin** – Quản trị hệ thống  

- Tích hợp **AI gợi ý & thống kê** (Scikit-learn)  
- Hỗ trợ **Dashboard động** (Chart.js)  
- Cung cấp **API public** và mô phỏng **thanh toán thuê bao**

---

## 🧠 Kiến trúc & Công nghệ

| Thành phần | Công nghệ sử dụng |
|-------------|------------------|
| **Backend** | FastAPI + SQLAlchemy + Alembic |
| **Frontend** | HTML / Jinja2 + TailwindCSS + Chart.js |
| **Database** | PostgreSQL / MySQL |
| **Auth** | JWT + Role-based Access Control |
| **AI / Data** | Scikit-learn, Pandas, Prophet |
| **Triển khai** | Docker + Render / Railway |
| **Quản lý phiên bản** | Git + GitHub |

---

## 📁 Cấu trúc thư mục

```bash
ev-data-marketplace/
│
├── app/                      # Backend
│   ├── api/                  # API routes (auth, dataset, admin, AI...)
│   ├── core/                 # Config, JWT, bảo mật
│   ├── models/               # Database models (SQLAlchemy)
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Logic nghiệp vụ (AI, CSV, Billing)
│   └── main.py               # Entry point FastAPI
│
├── web/                      # Frontend
│   ├── templates/            # HTML (Jinja2)
│   ├── static/               # CSS, JS, hình ảnh
│   └── app.js                # Logic frontend
```

---

## 🧩 Hướng Dẫn Cài Đặt & Chạy Dự Án

### 1️⃣ Chuẩn bị môi trường

Yêu cầu:

- Python >= 3.10 (cụ thể 3.11.9)  
- Node.js (chỉ cần nếu build Tailwind)  
- Git  
- PostgreSQL  

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Cấu hình môi trường (.env)

Tạo file `.env` tại thư mục gốc:

```bash
DATABASE_URL=postgresql+psycopg2://postgres:1234@localhost:5432/ev_marketplace
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
DEBUG=True
```

---

### 3️⃣ Tạo database & migration

```bash
alembic upgrade head
```

Nếu chưa có migration:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

---

### 4️⃣ Chạy server FastAPI

```bash
uvicorn app.main:app --reload
```

Truy cập sau khi chạy thành công:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Tại đây có thể test API (đăng ký, đăng nhập, upload, mua dữ liệu...).

---

### 5️⃣ Chạy giao diện web (HTML / Jinja2)

Nếu bạn dùng **Jinja2 template**:

- Tạo thư mục `/web/templates` và `/web/static`
- Truy cập qua trình duyệt:  
  👉 [http://127.0.0.1:8000/web/consumer](http://127.0.0.1:8000/web/consumer)

Nếu dùng **React/Tailwind**:

```bash
npm install
npm run dev
```

---

### 6️⃣ Chạy AI module (tùy chọn)

```bash
python -m app.services.ai_train
```

Mô hình **TF-IDF + Forecast** sẽ được train và lưu file `.pkl` trong `/models`.

---

### 7️⃣ Tài khoản demo (mẫu)

| Role | Email | Mật khẩu | Quyền |
|------|--------|----------|--------|
| Admin | [admin@ev.com](mailto:admin@ev.com) | 123456 | Toàn quyền |
| Provider | [provider@ev.com](mailto:provider@ev.com) | 123456 | Đăng dữ liệu |
| Consumer | [consumer@ev.com](mailto:consumer@ev.com) | 123456 | Mua dữ liệu |

---

### 8️⃣ Deploy (Render / Railway)

**Cách nhanh nhất:**

1. Fork repo này  
2. Đăng nhập [https://render.com](https://render.com)  
3. Chọn **New Web Service → Connect GitHub Repo**
4. Lệnh build:
   ```bash
   pip install -r requirements.txt
   ```
5. Lệnh chạy:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```
6. Sau khi deploy, cập nhật biến môi trường (`DATABASE_URL`, `JWT_SECRET`, ...)

---

## 👥 Thành viên nhóm & Vai trò

| Mã | Họ tên | Vai trò chính | Phụ trách |
|----|--------|----------------|------------|
| **TV1** | Lê Thành Nhật | 💡 Lead / Backend Core Architect | Backend, Auth, DB, API |
| **TV2** | Nguyễn Hữu Lộc | 🧰 Provider Portal Engineer | Upload CSV, Quản lý dữ liệu, Doanh thu |
| **TV3** | Lê Văn Nam | 🖥️ Consumer Portal & UI Lead | Giao diện, Tìm kiếm nâng cao, Dashboard |
| **TV4** | Nguyễn Ngọc Toàn | 🧾 Admin & Billing Engineer | Quản lý user, Duyệt dữ liệu, Báo cáo |
| **TV5** | Võ Duy Tuấn | 🤖 Data & AI Engineer | Xử lý CSV, Ẩn danh, AI gợi ý & Dự báo |

---

## 🧭 Lộ trình chi tiết từng thành viên (3 tuần)

### 🧠 TV1 – Lead / Backend Core Architect
| Tuần | Công việc chính | Kết quả mong đợi |
|------|------------------|------------------|
| Tuần 1 | Thiết kế ERD, setup FastAPI, DB, JWT Auth | API `/register`, `/login` hoạt động |
| Tuần 2 | API CRUD Dataset, Upload CSV, Transaction | Các API chính hoạt động ổn định |
| Tuần 3 | Role-based Auth, Mock payment, Deploy | Backend chạy ổn định trên Render/Railway |

---

### ⚙️ TV2 – Provider Portal Engineer
| Tuần | Công việc chính | Kết quả mong đợi |
|------|------------------|------------------|
| Tuần 1 | Thiết kế form upload (Tên, mô tả, giá, file CSV) | Giao diện upload hoàn chỉnh |
| Tuần 2 | Kết nối API thật, quản lý dataset | Provider có thể xem trạng thái dữ liệu |
| Tuần 3 | Trang doanh thu + biểu đồ Chart.js | Provider xem được doanh thu và lượt tải |

---

### 💻 TV3 – Consumer Portal & UI Lead
| Tuần | Công việc chính | Kết quả mong đợi |
|------|------------------|------------------|
| Tuần 1 | Trang chủ hiển thị dataset, tìm kiếm nâng cao | Hiển thị dữ liệu mock |
| Tuần 2 | Kết nối API thật, xem chi tiết, mua dữ liệu | Mua dữ liệu hoạt động (mock pay) |
| Tuần 3 | Dashboard động + AI gợi ý thật | Dashboard & AI hoạt động realtime |

---

### 🔐 TV4 – Admin & Billing Engineer
| Tuần | Công việc chính | Kết quả mong đợi |
|------|------------------|------------------|
| Tuần 1 | Trang quản lý người dùng, danh sách dữ liệu | UI Admin cơ bản |
| Tuần 2 | API duyệt dữ liệu + xem lịch sử giao dịch | Duyệt dataset hoạt động thật |
| Tuần 3 | Báo cáo thị trường, chia doanh thu (mock) | Admin có thể xem tổng quan toàn hệ thống |

---

### 🤖 TV5 – Data & AI Engineer
| Tuần | Công việc chính | Kết quả mong đợi |
|------|------------------|------------------|
| Tuần 1 | Xử lý file CSV, preview 5 dòng đầu, ẩn danh hóa | Upload hiển thị dữ liệu |
| Tuần 2 | AI gợi ý TF-IDF + Cosine Similarity | API `/ai/recommendations` hoạt động |
| Tuần 3 | Dự báo lượt tải (Linear Regression / Prophet) | API `/ai/forecast` + biểu đồ xu hướng |

---

## 📊 Kết quả cuối cùng

✅ Web hoạt động đủ 3 vai trò: Admin – Provider – Consumer  
✅ Có Upload CSV, Duyệt, Mua, Tải dữ liệu thật  
✅ Có Dashboard Chart.js & AI gợi ý thật (Scikit-learn)  
✅ Có API public, Role-based Auth, Log giao dịch  
✅ Có tài liệu, slide, demo video, deploy cloud

---

## 🧩 Sơ đồ hệ thống (Tổng quan)

```bash
Data Provider  →  Upload CSV  →  (Admin Duyệt)  →  Marketplace
                                 ↓
                     (AI xử lý) + Consumer Mua + Giao dịch + Dashboard
```
