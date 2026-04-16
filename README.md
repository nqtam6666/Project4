# NQT Gym Management System

> Hệ thống quản lý phòng gym toàn diện — Fitness SaaS B2B

## Giới thiệu

**NQT Gym Management System** là nền tảng quản lý phòng gym dạng SaaS (Software as a Service) hướng đến các doanh nghiệp phòng gym (B2B). Hệ thống cung cấp đầy đủ các nghiệp vụ từ quản lý hội viên, gói tập, check-in QR, PT, lớp học, đến thương mại điện tử bán thực phẩm chức năng và báo cáo doanh thu.

## Tính năng nổi bật

### Quản lý hội viên (Members)
- Đăng ký, cập nhật, xóa mềm hội viên
- Theo dõi gói tập, ngày hết hạn, lịch sử check-in
- QR code check-in tự động
- Theo dõi chỉ số cơ thể (BMI, cân nặng, % mỡ, % cơ...)
- Hệ thống giới thiệu (referral chain)

### Gói tập & PT
- Quản lý nhiều loại gói tập (theo ngày, có/không PT, sauna...)
- Đăng ký gói tập, tạm dừng, gia hạn
- Quản lý huấn luyện viên cá nhân (PT), gói PT, buổi tập

### Check-in QR
- Quét QR code để điểm danh
- Kiểm tra hạn gói, số lượt còn lại trong ngày
- Lịch sử check-in theo hội viên / chi nhánh

### Nhân viên & Ca làm việc
- Quản lý nhân sự, chức vụ
- Lịch làm việc theo ca

### Thương mại điện tử
- Danh mục sản phẩm (thực phẩm chức năng, đồ thể thao...)
- Giỏ hàng, đơn hàng, thanh toán, hóa đơn
- Mã giảm giá, khuyến mãi, banner
- Quản lý tồn kho, đơn vị vận chuyển

### Thông báo & Email tự động
- Nhắc nhở gói tập sắp hết hạn (N ngày trước, cấu hình qua Admin)
- Email xác nhận đăng ký gói tập
- Notification panel trong admin

### Báo cáo & Xuất dữ liệu
- Báo cáo doanh thu theo tháng (Excel)
- Danh sách hội viên, gói hết hạn (Excel)
- Dashboard thống kê với biểu đồ Chart.js

### Cấu hình động (Dynamic Config)
- Toàn bộ cấu hình hệ thống lưu trong database
- Chỉnh sửa qua Admin Panel, không cần restart server
- Bao gồm: thời hạn JWT, số ngày nhắc trước hết hạn, SMTP, chính sách đặt lịch...

### Phân quyền RBAC
- 4 vai trò: Admin, Quản lý, Huấn luyện viên, Hội viên
- Kiểm soát quyền từng API endpoint
- JWT authentication + refresh token

## Tech Stack

| Thành phần | Công nghệ |
|------------|-----------|
| Backend | Python 3.11+, Flask 3.x |
| ORM | Flask-SQLAlchemy, Flask-Migrate |
| Auth | Flask-JWT-Extended |
| Database | Microsoft SQL Server |
| Email | Flask-Mail (SMTP) |
| Scheduler | APScheduler 3.x |
| Frontend | HTML5, TailwindCSS, Vanilla JS (ES6+) |
| Charts | Chart.js |
| Export | openpyxl (Excel) |
| QR Code | qrcode[pil] |
| Build Tool | Node.js + TailwindCSS CLI |

## Cấu trúc project

```
D:/Project 4/
├── backend/
│   └── app/
│       ├── models/        # ORM models (~60 bảng G6*)
│       ├── routes/        # 15 API blueprints
│       ├── services/      # Business logic (email, config...)
│       ├── jobs/          # Background jobs (APScheduler)
│       ├── utils/         # Auth decorators, response helpers
│       └── seeds/         # Database seed scripts
├── frontend/
│   ├── templates/admin/   # Jinja2 admin templates
│   └── static/
│       ├── css/           # TailwindCSS output
│       ├── js/            # Vanilla JS modules
│       └── uploads/       # Uploaded images (local)
├── database/              # SQL Server DDL scripts
├── .env                   # Biến môi trường (xem .env.example)
├── requirements.txt
└── package.json
```

