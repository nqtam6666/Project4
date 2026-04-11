# NQT - Booking Conflict Checker

Kiểm tra xung đột lịch đặt PT và lớp học. Tất cả tên theo tiền tố **nqt**.

## Usage
/booking-check

**QUAN TRỌNG**: Tất cả validation rules lấy từ `NqtDichVuCauHinh`, KHÔNG hardcode!

## Conflict Detection Logic

```python
# app/services/nqt_dich_vu_dat_lich.py
from datetime import datetime
from app.services.nqt_dich_vu_cau_hinh import NqtDichVuCauHinh

def nqt_kiem_tra_xung_dot_lich(
    nqt_ma_hlt: int,
    nqt_thoi_gian_bat_dau: datetime,
    nqt_thoi_gian_ket_thuc: datetime,
    nqt_ma_phong: int = None
) -> tuple[bool, list, list]:
    """
    Kiểm tra xung đột lịch đặt.
    Returns: (nqt_co_the_dat, nqt_danh_sach_xung_dot, nqt_goi_y_gio_khac)
    """
    # 1. Kiểm tra lịch của huấn luyện viên
    nqt_lich_hlt = nqt_lay_lich_huan_luyen_vien(nqt_ma_hlt, nqt_thoi_gian_bat_dau.date())

    # 2. Kiểm tra trùng giờ
    for nqt_lich in nqt_lich_hlt:
        if nqt_kiem_tra_trung_gio(nqt_lich, nqt_thoi_gian_bat_dau, nqt_thoi_gian_ket_thuc):
            return False, [nqt_lich], nqt_goi_y_gio_trong(nqt_ma_hlt, nqt_thoi_gian_bat_dau)

    # 3. Kiểm tra sức chứa phòng tập
    if nqt_ma_phong:
        nqt_dat_lich_phong   = nqt_lay_lich_phong(nqt_ma_phong, nqt_thoi_gian_bat_dau, nqt_thoi_gian_ket_thuc)
        nqt_phong            = nqt_lay_thong_tin_phong(nqt_ma_phong)
        nqt_suc_chua_toi_da  = NqtDichVuCauHinh.nqt_lay('nqt_suc_chua_toi_da_phong', mac_dinh=100)

        if len(nqt_dat_lich_phong) >= nqt_suc_chua_toi_da:
            return False, [], nqt_goi_y_gio_trong(nqt_ma_hlt, nqt_thoi_gian_bat_dau)

    return True, [], []


def nqt_kiem_tra_trung_gio(nqt_lich, nqt_bat_dau: datetime, nqt_ket_thuc: datetime) -> bool:
    """Trả về True nếu hai khoảng giờ bị trùng."""
    return not (nqt_lich.nqt_thoi_gian_ket_thuc <= nqt_bat_dau
                or nqt_lich.nqt_thoi_gian_bat_dau >= nqt_ket_thuc)
```

## Validation Rules (TẤT CẢ TỪ CONFIG)

```python
def nqt_xac_thuc_yeu_cau_dat_lich(
    nqt_thoi_gian_bat_dau: datetime,
    nqt_thoi_gian_ket_thuc: datetime,
    nqt_ma_hoi_vien: int
) -> tuple[bool, list]:
    """Xác thực yêu cầu đặt lịch theo rules từ database."""

    nqt_danh_sach_loi = []

    # ✅ Lấy từ ConfigService - KHÔNG hardcode
    nqt_thoi_luong_toi_thieu = NqtDichVuCauHinh.nqt_lay('nqt_thoi_luong_dat_lich_toi_thieu', mac_dinh=30)
    nqt_thoi_luong_toi_da    = NqtDichVuCauHinh.nqt_lay('nqt_thoi_luong_dat_lich_toi_da',    mac_dinh=120)
    nqt_so_ngay_dat_truoc    = NqtDichVuCauHinh.nqt_lay('nqt_so_ngay_dat_truoc_toi_da',      mac_dinh=30)
    nqt_gio_mo_cua           = NqtDichVuCauHinh.nqt_lay('nqt_gio_mo_cua',                    mac_dinh='06:00')
    nqt_gio_dong_cua         = NqtDichVuCauHinh.nqt_lay('nqt_gio_dong_cua',                  mac_dinh='22:00')

    # ❌ SAI - KHÔNG làm thế này
    # NQT_THOI_LUONG_TOI_THIEU = 30  # HARDCODE!

    nqt_thoi_luong_phut = (nqt_thoi_gian_ket_thuc - nqt_thoi_gian_bat_dau).total_seconds() / 60

    if nqt_thoi_luong_phut < nqt_thoi_luong_toi_thieu:
        nqt_danh_sach_loi.append(f'Thời gian tối thiểu {nqt_thoi_luong_toi_thieu} phút')
    if nqt_thoi_luong_phut > nqt_thoi_luong_toi_da:
        nqt_danh_sach_loi.append(f'Thời gian tối đa {nqt_thoi_luong_toi_da} phút')

    nqt_so_ngay_truoc = (nqt_thoi_gian_bat_dau.date() - datetime.now().date()).days
    if nqt_so_ngay_truoc > nqt_so_ngay_dat_truoc:
        nqt_danh_sach_loi.append(f'Chỉ được đặt trước tối đa {nqt_so_ngay_dat_truoc} ngày')
    if nqt_so_ngay_truoc < 0:
        nqt_danh_sach_loi.append('Không thể đặt lịch trong quá khứ')

    nqt_gio_mo   = datetime.strptime(nqt_gio_mo_cua,   '%H:%M').time()
    nqt_gio_dong = datetime.strptime(nqt_gio_dong_cua, '%H:%M').time()
    if nqt_thoi_gian_bat_dau.time() < nqt_gio_mo or nqt_thoi_gian_ket_thuc.time() > nqt_gio_dong:
        nqt_danh_sach_loi.append(f'Phòng gym mở cửa {nqt_gio_mo_cua} – {nqt_gio_dong_cua}')

    if not nqt_kiem_tra_goi_tap_con_han(nqt_ma_hoi_vien):
        nqt_danh_sach_loi.append('Hội viên chưa có gói tập đang hoạt động')

    return len(nqt_danh_sach_loi) == 0, nqt_danh_sach_loi
```

## Config Keys cần thiết
| Config Key | Type | Mô tả |
|---|---|---|
| `nqt_thoi_luong_dat_lich_toi_thieu` | integer | Thời gian tối thiểu (phút) |
| `nqt_thoi_luong_dat_lich_toi_da`    | integer | Thời gian tối đa (phút) |
| `nqt_so_ngay_dat_truoc_toi_da`      | integer | Đặt trước tối đa (ngày) |
| `nqt_gio_mo_cua`                    | string  | Giờ mở cửa (HH:MM) |
| `nqt_gio_dong_cua`                  | string  | Giờ đóng cửa (HH:MM) |
| `nqt_suc_chua_toi_da_phong`         | integer | Sức chứa tối đa |
