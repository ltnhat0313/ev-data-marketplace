# ⚡ EV Data Analytics Marketplace  
**Chợ dữ liệu phân tích xe điện**

---

## 🧩 Giới thiệu dự án

**EV Data Analytics Marketplace** là nền tảng **mua bán, chia sẻ và phân tích dữ liệu xe điện (EV)** giữa các bên:
- **Data Providers** (nhà cung cấp dữ liệu)
- **Data Consumers** (nhà nghiên cứu, OEM, startup, hãng xe,…)
- **Admin** (quản trị hệ thống)

Hệ thống cho phép người dùng **tìm kiếm, thuê/mua và trực quan hóa dữ liệu EV** thông qua giao diện web thân thiện và API mở rộng.

---

## 🚀 Mục tiêu

### 🎯 Mục tiêu chính
- Xây dựng **nền tảng giao dịch dữ liệu EV** minh bạch, an toàn.
- Tích hợp **phân tích & dashboard dữ liệu** giúp người dùng khai thác insight dễ dàng.

### 🎯 Mục tiêu phụ
- Cho phép **tùy chọn thuê dữ liệu theo gói hoặc qua API**.
- Hỗ trợ **AI phân tích tự động** (hiệu suất pin, hành vi lái, trạm sạc, CO₂ tiết kiệm...).

---

## 🧱 Kiến trúc tổng quan

```

Frontend (Jinja2 Templates)
↓
FastAPI (Python)
↓
PostgreSQL Database
↓
Data Storage / API Integration

````

### Các thành phần chính:
- **FastAPI Backend:** REST API + Routing giao diện.
- **Frontend (Jinja2):** Giao diện HTML hiển thị danh mục, dashboard, thanh toán.
- **Database:** PostgreSQL (hoặc SQLite khi dev).
- **Authentication:** JWT Token / Session.
- **Role System:** Data Provider, Data Consumer, Admin.

---

## 🧑‍💻 Các tính năng chính

### 👥 1. Dành cho Data Consumer
- Tìm kiếm và lọc dữ liệu theo:
  - Thời gian, khu vực, loại xe, loại pin, định dạng dữ liệu.
- Mua/thuê dữ liệu (theo lượt tải, gói thuê bao, hoặc API).
- Xem **Dashboard phân tích EV**:
  - SoC/SoH pin, hành vi sạc, quãng đường, mức CO₂ tiết kiệm,...

### 📦 2. Dành cho Data Provider
- Đăng tải, mô tả và định giá gói dữ liệu.
- Theo dõi lượt tải, doanh thu.
- Cập nhật dữ liệu định kỳ qua API.

### 🛠️ 3. Dành cho Admin
- Quản lý user, datasets, giao dịch.
- Duyệt dữ liệu, xử lý tranh chấp.
- Báo cáo tổng quan hoạt động hệ thống.

---

## 📂 Cấu trúc thư mục

```bash
ev-data-marketplace/
│
├── app/
│   ├── main.py                # Entry point FastAPI
│   ├── models/                # Models (User, Product, Order, Record)
│   ├── routers/               # API routes (users, products, orders, records)
│   ├── schemas/               # Pydantic schemas
│   ├── templates/             # HTML (Jinja2 templates)
│   ├── static/                # CSS / JS / Images
│   └── database.py            # Database connection
│
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── run.sh                     # Script chạy server nhanh
````

---

## ⚙️ Cài đặt & chạy dự án

### 1️⃣ Clone repo

```bash
git clone https://github.com/ltnhat0313/ev-data-marketplace.git
cd ev-data-marketplace
```

### 2️⃣ Tạo môi trường ảo

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3️⃣ Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Chạy server

```bash
uvicorn app.main:app --reload
```

Truy cập tại: 👉 **[http://127.0.0.1:8000/web/home](http://127.0.0.1:8000/web/home)**

---

## 🧮 Ví dụ mô hình dữ liệu (Database Models)

| Model       | Thuộc tính chính                            |
| ----------- | ------------------------------------------- |
| **User**    | id, name, email, role, password_hash        |
| **Product** | id, name, price, provider_id, file_path     |
| **Order**   | id, consumer_id, product_id, amount, status |
| **Record**  | id, data_type, description, file_url        |

---

## 💡 Roadmap (Kế hoạch phát triển)

| Giai đoạn  | Nội dung                                  | Kết quả mong đợi             |
| ---------- | ----------------------------------------- | ---------------------------- |
| **Tuần 1** | Thiết lập backend, models, database       | CRUD users, products, orders |
| **Tuần 2** | Giao diện Jinja2 (Home, Login, Dashboard) | Web hiển thị được dữ liệu    |
| **Tuần 3** | Tích hợp API dữ liệu EV (fake dataset)    | Biểu đồ và thống kê EV       |
| **Tuần 4** | Bổ sung thanh toán & phân quyền           | Hoàn thiện MVP & Demo        |

---

## 🧠 Công nghệ sử dụng

| Thành phần      | Công nghệ           |
| --------------- | ------------------- |
| Backend         | FastAPI, Python     |
| Frontend        | HTML, CSS, Jinja2   |
| Database        | PostgreSQL / SQLite |
| Auth            | JWT / OAuth2        |
| Visualization   | Chart.js, Plotly    |
| Version Control | Git + GitHub        |

---

## 🧑‍🤝‍🧑 Nhóm phát triển

| Thành viên       | Vai trò         | Nhiệm vụ chính                        |
| ---------------- | --------------- | ------------------------------------- |
| **Toàn**         | Backend Lead    | API, Database, Models                 |
| **Nam**          | Frontend Dev    | Jinja2 Templates, CSS, Layout         |
| **Nhật (bạn)**   | Project Manager | Kiến trúc tổng thể, tích hợp hệ thống |
| **Thành viên 4** | Data Analyst    | Dashboard, Visualization              |
| **Thành viên 5** | QA / Tester     | Kiểm thử, tài liệu, demo              |

---

## 🧾 Giấy phép

Dự án phát hành theo giấy phép **MIT License** — bạn được phép sử dụng, sửa đổi và triển khai tự do cho mục đích học tập và nghiên cứu.

---

## 🌐 Liên hệ

* 📧 **Lê Thành Nhật** – `nhatlt6183@ut.edu.vn`
* 💻 GitHub: [@ltnhat0313](https://github.com/ltnhat0313)
* 📅 Dự án học kỳ: HK1 2025–2026
* 🏷️ Trường: UTH

---

```

---

Bạn có muốn tôi thêm **hình minh họa kiến trúc hệ thống (sơ đồ block hoặc luồng dữ liệu)** vào README này không?  
Nếu có, tôi sẽ tạo luôn ảnh `.png` phù hợp để bạn commit vào thư mục `docs/`.
```
