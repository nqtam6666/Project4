# NQT Gym Management System - Project Rules

## ⛔ QUY TẮC AN TOÀN CHO CLAUDE (BẮT BUỘC)

### 🚫 TUYỆT ĐỐI KHÔNG ĐƯỢC LÀM

1. **KHÔNG XOÁ FILE/FOLDER** mà không hỏi trước
2. **KHÔNG ĐỔI TÊN FILE/FOLDER** mà không hỏi trước
3. **KHÔNG GHI ĐÈ TOÀN BỘ FILE** - chỉ dùng Edit tool để sửa đúng phần cần thiết
4. **KHÔNG CHẠY LỆNH NGUY HIỂM**: `rm -rf`, `del /f`, `git reset --hard`, `DROP TABLE`, `TRUNCATE`
5. **KHÔNG SỬA FILE CỦA NGƯỜI KHÁC** (có tiền tố khác `nqt_`) trừ khi được yêu cầu rõ ràng
6. **KHÔNG ĐỔI TÊN BẢNG DB, TÊN BIẾN, HÀM, CLASS** đã tồn tại — dù tiền tố là gì (`nqt_`, `nxv_`, hay bất kỳ)
7. **KHÔNG TỰ Ý ĐỔI TIỀN TỐ** — mỗi thành viên có prefix riêng, Claude phải đọc từ `.env` để biết đang làm việc với ai

### ✅ QUY TRÌNH BẮT BUỘC TRƯỚC KHI THAY ĐỔI

**Bước 1: PREVIEW** - Luôn show cho user biết sẽ làm gì:
```
📋 PREVIEW THAY ĐỔI:
- File: backend/app/models/nqt_hoi_vien.py
- Hành động: Thêm method nqt_lay_theo_email()
- Dòng ảnh hưởng: 45-60
- Lý do: User yêu cầu thêm chức năng tìm hội viên theo email
```

**Bước 2: CHỜ XÁC NHẬN** - Đợi user đồng ý trước khi thực hiện

**Bước 3: THỰC HIỆN** - Chỉ sửa đúng phần đã preview

### 🔒 CÁC HÀNH ĐỘNG CẦN XÁC NHẬN

| Hành động | Mức độ | Yêu cầu |
|-----------|--------|---------|
| Tạo file mới | 🟡 Thấp | Preview tên + nội dung tóm tắt |
| Sửa file (< 20 dòng) | 🟡 Thấp | Preview diff |
| Sửa file (> 20 dòng) | 🟠 Trung bình | Preview chi tiết + xác nhận |
| Xoá file/folder | 🔴 Cao | **BẮT BUỘC** xác nhận rõ ràng |
| Đổi tên file/folder | 🔴 Cao | **BẮT BUỘC** xác nhận rõ ràng |
| Chạy migration DB | 🔴 Cao | **BẮT BUỘC** xác nhận rõ ràng |
| Git push/reset | 🔴 Cao | **BẮT BUỘC** xác nhận rõ ràng |

### 📝 FORMAT PREVIEW CHUẨN

```markdown
## 📋 PREVIEW THAY ĐỔI

### Tổng quan
- **Số file thay đổi**: 2
- **Số file tạo mới**: 1
- **Số file xoá**: 0

### Chi tiết

#### 1. ✏️ SỬA: `backend/app/models/nqt_hoi_vien.py`
- Dòng 45-60: Thêm method `nqt_lay_theo_email()`
```python
def nqt_lay_theo_email(self, nqt_email: str):
    return self.query.filter_by(nqt_email=nqt_email).first()
```

#### 2. ➕ TẠO MỚI: `backend/app/services/nqt_dich_vu_email.py`
- Mục đích: Service gửi email thông báo
- Nội dung: Class NqtDichVuEmail với các method gửi mail

---
⚠️ **Xác nhận để tiếp tục? (yes/no)**
```

### 🛡️ BACKUP RULE

