# models package — re-export all for Alembic detection
from backend.app.models.nqt_cau_hinh import NqtCauHinh  # noqa: F401
from backend.app.models.nqt_nguoi_dung import (  # noqa: F401
    NqtVaiTro, NqtQuyenHan, NqtNguoiDungVaiTro, NqtVaiTroQuyen, NqtNguoiDung,
)
from backend.app.models.nqt_chi_nhanh import NqtChiNhanh, NqtThietBi  # noqa: F401
from backend.app.models.nqt_nhan_vien import NqtNhanVien, NqtLichLamViec  # noqa: F401
from backend.app.models.nqt_hoi_vien import (  # noqa: F401
    NqtHoiVien, NqtGoiTap, NqtDangKyGoiTap, NqtDiemDanh, NqtChiSoCoThe,
)
from backend.app.models.nqt_khach_hang import (  # noqa: F401
    NqtKhachHang, NqtDiaChiGiaoHang, NqtHangThanhVien, NqtDiemKhachHang, NqtGiaoDichDiem,
)
from backend.app.models.nqt_don_hang import (  # noqa: F401
    NqtGioHang, NqtChiTietGioHang, NqtDonHang, NqtChiTietDonHang, NqtLichSuDonHang,
)
from backend.app.models.nqt_khuyen_mai import NqtMaGiamGia, NqtKhuyenMaiMuaKem, NqtBanner  # noqa: F401
from backend.app.models.nqt_thanh_toan import NqtThanhToan, NqtHoaDon  # noqa: F401
from backend.app.models.nqt_van_chuyen import NqtDonViVanChuyen, NqtVungVanChuyen  # noqa: F401
from backend.app.models.nqt_blog import NqtDanhMucBaiViet, NqtBaiViet, NqtDanhGiaSanPham  # noqa: F401
from backend.app.models.nqt_thong_bao import NqtThongBao, NqtLichGuiThongBao  # noqa: F401
from backend.app.models.nqt_xac_thuc import NqtOtpXacThuc, NqtPhienDangNhap, NqtNhatKyHoatDong  # noqa: F401
