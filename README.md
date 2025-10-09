# ⚡ EV Data Analytics Marketplace  
**Chợ dữ liệu phân tích xe điện**

---

## 🧩 Giới thiệu dự án

**EV Data Analytics Marketplace** là nền tảng **mua bán, chia sẻ và phân tích dữ liệu xe điện (EV)** giữa các bên:
- **Data Providers** (nhà cung cấp dữ liệu)
- **Data Consumers** (hãng xe, startup, nhà nghiên cứu,…)
- **Admin** (quản trị hệ thống)

Mục tiêu của dự án là xây dựng **chợ dữ liệu EV** giúp người dùng **khai thác, giao dịch và trực quan hóa dữ liệu xe điện** một cách **an toàn, minh bạch và dễ sử dụng**.

---

## 🚀 Mục tiêu dự án

### 🎯 Mục tiêu chính
- Phát triển **nền tảng trung gian** cho phép các bên **mua, bán, thuê hoặc chia sẻ dữ liệu EV**.
- Xây dựng hệ thống **dashboard phân tích EV** (hành vi lái xe, hiệu suất pin, trạm sạc, CO₂ tiết kiệm,...).

### 🎯 Mục tiêu phụ
- Hỗ trợ **API truy xuất dữ liệu EV** cho nghiên cứu & phát triển sản phẩm.
- Phân tích tự động bằng **AI / ML pipeline (phiên bản nâng cấp trong tương lai)**.

---

## 🧱 Kiến trúc hệ thống

Frontend 
↓
FastAPI Backend (Python)
↓
PostgreSQL Database
↓
Data Storage / API Integration


### Thành phần chính:
- **FastAPI Backend:** Xử lý API, logic nghiệp vụ, xác thực và quản lý dữ liệu.
- **Frontend (Jinja2):** Giao diện web cho người dùng (HTML/CSS/JS).
- **Database:** PostgreSQL / SQLite (tùy môi trường).
- **Authentication:** JWT / Session-based.
- **Role-based System:** Data Provider – Data Consumer – Admin.

---

## 🧑‍💻 Các tính năng chính

### 👥 Dành cho Data Consumer
- Tìm kiếm, lọc và mua dữ liệu EV (theo thời gian, khu vực, loại xe...).
- Xem báo cáo, biểu đồ và dashboard trực quan.
- Tải dữ liệu raw hoặc đã qua xử lý.

### 📦 Dành cho Data Provider
- Đăng tải và quản lý dataset.
- Thiết lập giá, mô tả và quyền truy cập.
- Theo dõi doanh thu và phản hồi người dùng.

### 🛠️ Dành cho Admin
- Quản lý user, datasets, orders.
- Duyệt nội dung dữ liệu đăng lên.
- Thống kê và giám sát hệ thống.

---

## 📂 Cấu trúc thư mục

```bash
ev-data-marketplace/
│
├── app/
│   ├── main.py                # Entry point FastAPI
│   ├── models/                # ORM models (User, Product, Order, Record)
│   ├── routers/               # API routes
│   ├── schemas/               # Pydantic Schemas
│   ├── templates/             # HTML Templates 
│   ├── static/                # CSS / JS / Images
│   └── database.py            # Kết nối CSDL
│
├── tests/                     # Unit tests
├── requirements.txt           # Danh sách thư viện Python
├── README.md                  # Tài liệu dự án
└── run.sh                     # Script chạy server nhanh

⚙️ Cài đặt & chạy dự án
1️⃣ Clone repository
git clone https://github.com/ltnhat0313/ev-data-marketplace.git
cd ev-data-marketplace

2️⃣ Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
3️⃣ Cài đặt dependencies
pip install -r requirements.txt

4️⃣ Chạy server
uvicorn app.main:app --reload


🔗 Truy cập tại: http://127.0.0.1:8000/web/home

🧮 Ví dụ mô hình dữ liệu
| Model       | Thuộc tính chính                            |
| ----------- | ------------------------------------------- |
| **User**    | id, name, email, role, password_hash        |
| **Product** | id, name, price, provider_id, file_path     |
| **Order**   | id, consumer_id, product_id, amount, status |
| **Record**  | id, data_type, description, file_url        |

🧭 Roadmap (Kế hoạch 1 tháng)
| Tuần       | Công việc chính                          | Kết quả mong đợi           |
| ---------- | ---------------------------------------- | -------------------------- |
| **Tuần 1** | Thiết lập backend, DB, CRUD cơ bản       | API hoạt động, DB liên kết |
| **Tuần 2** | Hoàn thiện giao diện (HTML, CSS, ...   ) | Web hiển thị dữ liệu       |
| **Tuần 3** | Kết nối dataset & tạo dashboard          | Biểu đồ EV hoạt động       |
| **Tuần 4** | Phân quyền, thanh toán, kiểm thử         | MVP hoàn chỉnh & demo nhóm |

🧠 Công nghệ sử dụng

| Thành phần      | Công nghệ              |
| --------------- | ---------------------- |
| Backend         | FastAPI (Python 3.11+) |
| Frontend        | HTML, CSS, ...  .      |
| Database        | PostgreSQL / SQLite    |
| Auth            | JWT / OAuth2           |
| Visualization   | Chart.js, Plotly       |
| Version Control | Git + GitHub           |

🧑‍🤝‍🧑 Nhóm phát triển

| Thành viên           | Vai trò                             | Nhiệm vụ                                                              |
| -------------------- | ----------------------------------- | --------------------------------------------------------------------- |
| **Lê Thành Nhật**    | 🧠 **Team Lead / System Architect** | Quản lý dự án, thiết kế kiến trúc hệ thống, tích hợp backend–frontend |
| **Nguyễn Ngọc Toàn** | 🎨 **Frontend Developer**           | Xây dựng giao diện Jinja2, CSS, điều hướng và UI tổng thể             |
| **Võ Duy Tuấn**      | ⚙️ **Backend Developer**            | API, Models, Database, xử lý logic nghiệp vụ                          |
| **Nguyễn Hữu Lộc**   | 📊 **Data Analyst / Visualization** | Dashboard, biểu đồ, xử lý dữ liệu mẫu EV                              |
| **Lê Văn Nam**       | 🧪 **QA / Tester**                  | Kiểm thử hệ thống, viết tài liệu, demo và báo cáo                     |

🌐 Liên hệ

👤 Lead: Lê Thành Nhật

📧 Email: nhatlt6183@ut.edu.vn

💻 GitHub: @ltnhat0313

🏫 Học kỳ: HK1 2025–2026 

