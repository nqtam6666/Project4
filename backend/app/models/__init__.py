# models package — re-export all for Alembic detection
from backend.app.models.g6_cau_hinh import G6CauHinh  # noqa: F401
from backend.app.models.g6_nguoi_dung import (  # noqa: F401
    G6VaiTro, G6QuyenHan, G6NguoiDungVaiTro, G6VaiTroQuyen, G6NguoiDung,
)
from backend.app.models.g6_chi_nhanh import G6ChiNhanh, G6ThietBi  # noqa: F401
from backend.app.models.g6_nhan_vien import G6NhanVien, G6LichLamViec  # noqa: F401
from backend.app.models.g6_hoi_vien import (  # noqa: F401
    G6HoiVien, G6GoiTap, G6DangKyGoiTap, G6DiemDanh, G6ChiSoCoThe,
)
from backend.app.models.g6_khach_hang import (  # noqa: F401
    G6KhachHang, G6DiaChiGiaoHang, G6HangThanhVien, G6DiemKhachHang, G6GiaoDichDiem,
)
from backend.app.models.g6_don_hang import (  # noqa: F401
    G6GioHang, G6ChiTietGioHang, G6DonHang, G6ChiTietDonHang, G6LichSuDonHang,
)
from backend.app.models.g6_khuyen_mai import G6MaGiamGia, G6KhuyenMaiMuaKem, G6Banner  # noqa: F401
from backend.app.models.g6_thanh_toan import G6ThanhToan, G6HoaDon  # noqa: F401
from backend.app.models.g6_van_chuyen import G6DonViVanChuyen, G6VungVanChuyen  # noqa: F401
from backend.app.models.g6_blog import G6DanhMucBaiViet, G6BaiViet, G6DanhGiaSanPham  # noqa: F401
from backend.app.models.g6_thong_bao import G6ThongBao, G6LichGuiThongBao  # noqa: F401
from backend.app.models.g6_xac_thuc import G6OtpXacThuc, G6PhienDangNhap, G6NhatKyHoatDong  # noqa: F401
from backend.app.models.g6_huan_luyen_vien import (  # noqa: F401
    G6HuanLuyenVien, G6GoiPT, G6DangKyGoiPT, G6BuoiTapPT,
)
from backend.app.models.g6_lop_hoc import G6LopHoc, G6LichLopHoc, G6DatChoLopHoc  # noqa: F401
from backend.app.models.g6_dich_vu_phu import G6DichVuPhu, G6DatDichVu  # noqa: F401
from backend.app.models.g6_san_pham import (  # noqa: F401
    G6DanhMucSanPham, G6MucTieuSucKhoe, G6ThuongHieu,
    G6SanPham, G6BienTheSanPham, G6HinhAnhSanPham,
    G6ThanhPhanDinhDuong, G6ChungNhanSanPham,
    G6TonKho, G6LichSuTonKho,
)
