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
- **Frontend**: Node.js + Vite, HTML5, TailwindCSS (CDN), JavaScript (ES6+ modules), Vanilla JS
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
| Nguyễn Quang Tâm | `nqt` | `nqt_ho_ten`, `NqtHoiVien` |
| Nguyễn Xuân Vinh | `nxv` | `nxv_ho_ten`, `NxvSanPham` |
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

### Database Soft Delete (XOÁ MỀM)

**Nguyên tắc cốt lõi**: Tất cả các bảng database phải có cột `g6_deleted_at` để hỗ trợ xoá mềm. **KHÔNG BAO GIỜ xoá vĩnh viễn dữ liệu** (hard delete).

```sql
-- ✅ ĐÚNG - Mỗi bảng phải có cột soft delete
g6_deleted_at DATETIME2 NULL DEFAULT NULL  -- NULL = chưa xoá, có giá trị = đã xoá

-- Ví dụ tạo bảng
CREATE TABLE G6HoiVien (
    g6_ma_hoi_vien INT PRIMARY KEY,
    g6_ho_ten NVARCHAR(100),
    g6_ngay_tao DATETIME2 DEFAULT GETDATE(),
    g6_ngay_cap_nhat DATETIME2,
    g6_deleted_at DATETIME2 NULL DEFAULT NULL  -- Cột soft delete BẮT BUỘC
);
```

```python
# ✅ ĐÚNG - Model Python
class NqtHoiVien(db.Model):
    # ... các cột khác
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

# ✅ ĐÚNG - Query lọc bỏ records đã xoá
def nqt_lay_tat_ca():
    return NqtHoiVien.query.filter(NqtHoiVien.g6_deleted_at == None).all()

# ✅ ĐÚNG - Soft delete
def nqt_xoa_mem(nqt_ma):
    hoi_vien = NqtHoiVien.query.get(nqt_ma)
    hoi_vien.g6_deleted_at = datetime.utcnow()
    db.session.commit()

# ❌ SAI - Hard delete
def nqt_xoa(nqt_ma):
    hoi_vien = NqtHoiVien.query.get(nqt_ma)
    db.session.delete(hoi_vien)  # KHÔNG LÀM THẾ NÀY!
```

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `g6_deleted_at` | `DATETIME2 NULL` | `NULL` = active, `timestamp` = đã xoá mềm |

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

### 🏗️ Kiến trúc: Flask API + Vite SPA (tách biệt)

**Backend**: Flask chỉ serve REST API (port 5000). **KHÔNG** serve HTML.
**Frontend**: Vite dev server (port 5173) serve toàn bộ HTML/JS/CSS, proxy `/api` → Flask.

```bash
# Chạy backend (terminal 1)
cd backend
flask run --debug

# Chạy frontend (terminal 2)
cd frontend
npm run dev
```

> ⚠️ **KHÔNG dùng Jinja2 templates.** Toàn bộ frontend (bao gồm Admin panel) đều là Vite static HTML. Thư mục `frontend/templates/admin/` là Jinja2 cũ — **KHÔNG SỬA, KHÔNG TẠO THÊM**. Tất cả trang admin mới phải là file `.html` trong `frontend/src/pages/admin/`.

### Backend (Flask — Python)
- Flask for REST API only (JSON responses)
- Flask-SQLAlchemy for ORM with SQL Server
- Flask-JWT-Extended for authentication
- Flask-Mail for email notifications
- APScheduler for background jobs
- Flask serve static files từ `frontend/static/uploads/` (uploaded images)

### Frontend (Vite + Vanilla JS)
- **Vite** — build tool + dev server (port 5173)
- **TailwindCSS CDN** — inline config mỗi trang (`<script src="https://cdn.tailwindcss.com?plugins=forms">`)
- **Vanilla JavaScript (ES6+ modules)** — import/export, không dùng framework
- **Chart.js** — data visualization (CDN)
- **JWT** lưu trong `localStorage` (`nqt_token`, `nqt_refresh_token`, `nqt_user`)
- Auth helpers: `nqtRequireAuth()`, `nqtApi()`, `nqtLogout()`, `nqtToast()` — từ `src/js/member/auth.js`

### Design System — Token chuẩn (DÙNG CHUNG CHO TẤT CẢ ZONE)

Token màu, font, icon được định nghĩa **một lần duy nhất** trong `frontend/src/js/nqtLayout.js` (`NQT_TW_CONFIG`).
**KHÔNG copy-paste inline config vào từng trang** — import và gán `tailwind.config = NQT_TW_CONFIG`.

```
Màu nền:    bg-main #0A0A0F | bg-card #12121A | bg-elevated #1C1C28
Accent:     neon-lime #C8F135 | neon-dim #A8D120
Text:       text-primary #F5F5F0 | text-secondary #A1A1AA | text-muted #52525B
Border:     border-subtle rgba(255,255,255,0.06) | border-neon rgba(200,241,53,0.3)
Status:     success #22C55E | error #EF4444 | warning #F59E0B | info #3B82F6

Font:       Inter (body, font-sans) | Space Grotesk (headings/labels, font-caps) | JetBrains Mono (số liệu, font-mono)
Icon:       Material Symbols Outlined (Google Fonts) — KHÔNG dùng Font Awesome cho trang mới
CDN TW:     https://cdn.tailwindcss.com?plugins=forms,container-queries (LUÔN có plugins suffix)
```