Trước khi sửa file quan trọng (models, config, database), luôn suggest:
```bash
# Backup trước khi sửa
cp ten_file.py ten_file.py.backup
```

---

## Project Overview
- **Project**: Website Quản Lý Phòng Gym (Fitness SaaS - B2B)
- **Author Prefix**: đọc từ `.env` → `AUTHOR_PREFIX`
- **Architecture**: Client-Server (RESTful API), MVC Pattern
- **Backend**: Python Flask
- **Frontend**: HTML5, TailwindCSS, JavaScript (ES6+), Node.js (build tools), ReUI
- **Database**: SQL Server

## QUY TẮC ĐẶT TÊN BẮT BUỘC (TIỀN TỐ THEO THÀNH VIÊN)

### 🔑 Đọc tiền tố từ .env

Claude **PHẢI** đọc file `.env` để xác định tiền tố của người đang làm việc:

```env
# .env
AUTHOR_PREFIX=nqt   # ← Mỗi thành viên tự đặt prefix của mình
```

| Thành viên | AUTHOR_PREFIX | Ví dụ |
|------------|--------------|-------|
| Nguyễn Quốc Thắng | `nqt` | `nqt_ho_ten`, `NqtHoiVien` |
| Nguyễn Xuân Việt | `nxv` | `nxv_ho_ten`, `NxvSanPham` |
| (thành viên khác) | `abc` | `abc_ho_ten`, `AbcXxx` |

> **Khi tạo code mới**: dùng đúng `AUTHOR_PREFIX` từ `.env`
> **Khi sửa code cũ**: giữ nguyên tiền tố gốc, KHÔNG đổi dù prefix khác với `.env`

### Nguyên tắc cốt lõi
**Tiền tố = dấu hiệu nhận diện phần việc của từng người.** Code đã tồn tại (bất kể tiền tố gì) — KHÔNG được đổi tên.

### ⚠️ KHÔNG SỬA tiền tố của người khác
- Nếu gặp code có tiền tố **khác** với `AUTHOR_PREFIX` trong `.env` — **KHÔNG được đổi tên**, đó là phần thành viên khác đã làm.
- Chỉ áp dụng `AUTHOR_PREFIX` cho code **mới tạo** hoặc code **chưa có tiền tố nào**.
- Khi sửa file của người khác: chỉ sửa **logic bên trong**, giữ nguyên toàn bộ tên biến/hàm/class/bảng của họ.

```python
# ✅ ĐÚNG - Giữ nguyên tiền tố người khác
vtq_tinh_gia()          # của vtq → KHÔNG đổi
pnm_goi_email()         # của pnm → KHÔNG đổi
nqt_tao_hoi_vien()      # của nqt → đây là phần của mình

# ❌ SAI
nqt_tinh_gia()          # Đổi tên hàm của vtq → VI PHẠM!
```

### Python (snake_case với tiền tố nqt_)
```python
# ✅ ĐÚNG
nqt_hoi_vien = None
nqt_danh_sach_goi_tap = []
nqt_so_ngay_nhac_truoc = 3

def nqt_lay_thong_tin_hoi_vien(nqt_ma_hoi_vien: int):
    pass

def nqt_kiem_tra_goi_tap_het_han():
    pass

def nqt_tinh_tong_doanh_thu(nqt_ngay_bat_dau, nqt_ngay_ket_thuc):
    pass

class NqtDichVuCauHinh:
    pass

class NqtHoiVien(db.Model):
    pass

# ❌ SAI - Thiếu tiền tố nqt
hoi_vien = None  # SAI!
def lay_thong_tin():  # SAI!
class HoiVien:  # SAI!
```

### JavaScript (camelCase với tiền tố nqt)
```javascript
// ✅ ĐÚNG
let nqtHoiVien = null;
let nqtDanhSachGoiTap = [];
const nqtSoNgayNhacTruoc = 3;

function nqtLayThongTinHoiVien(nqtMaHoiVien) {}
async function nqtKiemTraGoiTapHetHan() {}
class NqtQuanLyCauHinh {}

// ❌ SAI
let hoiVien = null;  // SAI!
function layThongTin() {}  // SAI!
```