## Cài đặt & Chạy

### Yêu cầu
- Python 3.11+
- Node.js 18+
- Microsoft SQL Server 2019+
- SQL Server ODBC Driver 17+

### 1. Clone & cài dependencies

```bash
git clone <repo-url>
cd "Project 4"

# Python dependencies
pip install -r requirements.txt

# Node dependencies (Tailwind)
npm install
```

### 2. Cấu hình môi trường

```bash
cp .env.example .env
# Chỉnh sửa .env: DB connection, mail SMTP, JWT secret...
```

Các biến bắt buộc trong `.env`:
```env
FLASK_ENV=development
DB_SERVER=localhost
DB_NAME=GymDB
DB_USERNAME=sa
DB_PASSWORD=your_password
JWT_SECRET_KEY=your_secret_key
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your_app_password
```

### 3. Tạo database & seed dữ liệu

```bash
# Chạy DDL tạo bảng (SQL Server Management Studio)
# Thứ tự: part1 → part2 → part3 → part4

# Seed dữ liệu mẫu
flask seed

# Hoặc reset hoàn toàn
flask seed-fresh
```

### 4. Build Tailwind CSS

```bash
# Development (watch mode)
npm run dev

# Production
npm run build
```

### 5. Chạy server

```bash
flask run --debug
```

Truy cập: `http://localhost:5000/admin/login`

**Tài khoản mặc định** (sau seed):
- Username: `admin`
- Password: `Admin@123`

## API Documentation

Base URL: `http://localhost:5000/api`

### Authentication
```
POST /api/nqt-dang-nhap          # Đăng nhập → JWT token
POST /api/nqt-lam-moi-token      # Refresh token
POST /api/nqt-dang-xuat          # Đăng xuất
GET  /api/nqt-toi                 # Thông tin user hiện tại
```

### Hội viên
```
GET    /api/nqt-hoi-vien          # Danh sách hội viên
POST   /api/nqt-hoi-vien          # Tạo hội viên mới
GET    /api/nqt-hoi-vien/:id      # Chi tiết hội viên
PUT    /api/nqt-hoi-vien/:id      # Cập nhật hội viên
DELETE /api/nqt-hoi-vien/:id      # Xóa mềm hội viên
POST   /api/nqt-diem-danh/qr      # QR check-in
```

### Báo cáo & Export
```
GET /api/nqt-bao-cao/doanh-thu/excel     # Export Excel doanh thu
GET /api/nqt-bao-cao/hoi-vien/excel      # Export Excel hội viên
GET /api/nqt-bao-cao/het-han/excel       # Export gói tập sắp hết hạn
GET /api/nqt-bao-cao/tong-hop            # Tổng hợp số liệu JSON
```

### Response format chuẩn
```json
{
  "nqt_thanh_cong": true,
  "nqt_du_lieu": {},
  "nqt_thong_diep": "Thành công",
  "nqt_loi": []
}
```

## Quy tắc đặt tên

| Thành phần | Quy tắc | Ví dụ |
|------------|---------|-------|
| Bảng DB | `G6` + PascalCase | `G6HoiVien` |
| Cột DB | `g6_` + snake_case | `g6_ho_ten` |
| Python var/func | `nqt_` + snake_case | `nqt_tao_hoi_vien()` |
| Python class | `Nqt` + PascalCase | `NqtDichVuEmail` |
| JS var/func | `nqt` + camelCase | `nqtLayHoiVien()` |
| API URL | `/nqt-` + kebab-case | `/api/nqt-hoi-vien` |

## Nhóm phát triển

| Thành viên | Prefix | Phụ trách |
|------------|--------|-----------|
| Nguyễn Quốc Thắng | `nqt` | Backend API, Admin UI, Database |

## License

Internal project — NQT Gym Management System © 2026
