# NQT Gym Management System - Project Rules

## Project Overview
- **Project**: Website Quản Lý Phòng Gym (Fitness SaaS - B2B)
- **Author Prefix**: `nqt` (bắt buộc cho tất cả tên biến, hàm, class)
- **Architecture**: Client-Server (RESTful API), MVC Pattern
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQL Server

## QUY TẮC ĐẶT TÊN BẮT BUỘC (TIỀN TỐ "nqt")

### Nguyên tắc cốt lõi
**TẤT CẢ tên biến, hàm, class, table PHẢI có tiền tố "nqt"** - viết theo phong cách clean code tiếng Việt.

### ⚠️ KHÔNG SỬA tiền tố của người khác
- Nếu gặp code có tiền tố **khác** `nqt` (ví dụ: `abc_`, `vtq_`, `pnm_`...) — **KHÔNG được đổi**, đó là phần thành viên khác trong nhóm đã làm và muốn đánh dấu phần việc của họ.
- Chỉ áp dụng tiền tố `nqt_` cho code **mới tạo** hoặc code **chưa có tiền tố nào**.
- Khi sửa file của người khác: chỉ sửa logic, giữ nguyên toàn bộ tên biến/hàm/class của họ.

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

### Database Tables (PascalCase với tiền tố Nqt)
```sql
-- ✅ ĐÚNG
NqtHoiVien, NqtGoiTap, NqtLichDat, NqtCauHinh, NqtNhanVien, NqtThietBi

-- ❌ SAI
HoiVien, GoiTap  -- SAI! Thiếu tiền tố Nqt
```

### Database Columns (snake_case với tiền tố nqt_)
```sql
-- ✅ ĐÚNG
nqt_ma_hoi_vien, nqt_ho_ten, nqt_ngay_sinh, nqt_ngay_tao, nqt_ngay_cap_nhat

-- ❌ SAI
ma_hoi_vien, ho_ten  -- SAI! Thiếu tiền tố nqt_
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
- Bootstrap 5 for responsive UI
- Vanilla JavaScript (ES6+)
- Chart.js for data visualization
- QR code library for check-in

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
    /js            # nqtQuanLyCauHinh.js, nqtHoiVien.js...
    /images
  /templates
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

# Install dependencies
pip install -r requirements.txt
```