### Database Tables (PascalCase với tiền tố G6)
```sql
-- ✅ ĐÚNG
G6HoiVien, G6GoiTap, G6LichDat, G6CauHinh, G6NhanVien, G6ThietBi

-- ❌ SAI
HoiVien, GoiTap          -- SAI! Thiếu tiền tố G6
NqtHoiVien, NxvGoiTap   -- SAI! Dùng tiền tố thành viên cho DB
```

### Database Columns (snake_case với tiền tố g6_)
```sql
-- ✅ ĐÚNG
g6_ma_hoi_vien, g6_ho_ten, g6_ngay_sinh, g6_ngay_tao, g6_ngay_cap_nhat

-- ❌ SAI
ma_hoi_vien, ho_ten  -- SAI! Thiếu tiền tố g6_
nqt_ho_ten           -- SAI! Dùng tiền tố thành viên cho cột DB
```

### API Routes
```python
# ✅ ĐÚNG
nqt_hoi_vien_bp = Blueprint('nqt_hoi_vien', __name__)

@nqt_hoi_vien_bp.route('/nqt-hoi-vien', methods=['GET'])
def nqt_lay_tat_ca_hoi_vien():
    pass
```

### Từ điển thuật ngữ tiếng Việt chuẩn

| Tiếng Anh | Tiếng Việt (snake_case) | Tiếng Việt (camelCase) |
|-----------|-------------------------|------------------------|
| member | nqt_hoi_vien | nqtHoiVien |
| package | nqt_goi_tap | nqtGoiTap |
| booking | nqt_lich_dat | nqtLichDat |
| trainer/PT | nqt_huan_luyen_vien | nqtHuanLuyenVien |
| equipment | nqt_thiet_bi | nqtThietBi |
| config | nqt_cau_hinh | nqtCauHinh |
| check-in | nqt_diem_danh | nqtDiemDanh |
| payment | nqt_thanh_toan | nqtThanhToan |
| revenue | nqt_doanh_thu | nqtDoanhThu |
| schedule | nqt_lich_trinh | nqtLichTrinh |
| class | nqt_lop_hoc | nqtLopHoc |
| body metric | nqt_chi_so_co_the | nqtChiSoCoThe |
| weight | nqt_can_nang | nqtCanNang |
| body fat | nqt_ti_le_mo | nqtTiLeMo |
| muscle mass | nqt_ti_le_co | nqtTiLeCo |
| expiry date | nqt_ngay_het_han | nqtNgayHetHan |
| create | nqt_tao | nqtTao |
| update | nqt_cap_nhat | nqtCapNhat |
| delete | nqt_xoa | nqtXoa |
| get/fetch | nqt_lay | nqtLay |
| check | nqt_kiem_tra | nqtKiemTra |
| validate | nqt_xac_thuc | nqtXacThuc |
| calculate | nqt_tinh | nqtTinh |
| send | nqt_gui | nqtGui |
| list | nqt_danh_sach | nqtDanhSach |
| detail | nqt_chi_tiet | nqtChiTiet |
| search | nqt_tim_kiem | nqtTimKiem |
| filter | nqt_loc | nqtLoc |
| sort | nqt_sap_xep | nqtSapXep |
| export | nqt_xuat | nqtXuat |
| import | nqt_nhap | nqtNhap |
| report | nqt_bao_cao | nqtBaoCao |
| notification | nqt_thong_bao | nqtThongBao |
| reminder | nqt_nhac_nho | nqtNhacNho |
| user | nqt_nguoi_dung | nqtNguoiDung |
| admin | nqt_quan_tri | nqtQuanTri |
| role | nqt_vai_tro | nqtVaiTro |
| permission | nqt_quyen | nqtQuyen |
| login | nqt_dang_nhap | nqtDangNhap |
| logout | nqt_dang_xuat | nqtDangXuat |
| register | nqt_dang_ky | nqtDangKy |
| password | nqt_mat_khau | nqtMatKhau |
| token | nqt_ma_xac_thuc | nqtMaXacThuc |
| session | nqt_phien | nqtPhien |
| error | nqt_loi | nqtLoi |
| success | nqt_thanh_cong | nqtThanhCong |
| message | nqt_thong_diep | nqtThongDiep |
| status | nqt_trang_thai | nqtTrangThai |
| active | nqt_hoat_dong | nqtHoatDong |
| inactive | nqt_khong_hoat_dong | nqtKhongHoatDong |
| total | nqt_tong | nqtTong |
| count | nqt_so_luong | nqtSoLuong |
| price | nqt_gia | nqtGia |
| duration | nqt_thoi_luong | nqtThoiLuong |
| start time | nqt_thoi_gian_bat_dau | nqtThoiGianBatDau |
| end time | nqt_thoi_gian_ket_thuc | nqtThoiGianKetThuc |
| date | nqt_ngay | nqtNgay |
| time | nqt_gio | nqtGio |
| today | nqt_hom_nay | nqtHomNay |
| tomorrow | nqt_ngay_mai | nqtNgayMai |
| yesterday | nqt_hom_qua | nqtHomQua |
| week | nqt_tuan | nqtTuan |
| month | nqt_thang | nqtThang |
| year | nqt_nam | nqtNam |
| service | nqt_dich_vu | nqtDichVu |
| product | nqt_san_pham | nqtSanPham |
| order | nqt_don_hang | nqtDonHang |
| cart | nqt_gio_hang | nqtGioHang |
| invoice | nqt_hoa_don | nqtHoaDon |
| receipt | nqt_bien_lai | nqtBienLai |
| discount | nqt_giam_gia | nqtGiamGia |
| promotion | nqt_khuyen_mai | nqtKhuyenMai |

