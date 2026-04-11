# NQT - Background Job Generator

Tạo scheduled tasks và cron jobs cho hệ thống gym. Tất cả tên theo tiền tố **nqt**.

## Usage
/cron-job <loai_cong_viec>

**QUAN TRỌNG**: Tất cả giá trị config lấy từ `NqtDichVuCauHinh`, KHÔNG hardcode!

## Job Types

### 1. nqt-kiem-tra-het-han
Quét gói tập sắp hết hạn và gửi email thông báo.

```python
# app/jobs/nqt_kiem_tra_het_han.py
from datetime import datetime, timedelta
from app.services.nqt_dich_vu_cau_hinh import NqtDichVuCauHinh
from app.services.nqt_dich_vu_email    import NqtDichVuEmail
from app.models.nqt_goi_tap            import NqtGoiTap
from app.models.nqt_hoi_vien           import NqtHoiVien

def nqt_kiem_tra_goi_tap_sap_het_han():
    """Chạy hàng ngày - giờ chạy lấy từ config"""

    nqt_hom_nay       = datetime.now().date()

    # ✅ Lấy từ config - KHÔNG hardcode
    nqt_so_ngay_nhac  = NqtDichVuCauHinh.nqt_lay('nqt_so_ngay_nhac_truoc_het_han', mac_dinh=3)
    nqt_ngay_canh_bao = nqt_hom_nay + timedelta(days=nqt_so_ngay_nhac)

    # ❌ SAI
    # nqt_ngay_canh_bao = nqt_hom_nay + timedelta(days=3)  # HARDCODE!

    nqt_danh_sach_sap_het = NqtGoiTap.query.filter(
        NqtGoiTap.nqt_ngay_het_han == nqt_ngay_canh_bao,
        NqtGoiTap.nqt_trang_thai   == True
    ).all()

    for nqt_goi in nqt_danh_sach_sap_het:
        nqt_hoi_vien = NqtHoiVien.query.get(nqt_goi.nqt_ma_hoi_vien)
        NqtDichVuEmail.nqt_gui_nhac_het_han(nqt_hoi_vien.nqt_email, nqt_goi)
```

### 2. nqt-gia-han-tu-dong
Xử lý thanh toán gia hạn tự động.

```python
# app/jobs/nqt_gia_han_tu_dong.py
def nqt_xu_ly_gia_han_tu_dong():
    """Chạy hàng ngày lúc 00:05"""

    nqt_hom_nay = datetime.now().date()

    nqt_danh_sach_can_gia_han = NqtGoiTap.query.filter(
        NqtGoiTap.nqt_ngay_het_han == nqt_hom_nay,
        NqtGoiTap.nqt_tu_dong_gia_han == True,
        NqtGoiTap.nqt_trang_thai == True
    ).all()

    for nqt_goi in nqt_danh_sach_can_gia_han:
        try:
            nqt_ket_qua = nqt_cong_thanh_toan.nqt_thu_tien(
                nqt_goi.nqt_ma_hoi_vien, nqt_goi.nqt_gia
            )
            if nqt_ket_qua.nqt_thanh_cong:
                nqt_gia_han_goi_tap(nqt_goi)
                NqtDichVuEmail.nqt_gui_xac_nhan_gia_han(nqt_goi)
            else:
                NqtDichVuEmail.nqt_gui_thanh_toan_that_bai(nqt_goi)
        except Exception as nqt_loi:
            nqt_ghi_log_loi(nqt_loi)
```

### 3. nqt-bao-cao-diem-danh
Tạo báo cáo điểm danh hàng ngày.

```python
# app/jobs/nqt_bao_cao_diem_danh.py
def nqt_tao_bao_cao_diem_danh_hang_ngay():
    """Chạy mỗi ngày lúc 23:00"""

    nqt_hom_nay = datetime.now().date()

    nqt_danh_sach_diem_danh = NqtDiemDanh.query.filter(
        func.date(NqtDiemDanh.nqt_thoi_gian_vao) == nqt_hom_nay
    ).all()

    nqt_bao_cao = {
        'nqt_ngay':              nqt_hom_nay,
        'nqt_tong_luot_vao':     len(nqt_danh_sach_diem_danh),
        'nqt_gio_cao_diem':      nqt_tinh_gio_cao_diem(nqt_danh_sach_diem_danh),
        'nqt_hoi_vien_duy_nhat': len(set(dd.nqt_ma_hoi_vien for dd in nqt_danh_sach_diem_danh))
    }

    nqt_luu_bao_cao(nqt_bao_cao)
    nqt_thong_bao_quan_ly(nqt_bao_cao)
```

## Scheduler Setup

```python
# app/__init__.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.nqt_dich_vu_cau_hinh import NqtDichVuCauHinh

def nqt_khoi_tao_scheduler():
    nqt_scheduler = BackgroundScheduler()

    # Lấy giờ chạy từ config - KHÔNG hardcode
    nqt_gio_kiem_tra  = NqtDichVuCauHinh.nqt_lay('nqt_gio_kiem_tra_het_han',  mac_dinh=8)
    nqt_phut_kiem_tra = NqtDichVuCauHinh.nqt_lay('nqt_phut_kiem_tra_het_han', mac_dinh=0)

    from app.jobs.nqt_kiem_tra_het_han  import nqt_kiem_tra_goi_tap_sap_het_han
    from app.jobs.nqt_gia_han_tu_dong   import nqt_xu_ly_gia_han_tu_dong
    from app.jobs.nqt_bao_cao_diem_danh import nqt_tao_bao_cao_diem_danh_hang_ngay

    nqt_scheduler.add_job(nqt_kiem_tra_goi_tap_sap_het_han,    'cron', hour=nqt_gio_kiem_tra, minute=nqt_phut_kiem_tra)
    nqt_scheduler.add_job(nqt_xu_ly_gia_han_tu_dong,           'cron', hour=0,  minute=5)
    nqt_scheduler.add_job(nqt_tao_bao_cao_diem_danh_hang_ngay, 'cron', hour=23, minute=0)

    nqt_scheduler.start()
    return nqt_scheduler
```