---

## 🗺️ UI ZONES — Phân vùng giao diện theo người dùng

Hệ thống có **5 zone** riêng biệt. Mỗi zone có layout, auth guard và sidebar khác nhau nhưng **CÙNG design token**.

### ZONE 1 — Landing / Public (`/`, `/src/pages/*.html`)
**Đối tượng:** Khách vãng lai chưa đăng nhập  
**Mục đích:** Giới thiệu dịch vụ, thu hút đăng ký  
**Layout:** Fixed navbar (`nqtRenderPublicNav`) + Footer (`nqtRenderFooter`) — KHÔNG có sidebar  
**Auth:** Không yêu cầu — truy cập tự do  
**Dark mode:** `<html class="dark">` hardcoded — luôn dark  
**Trang hiện có:** `index.html`, `goi-tap.html`, `huan-luyen-vien.html`, `lop-hoc.html`, `blog.html`, `blog-chi-tiet.html`, `su-kien.html`, `shop.html`, `shop-chi-tiet.html`

Navbar hiển thị nút **Đăng nhập** → redirect `/src/pages/member/login.html`  
Nút **Đăng ký** → redirect `/src/pages/member/register.html`  
Sau khi đăng nhập thành công → redirect về zone tương ứng với role.

---

### ZONE 2 — Auth (`/src/pages/member/login.html`, `/src/pages/member/register.html`)
**Đối tượng:** Bất kỳ ai cần xác thực  
**Mục đích:** Đăng nhập / Đăng ký tài khoản  
**Layout:** Full-screen centered form — KHÔNG có navbar, KHÔNG có sidebar  
**Auth:** Nếu đã có token hợp lệ → redirect ngay về zone đúng với role  
**Dark mode:** `<html class="dark">` hardcoded  
**Sau đăng nhập:** Đọc `role` trong JWT payload → redirect:
- `NqtHoiVien` → `/src/pages/member/dashboard.html`
- `NqtHuanLuyenVien` → `/src/pages/pt/dashboard.html` *(zone 4)*
- `NqtQuanLy` / `NqtQuanTri` / `NqtNhanVien` → `/src/pages/admin/dashboard.html` *(zone 5)*

---

### ZONE 3 — Member Portal (`/src/pages/member/*.html`)
**Đối tượng:** Hội viên đã đăng nhập  
**Mục đích:** Quản lý cá nhân — gói tập, điểm danh, lịch tập, chỉ số cơ thể  
**Layout:** Sidebar cố định trái (`nqtRenderSidebar`) — KHÔNG có public navbar  
**Auth guard:** `nqtRequireAuth()` — redirect về login nếu thiếu `nqt_token`  
**Token lưu:** `localStorage.nqt_token`, `nqt_refresh_token`, `nqt_user`  
**Dark mode:** `<html class="dark">` hardcoded  
**Sidebar label:** "Member Portal"  
**Trang:** dashboard, ho_so, goi-tap, diem-danh, chi-so, lich-tap, dich-vu, (shop/don-hang)

---

### ZONE 4 — PT Portal (`/src/pages/pt/*.html`) *(chưa có, tạo khi cần)*
**Đối tượng:** Huấn luyện viên (PT) đã đăng nhập  
**Mục đích:** Xem lịch dạy, quản lý học viên được giao, ghi chú buổi tập  
**Layout:** Sidebar riêng (tạo `nqtRenderPTSidebar`) — KHÔNG dùng sidebar của member  
**Auth guard:** Kiểm tra `nqt_token` + role `NqtHuanLuyenVien`  
**Token lưu:** Cùng key với member (`nqt_token`, `nqt_user`) — phân biệt qua `role` trong JWT  
**Dark mode:** `<html class="dark">` hardcoded  
**Sidebar label:** "PT Portal"

---

### ZONE 5 — Admin/Staff Panel (`/src/pages/admin/*.html`)
**Đối tượng:** Admin (`NqtQuanTri`), Quản lý (`NqtQuanLy`), Nhân viên (`NqtNhanVien`)  
**Mục đích:** Quản trị toàn hệ thống  
**Layout:** Admin shell — `nqtInitAdminLayout(activePage)` từ `nqtAdminLayout.js`  
**Auth guard:** Kiểm tra `localStorage.nqt_admin_token` + role hợp lệ  
**Token lưu:** `localStorage.nqt_admin_token` (tách biệt với member token)  
**Dark mode:** Toggle qua `localStorage.nqt_dark_mode`, apply class `dark` trên `<html>`  
**Icon:** Font Awesome 6 (đã dùng trong admin — giữ nguyên để không break)  
**Màu:** Cùng token `NQT_TW_CONFIG` nhưng light-mode-first (admin hỗ trợ cả light lẫn dark)  
**Sidebar label:** "Admin Panel"  
**URL:** `http://localhost:5173/src/pages/admin/dashboard.html`