## QUAN TRỌNG: Dynamic Configuration (Không Hardcode)

### Nguyên tắc cốt lõi
**KHÔNG BAO GIỜ hardcode các giá trị cấu hình.** Tất cả settings phải được lưu trong database và có thể chỉnh sửa qua Admin Panel.

### Cách implement
```python
# ✅ ĐÚNG - Lấy từ database với tiền tố nqt
nqt_cau_hinh = NqtDichVuCauHinh.nqt_lay('nqt_so_ngay_nhac_truoc', mac_dinh=3)

# ❌ SAI - Hardcode
NQT_SO_NGAY_NHAC = 3  # KHÔNG LÀM THẾ NÀY
```

### Các loại cấu hình phải dynamic:
1. **Website Settings**: Tên, logo, favicon, liên hệ, social media, footer
2. **Business Settings**: Giờ mở/đóng cửa, booking rules, sức chứa
3. **Security Settings**: JWT expiry, login attempts, password policy
4. **Email Settings**: SMTP, templates, sender
5. **Payment Settings**: Gateway, currency, tax
6. **Theme Settings**: Colors, fonts, dark mode

## Tech Stack Requirements

### Backend (Flask API)
- Flask-RESTful for API endpoints
- Flask-SQLAlchemy for ORM with SQL Server
- Flask-JWT-Extended for authentication
- Flask-Mail for email notifications
- APScheduler or Celery for background jobs

### Frontend
- **TailwindCSS** for responsive UI (thay thế Bootstrap 5)
- **Node.js + npm** cho build tools (Tailwind CLI, bundler)
- Vanilla JavaScript (ES6+)
- Chart.js for data visualization
- QR code library for check-in

### Node.js / Tailwind setup
```bash
# Khởi tạo (chạy 1 lần)
npm init -y
npm install -D tailwindcss
npx tailwindcss init

# Build CSS (dev)
npx tailwindcss -i ./frontend/static/css/input.css -o ./frontend/static/css/output.css --watch

# Build CSS (production)
npx tailwindcss -i ./frontend/static/css/input.css -o ./frontend/static/css/output.css --minify
```

