"""
Seed dữ liệu mẫu cho NQT Gym Management System.
Idempotent: mỗi nhóm kiểm tra xem đã có dữ liệu chưa trước khi insert.

Chạy qua Flask CLI:
    flask seed

Hoặc chạy trực tiếp:
    python -m backend.app.seeds.nqt_seed
"""

from datetime import date, time, datetime
import bcrypt



def nqt_chay_seed():
    from backend.app import db
    from backend.app.models.nqt_cau_hinh import NqtCauHinh
    from backend.app.models.nqt_nguoi_dung import (
        NqtVaiTro, NqtQuyenHan, NqtNguoiDung,
        NqtNguoiDungVaiTro, NqtVaiTroQuyen,
    )
    from backend.app.models.nqt_chi_nhanh import NqtChiNhanh, NqtThietBi
    from backend.app.models.nqt_nhan_vien import NqtNhanVien
    from backend.app.models.nqt_hoi_vien import NqtGoiTap, NqtHoiVien
    from backend.app.models.nqt_khach_hang import NqtHangThanhVien

    print("=== Bắt đầu seed dữ liệu ===")
    
    # Tạo bảng nếu chưa có (cần thiết khi chuyển sang DB mới)
    db.create_all()
    print("[INFO] Đã kiểm tra/tạo schema database")

    # ------------------------------------------------------------------
    # 1. NqtCauHinh
    # ------------------------------------------------------------------
    if NqtCauHinh.query.first():
        print("[SKIP] NqtCauHinh — đã có dữ liệu")
    else:
        nqt_danh_sach_cau_hinh = [
            # Nhóm: website
            ("ten_website",         "NQT Gym",                          "string",  "website",  "Tên website"),
            ("mo_ta_website",       "Hệ thống quản lý phòng gym NQT",   "string",  "website",  "Mô tả website"),
            ("logo_url",            "",                                 "string",  "website",  "URL logo website"),
            ("favicon_url",         "",                                 "string",  "website",  "URL favicon"),
            ("avatar_mac_dinh_url", "",                                 "string",  "website",  "URL avatar mặc định cho người dùng"),
            ("email_lien_he",       "contact@nqtgym.vn",                "string",  "website",  "Email liên hệ"),
            ("so_dien_thoai_lien_he", "1900 1234",                      "string",  "website",  "Hotline liên hệ"),
            ("dia_chi_tru_so",      "123 Cầu Giấy, Hà Nội",            "string",  "website",  "Địa chỉ trụ sở"),
            ("facebook_url",        "https://facebook.com/nqtgym",      "string",  "website",  "Link Facebook"),
            ("zalo_url",            "https://zalo.me/nqtgym",           "string",  "website",  "Link Zalo"),
            # Nhóm: business
            ("gio_mo_cua",          "05:00",                            "string",  "business", "Giờ mở cửa mặc định"),
            ("gio_dong_cua",        "23:00",                            "string",  "business", "Giờ đóng cửa mặc định"),
            ("so_ngay_nhac_het_han", "7",                               "integer", "business", "Số ngày nhắc trước khi gói hết hạn"),
            ("so_ngay_nhac_het_han_2", "3",                             "integer", "business", "Số ngày nhắc lần 2 trước khi gói hết hạn"),
            ("so_luot_checkin_ngay_mac_dinh", "1",                      "integer", "business", "Số lượt check-in tối đa mỗi ngày (mặc định)"),
            ("cho_phep_checkin_truoc_phut",   "15",                     "integer", "business", "Cho phép check-in trước N phút"),
            ("suc_chua_mac_dinh",   "100",                              "integer", "business", "Sức chứa mặc định mỗi chi nhánh"),
            # Nhóm: security
            ("jwt_expiry_giay",     "3600",                             "integer", "security", "JWT access token hết hạn sau N giây"),
            ("so_lan_sai_mat_khau", "5",                                "integer", "security", "Số lần sai mật khẩu trước khi khoá tài khoản"),
            ("thoi_gian_khoa_phut", "30",                               "integer", "security", "Khoá tài khoản trong N phút"),
            ("otp_het_han_phut",    "10",                               "integer", "security", "OTP hết hạn sau N phút"),
            # Nhóm: email
            ("smtp_host",           "smtp.gmail.com",                   "string",  "email",    "SMTP Server"),
            ("smtp_port",           "587",                              "integer", "email",    "SMTP Port"),
            ("smtp_bao_mat",        "tls",                              "string",  "email",    "Bảo mật: none/ssl/tls"),
            ("smtp_email",          "",                                 "string",  "email",    "Email đăng nhập SMTP"),
            ("smtp_mat_khau",       "",                                 "string",  "email",    "Mật khẩu ứng dụng SMTP"),
            ("email_gui_tu",        "no-reply@nqtgym.vn",               "string",  "email",    "Email gửi đi (From)"),
            ("ten_nguoi_gui_email", "NQT Gym",                          "string",  "email",    "Tên hiển thị người gửi"),
            ("email_cc_mac_dinh",   "",                                 "string",  "email",    "Email CC mặc định"),
            ("email_bcc_mac_dinh",  "",                                 "string",  "email",    "Email BCC mặc định"),
            # Nhóm: payment
            ("tien_te",             "VND",                              "string",  "payment",  "Đơn vị tiền tệ"),
            ("thue_vat_phan_tram",  "10",                               "integer", "payment",  "Thuế VAT (%)"),
            ("phi_giao_hang_mac_dinh", "30000",                         "integer", "payment",  "Phí giao hàng mặc định (VND)"),
            ("mien_phi_giao_hang_tu",  "500000",                        "integer", "payment",  "Miễn phí giao hàng khi đơn >= N VND"),
            # Nhóm: loyalty
            ("ty_le_tich_diem",     "100",                              "integer", "loyalty",  "Mỗi N VND mua hàng được 1 điểm"),
            ("diem_quy_doi_tien",   "1000",                             "integer", "loyalty",  "1 điểm = N VND khi quy đổi"),
            # Nhóm: theme
            ("mau_chu_dao",         "#2563EB",                          "string",  "theme",    "Màu chủ đạo (hex)"),
            ("mau_phu",             "#10B981",                          "string",  "theme",    "Màu phụ (hex)"),
        ]
        for nqt_khoa, nqt_gia_tri, nqt_kieu, nqt_nhom, nqt_mo_ta in nqt_danh_sach_cau_hinh:
            db.session.add(NqtCauHinh(
                nqt_khoa=nqt_khoa,
                nqt_gia_tri=nqt_gia_tri,
                nqt_kieu_du_lieu=nqt_kieu,
                nqt_nhom=nqt_nhom,
                nqt_mo_ta=nqt_mo_ta,
            ))
        db.session.commit()
        print(f"[OK] NqtCauHinh — đã seed {len(nqt_danh_sach_cau_hinh)} rows")

    # ------------------------------------------------------------------
    # 2. NqtVaiTro
    # ------------------------------------------------------------------
    if NqtVaiTro.query.first():
        print("[SKIP] NqtVaiTro — đã có dữ liệu")
    else:
        nqt_danh_sach_vai_tro = [
            ("quan_tri",         "Quản trị hệ thống — toàn quyền"),
            ("quan_ly",          "Quản lý chi nhánh"),
            ("huan_luyen_vien",  "Huấn luyện viên PT"),
            ("le_tan",           "Lễ tân / Nhân viên tiếp đón"),
        ]
        for nqt_ten, nqt_mo_ta in nqt_danh_sach_vai_tro:
            db.session.add(NqtVaiTro(nqt_ten_vai_tro=nqt_ten, nqt_mo_ta=nqt_mo_ta))
        db.session.commit()
        print(f"[OK] NqtVaiTro — đã seed {len(nqt_danh_sach_vai_tro)} rows")

    # ------------------------------------------------------------------
    # 3. NqtQuyenHan
    # ------------------------------------------------------------------
    if NqtQuyenHan.query.first():
        print("[SKIP] NqtQuyenHan — đã có dữ liệu")
    else:
        nqt_danh_sach_quyen = [
            # Nhóm hoi_vien
            ("xem_hoi_vien",     "hoi_vien"),
            ("them_hoi_vien",    "hoi_vien"),
            ("sua_hoi_vien",     "hoi_vien"),
            ("xoa_hoi_vien",     "hoi_vien"),
            # Nhóm goi_tap
            ("xem_goi_tap",      "goi_tap"),
            ("them_goi_tap",     "goi_tap"),
            ("sua_goi_tap",      "goi_tap"),
            ("xoa_goi_tap",      "goi_tap"),
            # Nhóm nhan_vien
            ("xem_nhan_vien",    "nhan_vien"),
            ("them_nhan_vien",   "nhan_vien"),
            ("sua_nhan_vien",    "nhan_vien"),
            ("xoa_nhan_vien",    "nhan_vien"),
            # Nhóm don_hang
            ("xem_don_hang",     "don_hang"),
            ("sua_don_hang",     "don_hang"),
            ("huy_don_hang",     "don_hang"),
            # Nhóm bao_cao
            ("xem_bao_cao",      "bao_cao"),
            ("xuat_bao_cao",     "bao_cao"),
            # Nhóm cau_hinh
            ("quan_ly_cau_hinh", "cau_hinh"),
            ("xem_cau_hinh",     "cau_hinh"),
            ("sua_cau_hinh",     "cau_hinh"),
        ]
        for nqt_ten, nqt_nhom in nqt_danh_sach_quyen:
            db.session.add(NqtQuyenHan(nqt_ten_quyen=nqt_ten, nqt_nhom_quyen=nqt_nhom))
        db.session.commit()
        print(f"[OK] NqtQuyenHan — đã seed {len(nqt_danh_sach_quyen)} rows")

    # ------------------------------------------------------------------
    # 4. NqtVaiTroQuyen (mapping)
    # ------------------------------------------------------------------
    if NqtVaiTroQuyen.query.first():
        print("[SKIP] NqtVaiTroQuyen — đã có dữ liệu")
    else:
        nqt_vai_tro_map = {v.nqt_ten_vai_tro: v.nqt_ma_vai_tro for v in NqtVaiTro.query.all()}
        nqt_quyen_map   = {q.nqt_ten_quyen:   q.nqt_ma_quyen   for q in NqtQuyenHan.query.all()}

        # quan_tri nhận tất cả quyền
        nqt_quyen_theo_vai_tro = {
            "quan_tri": list(nqt_quyen_map.keys()),
            "quan_ly": [
                "xem_hoi_vien", "them_hoi_vien", "sua_hoi_vien",
                "xem_goi_tap",  "them_goi_tap",  "sua_goi_tap",
                "xem_nhan_vien","them_nhan_vien", "sua_nhan_vien",
                "xem_don_hang", "sua_don_hang",
                "xem_bao_cao",  "xuat_bao_cao",
            ],
            "huan_luyen_vien": [
                "xem_hoi_vien",
                "xem_goi_tap",
                "xem_bao_cao",
            ],
            "le_tan": [
                "xem_hoi_vien", "them_hoi_vien", "sua_hoi_vien",
                "xem_goi_tap",
                "xem_don_hang",
            ],
        }

        nqt_dem = 0
        for nqt_ten_vai_tro, nqt_ds_quyen in nqt_quyen_theo_vai_tro.items():
            nqt_ma_vai_tro = nqt_vai_tro_map.get(nqt_ten_vai_tro)
            if not nqt_ma_vai_tro:
                continue
            for nqt_ten_quyen in nqt_ds_quyen:
                nqt_ma_quyen = nqt_quyen_map.get(nqt_ten_quyen)
                if nqt_ma_quyen:
                    db.session.add(NqtVaiTroQuyen(
                        nqt_ma_vai_tro=nqt_ma_vai_tro,
                        nqt_ma_quyen=nqt_ma_quyen,
                    ))
                    nqt_dem += 1
        db.session.commit()
        print(f"[OK] NqtVaiTroQuyen — đã seed {nqt_dem} rows")

    # ------------------------------------------------------------------
    # 5. NqtChiNhanh
    # ------------------------------------------------------------------
    if NqtChiNhanh.query.first():
        print("[SKIP] NqtChiNhanh — đã có dữ liệu")
    else:
        nqt_danh_sach_chi_nhanh = [
            {
                "nqt_ten_chi_nhanh": "NQT Gym - Cầu Giấy",
                "nqt_dia_chi": "123 Xuân Thủy, Cầu Giấy",
                "nqt_thanh_pho": "Hà Nội",
                "nqt_tinh": "Hà Nội",
                "nqt_hotline": "024 3567 8901",
                "nqt_email": "caugiay@nqtgym.vn",
                "nqt_gio_mo_cua": time(5, 0),
                "nqt_gio_dong_cua": time(23, 0),
                "nqt_suc_chua_toi_da": 120,
                "nqt_co_sauna": True,
                "nqt_co_ho_boi": False,
                "nqt_vi_do": 21.036944,
                "nqt_kinh_do": 105.782778,
            },
            {
                "nqt_ten_chi_nhanh": "NQT Gym - Đống Đa",
                "nqt_dia_chi": "45 Láng Hạ, Đống Đa",
                "nqt_thanh_pho": "Hà Nội",
                "nqt_tinh": "Hà Nội",
                "nqt_hotline": "024 3678 9012",
                "nqt_email": "dongda@nqtgym.vn",
                "nqt_gio_mo_cua": time(5, 30),
                "nqt_gio_dong_cua": time(22, 30),
                "nqt_suc_chua_toi_da": 80,
                "nqt_co_sauna": True,
                "nqt_co_ho_boi": True,
                "nqt_vi_do": 21.022222,
                "nqt_kinh_do": 105.841389,
            },
        ]
        for nqt_cn in nqt_danh_sach_chi_nhanh:
            db.session.add(NqtChiNhanh(**nqt_cn))
        db.session.commit()
        print(f"[OK] NqtChiNhanh — đã seed {len(nqt_danh_sach_chi_nhanh)} rows")

    # ------------------------------------------------------------------
    # 6. NqtNguoiDung
    # ------------------------------------------------------------------
    if NqtNguoiDung.query.first():
        print("[SKIP] NqtNguoiDung — đã có dữ liệu")
    else:
        nqt_cn_1 = NqtChiNhanh.query.first()
        nqt_danh_sach_nguoi_dung = [
            {
                "nqt_ten_dang_nhap": "admin",
                "nqt_mat_khau": bcrypt.hashpw("Admin@123".encode(), bcrypt.gensalt()).decode(),
                "nqt_ho_ten": "Quản Trị Viên",
                "nqt_email": "admin@nqtgym.vn",
                "nqt_so_dien_thoai": "0901 000 001",
                "nqt_ma_chi_nhanh": nqt_cn_1.nqt_ma_chi_nhanh if nqt_cn_1 else None,
            },
            {
                "nqt_ten_dang_nhap": "manager_caugiay",
                "nqt_mat_khau": bcrypt.hashpw("Manager@123".encode(), bcrypt.gensalt()).decode(),
                "nqt_ho_ten": "Nguyễn Văn Quản",
                "nqt_email": "manager@nqtgym.vn",
                "nqt_so_dien_thoai": "0901 000 002",
                "nqt_ma_chi_nhanh": nqt_cn_1.nqt_ma_chi_nhanh if nqt_cn_1 else None,
            },
            {
                "nqt_ten_dang_nhap": "letan_01",
                "nqt_mat_khau": bcrypt.hashpw("LeTan@123".encode(), bcrypt.gensalt()).decode(),
                "nqt_ho_ten": "Trần Thị Lễ",
                "nqt_email": "letan@nqtgym.vn",
                "nqt_so_dien_thoai": "0901 000 003",
                "nqt_ma_chi_nhanh": nqt_cn_1.nqt_ma_chi_nhanh if nqt_cn_1 else None,
            },
        ]
        for nqt_nd in nqt_danh_sach_nguoi_dung:
            db.session.add(NqtNguoiDung(**nqt_nd))
        db.session.commit()
        print(f"[OK] NqtNguoiDung — đã seed {len(nqt_danh_sach_nguoi_dung)} rows")

    # ------------------------------------------------------------------
    # 7. NqtNguoiDungVaiTro (gán role)
    # ------------------------------------------------------------------
    if NqtNguoiDungVaiTro.query.first():
        print("[SKIP] NqtNguoiDungVaiTro — đã có dữ liệu")
    else:
        nqt_nd_map = {u.nqt_ten_dang_nhap: u.nqt_ma_nguoi_dung for u in NqtNguoiDung.query.all()}
        nqt_vt_map = {v.nqt_ten_vai_tro:   v.nqt_ma_vai_tro    for v in NqtVaiTro.query.all()}

        nqt_gan_vai_tro = [
            ("admin",            "quan_tri"),
            ("manager_caugiay",  "quan_ly"),
            ("letan_01",         "le_tan"),
        ]
        nqt_dem = 0
        for nqt_ten_dang_nhap, nqt_ten_vai_tro in nqt_gan_vai_tro:
            nqt_ma_nd = nqt_nd_map.get(nqt_ten_dang_nhap)
            nqt_ma_vt = nqt_vt_map.get(nqt_ten_vai_tro)
            if nqt_ma_nd and nqt_ma_vt:
                db.session.add(NqtNguoiDungVaiTro(
                    nqt_ma_nguoi_dung=nqt_ma_nd,
                    nqt_ma_vai_tro=nqt_ma_vt,
                ))
                nqt_dem += 1
        db.session.commit()
        print(f"[OK] NqtNguoiDungVaiTro — đã seed {nqt_dem} rows")

    # ------------------------------------------------------------------
    # 8. NqtNhanVien
    # ------------------------------------------------------------------
    if NqtNhanVien.query.first():
        print("[SKIP] NqtNhanVien — đã có dữ liệu")
    else:
        nqt_nd_map = {u.nqt_ten_dang_nhap: u.nqt_ma_nguoi_dung for u in NqtNguoiDung.query.all()}
        nqt_cn_1   = NqtChiNhanh.query.first()
        nqt_ma_cn  = nqt_cn_1.nqt_ma_chi_nhanh if nqt_cn_1 else 1

        nqt_danh_sach_nhan_vien = [
            {
                "nqt_ma_nguoi_dung": nqt_nd_map.get("admin"),
                "nqt_ma_chi_nhanh": nqt_ma_cn,
                "nqt_ho_ten": "Quản Trị Viên",
                "nqt_ngay_sinh": date(1990, 1, 1),
                "nqt_gioi_tinh": "nam",
                "nqt_so_dien_thoai": "0901 000 001",
                "nqt_email": "admin@nqtgym.vn",
                "nqt_ngay_vao_lam": date(2023, 1, 1),
                "nqt_luong_co_ban": 20_000_000,
            },
            {
                "nqt_ma_nguoi_dung": nqt_nd_map.get("manager_caugiay"),
                "nqt_ma_chi_nhanh": nqt_ma_cn,
                "nqt_ho_ten": "Nguyễn Văn Quản",
                "nqt_ngay_sinh": date(1992, 6, 15),
                "nqt_gioi_tinh": "nam",
                "nqt_so_dien_thoai": "0901 000 002",
                "nqt_email": "manager@nqtgym.vn",
                "nqt_ngay_vao_lam": date(2023, 3, 1),
                "nqt_luong_co_ban": 15_000_000,
            },
            {
                "nqt_ma_nguoi_dung": nqt_nd_map.get("letan_01"),
                "nqt_ma_chi_nhanh": nqt_ma_cn,
                "nqt_ho_ten": "Trần Thị Lễ",
                "nqt_ngay_sinh": date(1998, 9, 20),
                "nqt_gioi_tinh": "nu",
                "nqt_so_dien_thoai": "0901 000 003",
                "nqt_email": "letan@nqtgym.vn",
                "nqt_ngay_vao_lam": date(2024, 1, 15),
                "nqt_luong_co_ban": 8_000_000,
            },
        ]
        for nqt_nv in nqt_danh_sach_nhan_vien:
            db.session.add(NqtNhanVien(**nqt_nv))
        db.session.commit()
        print(f"[OK] NqtNhanVien — đã seed {len(nqt_danh_sach_nhan_vien)} rows")

    # ------------------------------------------------------------------
    # 9. NqtGoiTap
    # ------------------------------------------------------------------
    if NqtGoiTap.query.first():
        print("[SKIP] NqtGoiTap — đã có dữ liệu")
    else:
        nqt_danh_sach_goi = [
            {
                "nqt_ten_goi": "Gói 1 Tháng",
                "nqt_mo_ta": "Tập luyện tự do 1 tháng, 1 lượt/ngày",
                "nqt_so_ngay": 30,
                "nqt_gia": 500_000,
                "nqt_gia_khuyen_mai": None,
                "nqt_co_pt": False,
                "nqt_so_buoi_pt": 0,
                "nqt_co_sauna": False,
                "nqt_mau_hien_thi": "#3B82F6",
                "nqt_la_noi_bat": False,
                "nqt_thu_tu_hien_thi": 1,
            },
            {
                "nqt_ten_goi": "Gói 3 Tháng",
                "nqt_mo_ta": "Tập luyện tự do 3 tháng — tiết kiệm 10%",
                "nqt_so_ngay": 90,
                "nqt_gia": 1_350_000,
                "nqt_gia_khuyen_mai": 1_200_000,
                "nqt_co_pt": False,
                "nqt_so_buoi_pt": 0,
                "nqt_co_sauna": False,
                "nqt_mau_hien_thi": "#10B981",
                "nqt_la_noi_bat": False,
                "nqt_thu_tu_hien_thi": 2,
            },
            {
                "nqt_ten_goi": "Gói 6 Tháng",
                "nqt_mo_ta": "Tập luyện tự do 6 tháng — tiết kiệm 20%",
                "nqt_so_ngay": 180,
                "nqt_gia": 2_400_000,
                "nqt_gia_khuyen_mai": None,
                "nqt_co_pt": False,
                "nqt_so_buoi_pt": 0,
                "nqt_co_sauna": True,
                "nqt_mau_hien_thi": "#F59E0B",
                "nqt_la_noi_bat": True,
                "nqt_thu_tu_hien_thi": 3,
            },
            {
                "nqt_ten_goi": "Gói 1 Năm",
                "nqt_mo_ta": "Tập luyện tự do 12 tháng — tiết kiệm 30%",
                "nqt_so_ngay": 365,
                "nqt_gia": 4_200_000,
                "nqt_gia_khuyen_mai": None,
                "nqt_co_pt": False,
                "nqt_so_buoi_pt": 0,
                "nqt_co_sauna": True,
                "nqt_mau_hien_thi": "#8B5CF6",
                "nqt_la_noi_bat": False,
                "nqt_thu_tu_hien_thi": 4,
            },
            {
                "nqt_ten_goi": "Gói PT 12 Buổi",
                "nqt_mo_ta": "12 buổi tập cùng huấn luyện viên cá nhân",
                "nqt_so_ngay": 60,
                "nqt_gia": 3_600_000,
                "nqt_gia_khuyen_mai": None,
                "nqt_co_pt": True,
                "nqt_so_buoi_pt": 12,
                "nqt_co_sauna": False,
                "nqt_mau_hien_thi": "#EF4444",
                "nqt_la_noi_bat": False,
                "nqt_thu_tu_hien_thi": 5,
            },
        ]
        for nqt_gt in nqt_danh_sach_goi:
            db.session.add(NqtGoiTap(**nqt_gt))
        db.session.commit()
        print(f"[OK] NqtGoiTap — đã seed {len(nqt_danh_sach_goi)} rows")

    # ------------------------------------------------------------------
    # 10. NqtHangThanhVien
    # ------------------------------------------------------------------
    if NqtHangThanhVien.query.first():
        print("[SKIP] NqtHangThanhVien — đã có dữ liệu")
    else:
        nqt_danh_sach_hang = [
            ("Đồng",        0,      1.0,  "#CD7F32", "bronze"),
            ("Bạc",         5000,   1.2,  "#C0C0C0", "silver"),
            ("Vàng",        15000,  1.5,  "#FFD700", "gold"),
            ("Kim Cương",   50000,  2.0,  "#B9F2FF", "diamond"),
        ]
        for nqt_ten, nqt_diem, nqt_he_so, nqt_mau, nqt_icon in nqt_danh_sach_hang:
            db.session.add(NqtHangThanhVien(
                nqt_ten_hang=nqt_ten,
                nqt_diem_toi_thieu=nqt_diem,
                nqt_he_so_tich_diem=nqt_he_so,
                nqt_mau_hien_thi=nqt_mau,
                nqt_icon=nqt_icon,
            ))
        db.session.commit()
        print(f"[OK] NqtHangThanhVien — đã seed {len(nqt_danh_sach_hang)} rows")

    # ------------------------------------------------------------------
    # 11. NqtHoiVien
    # ------------------------------------------------------------------
    if NqtHoiVien.query.first():
        print("[SKIP] NqtHoiVien — đã có dữ liệu")
    else:
        import uuid
        nqt_cn_1  = NqtChiNhanh.query.first()
        nqt_ma_cn = nqt_cn_1.nqt_ma_chi_nhanh if nqt_cn_1 else 1

        nqt_danh_sach_hoi_vien = [
            {
                "nqt_ma_chi_nhanh": nqt_ma_cn,
                "nqt_ho_ten": "Nguyễn Thị Hoa",
                "nqt_ngay_sinh": date(1995, 3, 12),
                "nqt_gioi_tinh": "nu",
                "nqt_so_dien_thoai": "0912 345 001",
                "nqt_email": "hoa.nguyen@example.com",
                "nqt_dia_chi": "12 Trần Duy Hưng, Cầu Giấy, Hà Nội",
                "nqt_ngay_dang_ky": date(2025, 1, 10),
                "nqt_ma_qr": f"NQT-{uuid.uuid4().hex[:10].upper()}",
            },
            {
                "nqt_ma_chi_nhanh": nqt_ma_cn,
                "nqt_ho_ten": "Trần Văn Mạnh",
                "nqt_ngay_sinh": date(1990, 7, 25),
                "nqt_gioi_tinh": "nam",
                "nqt_so_dien_thoai": "0912 345 002",
                "nqt_email": "manh.tran@example.com",
                "nqt_dia_chi": "34 Hoàng Quốc Việt, Cầu Giấy, Hà Nội",
                "nqt_ngay_dang_ky": date(2025, 2, 1),
                "nqt_ma_qr": f"NQT-{uuid.uuid4().hex[:10].upper()}",
            },
            {
                "nqt_ma_chi_nhanh": nqt_ma_cn,
                "nqt_ho_ten": "Lê Thị Thu",
                "nqt_ngay_sinh": date(1998, 11, 5),
                "nqt_gioi_tinh": "nu",
                "nqt_so_dien_thoai": "0912 345 003",
                "nqt_email": "thu.le@example.com",
                "nqt_dia_chi": "56 Nguyễn Phong Sắc, Cầu Giấy, Hà Nội",
                "nqt_ngay_dang_ky": date(2025, 3, 15),
                "nqt_ma_qr": f"NQT-{uuid.uuid4().hex[:10].upper()}",
            },
            {
                "nqt_ma_chi_nhanh": nqt_ma_cn,
                "nqt_ho_ten": "Phạm Đức Minh",
                "nqt_ngay_sinh": date(1993, 5, 18),
                "nqt_gioi_tinh": "nam",
                "nqt_so_dien_thoai": "0912 345 004",
                "nqt_email": "minh.pham@example.com",
                "nqt_dia_chi": "78 Dịch Vọng, Cầu Giấy, Hà Nội",
                "nqt_ngay_dang_ky": date(2025, 4, 1),
                "nqt_ma_qr": f"NQT-{uuid.uuid4().hex[:10].upper()}",
            },
            {
                "nqt_ma_chi_nhanh": nqt_ma_cn,
                "nqt_ho_ten": "Hoàng Lan Anh",
                "nqt_ngay_sinh": date(2000, 8, 30),
                "nqt_gioi_tinh": "nu",
                "nqt_so_dien_thoai": "0912 345 005",
                "nqt_email": "lananh.hoang@example.com",
                "nqt_dia_chi": "90 Mai Dịch, Cầu Giấy, Hà Nội",
                "nqt_ngay_dang_ky": date(2025, 4, 10),
                "nqt_ma_qr": f"NQT-{uuid.uuid4().hex[:10].upper()}",
            },
        ]
        for nqt_hv in nqt_danh_sach_hoi_vien:
            db.session.add(NqtHoiVien(**nqt_hv))
        db.session.commit()
        print(f"[OK] NqtHoiVien — đã seed {len(nqt_danh_sach_hoi_vien)} rows")

    print("=== Seed hoàn tất ===")


def nqt_chay_drop_va_seed():
    """
    Drop toàn bộ bảng, tạo lại với NVARCHAR (nhờ @compiles rule trong __init__.py),
    sau đó seed dữ liệu mẫu.
    Dùng khi bảng cũ có VARCHAR → tiếng Việt bị lỗi '?'.
    """
    from backend.app import db

    print("=== DROP & RECREATE tất cả bảng ===")
    db.drop_all()
    print("[OK] Đã xóa tất cả bảng")
    db.create_all()
    print("[OK] Đã tạo lại tất cả bảng (NVARCHAR)")
    nqt_chay_seed()


# Chạy trực tiếp (không dùng flask CLI)
if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    from backend.app import nqt_tao_app
    nqt_app = nqt_tao_app()
    with nqt_app.app_context():
        nqt_chay_seed()