---

### Bảng tóm tắt 5 Zone

| Zone | Folder | Auth token | Layout | Dark mode | Icon |
|------|--------|-----------|--------|-----------|------|
| Landing/Public | `src/pages/*.html` + `index.html` | Không cần | Navbar + Footer | Forced dark | Material Symbols |
| Auth | `src/pages/member/login.html` + `register.html` | Redirect nếu có | Full-screen form | Forced dark | Material Symbols |
| Member Portal | `src/pages/member/` | `nqt_token` | Sidebar (Member) | Forced dark | Material Symbols |
| PT Portal | `src/pages/pt/` | `nqt_token` + role PT | Sidebar (PT) | Forced dark | Material Symbols |
| Admin/Staff | `src/pages/admin/` | `nqt_admin_token` | Admin shell | Toggle (light/dark) | Font Awesome 6 |

---

### Luồng điều hướng Auth

```
Khách vãng lai
  → xem Landing/Public (zone 1)
  → click "Đăng nhập" / "Đăng ký"
  → vào trang Auth (zone 2)
  → nhập thông tin → gọi API login
  → nhận JWT → lưu token → đọc role
      ├── role = HoiVien    → redirect Member Portal (zone 3)
      ├── role = PT          → redirect PT Portal (zone 4)
      └── role = Admin/Staff → redirect Admin Panel (zone 5)
```

---

### Mockup reference
Canonical design token lấy từ `frontend/nqtam_design/` (4 file HTML) — KHÔNG sửa các file này.

### Cấu trúc project thực tế
```
frontend/
├── index.html                    # Landing page (Vite entry)
├── vite.config.js                # Đăng ký tất cả entry points tại đây
├── tailwind.config.js
├── package.json
├── src/
│   ├── css/input.css             # @tailwind directives (cho build)
│   ├── js/
│   │   ├── landing.js            # Landing page logic
│   │   └── member/
│   │       └── auth.js           # Shared auth helpers
│   └── pages/
│       ├── member/               # Trang hội viên (cần JWT)
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── dashboard.html
│       │   └── ho_so.html
│       ├── shop/                 # Trang shop/giỏ hàng
│       └── (public pages)        # Gói tập, HLV, blog, v.v.
├── nqtam_design/                 # Mockup reference (KHÔNG sửa)
│   ├── nqt_gym_homepage/code.html
│   ├── nqt_gym_membership_plans/code.html
│   ├── nqt_gym_trainers_classes/code.html
│   └── nqt_gym_contact_booking/code.html
├── templates/admin/              # Jinja2 cũ — KHÔNG SỬA, KHÔNG TẠO THÊM (đã migrate sang Vite)
└── static/
    └── uploads/                  # Ảnh upload (Flask serve tại /static/uploads/)
```

### Admin Panel (Vite)
Admin panel đã được migrate hoàn toàn sang Vite static HTML:
- Shared layout: `frontend/src/js/admin/nqtAdminLayout.js`
- Tất cả trang admin: `frontend/src/pages/admin/*.html`
- URL admin: `http://localhost:5173/src/pages/admin/dashboard.html`
- Auth guard được xử lý trong `nqtAdminLayout.js` (kiểm tra JWT `nqt_token`)

### Quy tắc thêm trang mới
Mỗi trang HTML mới **BẮT BUỘC** phải đăng ký trong `vite.config.js`:
```js
// vite.config.js
rollupOptions: {
  input: {
    main: resolve(__dirname, 'index.html'),
    memberLogin: resolve(__dirname, 'src/pages/member/login.html'),
    // ← Thêm entry mới ở đây
    goiTap: resolve(__dirname, 'src/pages/goi-tap.html'),
  }
}
```

## Role-Based Access Control (RBAC)

| Role | Tên | Zone | Quyền |
|------|-----|------|-------|
| `NqtQuanTri` | Admin | Zone 5 | Full system access, quản lý toàn bộ cấu hình |
| `NqtQuanLy` | Manager | Zone 5 | Quản lý hội viên, PT, thiết bị, gói tập |
| `NqtNhanVien` | Nhân viên (lễ tân...) | Zone 5 | Checkin, bán hàng, xem lịch |
| `NqtHuanLuyenVien` | PT | Zone 4 | Xem lịch dạy, quản lý học viên được giao |
| `NqtHoiVien` | Hội viên | Zone 3 | Đặt lịch, theo dõi tiến trình, mua gói |

> Role được lưu trong JWT payload. Sau đăng nhập, frontend đọc role để redirect đúng zone.

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
# Chạy backend (Flask API)
cd backend
pip install -r requirements.txt   # cài 1 lần
flask run --debug                  # port 5000

# Chạy frontend (Vite dev server)
cd frontend
npm install                        # cài 1 lần
npm run dev                        # port 5173

# Build frontend production
cd frontend
npm run build                      # output → frontend/dist/

# Database migrations
flask db init
flask db migrate -m "message"
flask db upgrade

# Seed dữ liệu
flask seed
flask seed-fresh                   # reset + seed lại

# Run tests
pytest
```