### Cấu trúc Tailwind
```
/frontend
  /static
    /css
      input.css      # @tailwind directives
      output.css     # Generated (gitignore)
    /js
    /images
  /templates
tailwind.config.js
package.json
```

> ⚠️ `output.css` và `node_modules/` phải có trong `.gitignore`

## Project Structure
```
/backend
  /app
    /models        # NqtHoiVien, NqtGoiTap, NqtCauHinh...
    /routes        # nqt_hoi_vien_bp, nqt_goi_tap_bp...
    /services      # NqtDichVuCauHinh, NqtDichVuHoiVien...
    /utils         # nqt_xac_thuc, nqt_ma_hoa...
    /jobs          # nqt_kiem_tra_het_han, nqt_gui_email...
  config.py
  run.py

/frontend
  /static
    /css
      input.css        # @tailwind base/components/utilities
      output.css       # Generated - KHÔNG commit
    /js                # nqtQuanLyCauHinh.js, nqtHoiVien.js...
    /images
  /templates

tailwind.config.js
package.json
node_modules/          # KHÔNG commit
```

## Role-Based Access Control (RBAC)
- **NqtQuanTri (Admin)**: Full system access, **QUẢN LÝ TẤT CẢ CẤU HÌNH**
- **NqtQuanLy (Manager)**: Manage members, PT, equipment, packages
- **NqtHuanLuyenVien (PT)**: View schedule, manage assigned members
- **NqtHoiVien (Member)**: Book sessions, track progress

## API Response Format
```json
{
  "nqt_thanh_cong": true,
  "nqt_du_lieu": {},
  "nqt_thong_diep": "Thành công",
  "nqt_loi": []
}
```

## Security Checklist
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF tokens for forms
- [ ] Rate limiting on auth endpoints
- [ ] Secure password storage (bcrypt)
- [ ] HTTPS only in production

## 📷 QUY TẮC UPLOAD HÌNH ẢNH

### Nguyên tắc cốt lõi
**KHÔNG SỬ DỤNG URL HÌNH ẢNH BÊN NGOÀI.** Tất cả hình ảnh (avatar, ảnh sản phẩm, logo, v.v.) phải được upload lên server và lưu đường dẫn local.

### Cách implement
```python
# ✅ ĐÚNG - Lưu đường dẫn local
nqt_anh_dai_dien = "/uploads/avatars/user_123.jpg"
nqt_anh_san_pham = "/uploads/products/goi_tap_001.png"

# ❌ SAI - URL bên ngoài
nqt_anh_dai_dien = "https://example.com/avatar.jpg"  # KHÔNG!
nqt_anh_dai_dien = "https://placehold.co/200x200"    # KHÔNG!
```

### Cấu trúc thư mục uploads
```
/frontend
  /static
    /uploads
      /avatars       # Avatar người dùng, hội viên
      /products      # Ảnh sản phẩm, gói tập
      /branches      # Ảnh chi nhánh
      /equipment     # Ảnh thiết bị
      /temp          # Upload tạm (xoá sau 24h)
```

### Quy tắc đặt tên file
- Format: `{loai}_{ma}_{timestamp}.{ext}`
- Ví dụ: `avatar_hv_001_1713024000.jpg`, `product_gt_005_1713024000.png`
- Chỉ chấp nhận: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`
- Giới hạn dung lượng: 5MB/file

### API Upload
```python
@nqt_upload_bp.route('/nqt-upload', methods=['POST'])
def nqt_upload_hinh_anh():
    # Validate file type, size
    # Save to /uploads/{category}/
    # Return local path
    return {"nqt_duong_dan": "/uploads/avatars/file.jpg"}
```

## Common Commands
```bash
# Run Flask server
flask run --debug

# Database migrations
flask db init
flask db migrate -m "message"
flask db upgrade

# Run tests
pytest

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies (Tailwind)
npm install

# Build Tailwind CSS (dev - watch mode)
npm run dev

# Build Tailwind CSS (production)
npm run build
```
