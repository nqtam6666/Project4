"""
Seed dữ liệu mẫu cho G6 Gym Management System.
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
    from backend.app.models.g6_cau_hinh import G6CauHinh
    from backend.app.models.g6_nguoi_dung import (
        G6VaiTro, G6QuyenHan, G6NguoiDung,
        G6NguoiDungVaiTro, G6VaiTroQuyen,
    )
    from backend.app.models.g6_chi_nhanh import G6ChiNhanh, G6ThietBi
    from backend.app.models.g6_nhan_vien import G6NhanVien
    from backend.app.models.g6_hoi_vien import G6GoiTap, G6HoiVien
    from backend.app.models.g6_khach_hang import G6HangThanhVien

    print("=== Bắt đầu seed dữ liệu ===")

    # Tạo bảng nếu chưa có (cần thiết khi chuyển sang DB mới)
    db.create_all()
    print("[INFO] Đã kiểm tra/tạo schema database")

    # ------------------------------------------------------------------
    # 1. G6CauHinh
    # ------------------------------------------------------------------
    if G6CauHinh.query.first():
        print("[SKIP] G6CauHinh — đã có dữ liệu")
    else:
        g6_danh_sach_cau_hinh = [
            # Nhóm: website
            ("g6_ten_website",         "G6 Gym",                           "string",  "website",  "Tên website"),
            ("g6_mo_ta_website",       "Hệ thống quản lý phòng gym G6",   "string",  "website",  "Mô tả website"),
            ("g6_logo_url",            "",                                 "string",  "website",  "URL logo website"),
            ("g6_favicon_url",         "",                                 "string",  "website",  "URL favicon"),
            ("g6_so_dien_thoai_hotline", "1900 6868",                     "string",  "website",  "Hotline hiển thị"),
            ("g6_email_lien_he",       "contact@g6gym.vn",                 "string",  "website",  "Email liên hệ"),
            ("g6_dia_chi_tru_so",      "123 Cầu Giấy, Hà Nội",            "string",  "website",  "Địa chỉ trụ sở"),
            ("g6_facebook_url",        "https://facebook.com/g6gym",       "string",  "website",  "Facebook fanpage"),
            ("g6_zalo_url",            "https://zalo.me/g6gym",            "string",  "website",  "Zalo OA"),
            ("g6_instagram_url",       "",                                 "string",  "website",  "Instagram"),
            ("g6_youtube_url",         "",                                 "string",  "website",  "YouTube channel"),
            ("g6_footer_noi_dung",     "",                                 "string",  "website",  "Nội dung footer"),
            # Nhóm: security
            ("g6_loai_ma_hoa_mat_khau", "bcrypt",                          "string",  "security", "Thuật toán mã hóa: bcrypt|argon2|pbkdf2"),
            ("g6_jwt_het_han_phut",    "60",                               "int",     "security", "JWT access token hết hạn (phút)"),
            ("g6_jwt_refresh_ngay",    "7",                                "int",     "security", "JWT refresh token hết hạn (ngày)"),
            ("g6_so_lan_dang_nhap_sai", "5",                               "int",     "security", "Số lần đăng nhập sai tối đa"),
            ("g6_khoa_tai_khoan_phut", "30",                               "int",     "security", "Khóa tài khoản sau N phút"),
            ("g6_do_dai_mat_khau_toi_thieu", "8",                          "int",     "security", "Độ dài mật khẩu tối thiểu"),
            # Nhóm: email
            ("g6_smtp_host",           "",                                 "string",  "email",    "SMTP host"),
            ("g6_smtp_port",           "587",                              "int",     "email",    "SMTP port"),
            ("g6_smtp_username",       "",                                 "string",  "email",    "SMTP username"),
            ("g6_smtp_mat_khau",       "",                                 "string",  "email",    "SMTP password"),
            ("g6_smtp_ma_hoa",         "TLS",                              "string",  "email",    "SMTP encryption: TLS|SSL|None"),
            ("g6_email_gui_di",        "",                                 "string",  "email",    "From email address"),
            ("g6_ten_email_gui_di",    "",                                 "string",  "email",    "From email name"),
            # Nhóm: payment
            ("g6_don_vi_tien_te",      "VND",                              "string",  "payment",  "Đơn vị tiền tệ"),
            ("g6_vnpay_terminal_id",   "",                                 "string",  "payment",  "VNPay Terminal ID"),
            ("g6_vnpay_secret_key",    "",                                 "string",  "payment",  "VNPay Secret Key"),
            ("g6_momo_partner_code",   "",                                 "string",  "payment",  "MoMo Partner Code"),
            ("g6_momo_access_key",     "",                                 "string",  "payment",  "MoMo Access Key"),
            ("g6_momo_secret_key",     "",                                 "string",  "payment",  "MoMo Secret Key"),
            ("g6_thue_vat_phan_tram",  "0",                                "int",     "payment",  "Thuế VAT %"),
            # Nhóm: website (notification / loyalty)
            ("g6_so_ngay_nhac_het_han", "7",                               "int",     "website",  "Nhắc hội viên trước N ngày hết hạn"),
            ("g6_so_ngay_nhac_lan_2",  "3",                                "int",     "website",  "Nhắc lần 2 trước N ngày hết hạn"),
            ("g6_diem_tren_moi_1000_dong", "1",                            "int",     "website",  "1 điểm / N đồng chi tiêu"),
            ("g6_1_diem_bang_dong",    "100",                              "int",     "website",  "1 điểm = N đồng khi dùng"),
            # Nhóm: security (OTP)
            ("g6_otp_het_han_phut",    "5",                                "int",     "security", "OTP hết hạn sau N phút"),
            ("g6_otp_so_lan_nhap_sai", "3",                                "int",     "security", "OTP sai tối đa N lần"),
            # Nhóm: theme
            ("g6_mau_chinh",           "#0d6efd",                          "string",  "theme",    "Màu chủ đạo (hex)"),
            ("g6_mau_phu",             "#6c757d",                          "string",  "theme",    "Màu phụ (hex)"),
            ("g6_che_do_toi",          "0",                                "bool",    "theme",    "Bật chế độ tối mặc định"),
        ]
        for g6_khoa, g6_gia_tri, g6_kieu, g6_nhom, g6_mo_ta in g6_danh_sach_cau_hinh:
            db.session.add(G6CauHinh(
                g6_khoa=g6_khoa,
                g6_gia_tri=g6_gia_tri,
                g6_kieu_du_lieu=g6_kieu,
                g6_nhom=g6_nhom,
                g6_mo_ta=g6_mo_ta,
            ))
        db.session.commit()
        print(f"[OK] G6CauHinh — đã seed {len(g6_danh_sach_cau_hinh)} rows")

    # ------------------------------------------------------------------
    # 2. G6VaiTro
    # ------------------------------------------------------------------
    if G6VaiTro.query.first():
        print("[SKIP] G6VaiTro — đã có dữ liệu")
    else:
        g6_danh_sach_vai_tro = [
            ("G6QuanTri",         "Quản trị hệ thống — toàn quyền"),
            ("G6QuanLy",          "Quản lý chi nhánh"),
            ("G6HuanLuyenVien",   "Huấn luyện viên PT"),
            ("G6LeTan",           "Lễ tân - check-in, đăng ký hội viên"),
        ]
        for g6_ten, g6_mo_ta in g6_danh_sach_vai_tro:
            db.session.add(G6VaiTro(g6_ten_vai_tro=g6_ten, g6_mo_ta=g6_mo_ta))
        db.session.commit()
        print(f"[OK] G6VaiTro — đã seed {len(g6_danh_sach_vai_tro)} rows")

    # ------------------------------------------------------------------
    # 3. G6QuyenHan
    # ------------------------------------------------------------------
    if G6QuyenHan.query.first():
        print("[SKIP] G6QuyenHan — đã có dữ liệu")
    else:
        g6_danh_sach_quyen = [
            # Nhóm hoi_vien
            ("g6_xem_hoi_vien",        "hoi_vien"),
            ("g6_tao_hoi_vien",        "hoi_vien"),
            ("g6_sua_hoi_vien",        "hoi_vien"),
            ("g6_xoa_hoi_vien",        "hoi_vien"),
            # Nhóm san_pham
            ("g6_xem_san_pham",        "san_pham"),
            ("g6_tao_san_pham",        "san_pham"),
            ("g6_sua_san_pham",        "san_pham"),
            ("g6_xoa_san_pham",        "san_pham"),
            # Nhóm don_hang
            ("g6_xem_don_hang",        "don_hang"),
            ("g6_cap_nhat_don_hang",   "don_hang"),
            ("g6_huy_don_hang",        "don_hang"),
            # Nhóm bao_cao
            ("g6_xem_doanh_thu",       "bao_cao"),
            ("g6_xuat_bao_cao",        "bao_cao"),
            # Nhóm cau_hinh
            ("g6_xem_cau_hinh",        "cau_hinh"),
            ("g6_sua_cau_hinh",        "cau_hinh"),
            # Nhóm nhan_vien
            ("g6_quan_ly_nhan_vien",   "nhan_vien"),
            # Nhóm kho_hang
            ("g6_xem_kho_hang",        "kho_hang"),
            ("g6_dieu_chinh_kho",      "kho_hang"),
            # Nhóm hoi_vien (checkin)
            ("g6_checkin_hoi_vien",     "hoi_vien"),
            # Nhóm lop_hoc
            ("g6_xem_lich_lop_hoc",    "lop_hoc"),
            ("g6_quan_ly_lop_hoc",     "lop_hoc"),
        ]
        for g6_ten, g6_nhom in g6_danh_sach_quyen:
            db.session.add(G6QuyenHan(g6_ten_quyen=g6_ten, g6_nhom_quyen=g6_nhom))
        db.session.commit()
        print(f"[OK] G6QuyenHan — đã seed {len(g6_danh_sach_quyen)} rows")

    # ------------------------------------------------------------------
    # 4. G6VaiTroQuyen (mapping)
    # ------------------------------------------------------------------
    if G6VaiTroQuyen.query.first():
        print("[SKIP] G6VaiTroQuyen — đã có dữ liệu")
    else:
        g6_vai_tro_map = {v.g6_ten_vai_tro: v.g6_ma_vai_tro for v in G6VaiTro.query.all()}
        g6_quyen_map   = {q.g6_ten_quyen:   q.g6_ma_quyen   for q in G6QuyenHan.query.all()}

        # G6QuanTri nhận tất cả quyền
        g6_quyen_theo_vai_tro = {
            "G6QuanTri": list(g6_quyen_map.keys()),
            "G6QuanLy": [
                "g6_xem_hoi_vien", "g6_tao_hoi_vien", "g6_sua_hoi_vien",
                "g6_xem_san_pham", "g6_tao_san_pham", "g6_sua_san_pham",
                "g6_xem_don_hang", "g6_cap_nhat_don_hang",
                "g6_xem_doanh_thu", "g6_xuat_bao_cao",
                "g6_quan_ly_nhan_vien",
                "g6_xem_kho_hang", "g6_dieu_chinh_kho",
                "g6_checkin_hoi_vien",
                "g6_xem_lich_lop_hoc", "g6_quan_ly_lop_hoc",
            ],
            "G6HuanLuyenVien": [
                "g6_xem_hoi_vien",
                "g6_xem_san_pham",
                "g6_xem_lich_lop_hoc",
            ],
            "G6LeTan": [
                "g6_xem_hoi_vien", "g6_tao_hoi_vien", "g6_sua_hoi_vien",
                "g6_checkin_hoi_vien",
                "g6_xem_san_pham",
                "g6_xem_don_hang",
                "g6_xem_lich_lop_hoc",
            ],
        }

        g6_dem = 0
        for g6_ten_vai_tro, g6_ds_quyen in g6_quyen_theo_vai_tro.items():
            g6_ma_vai_tro = g6_vai_tro_map.get(g6_ten_vai_tro)
            if not g6_ma_vai_tro:
                continue
            for g6_ten_quyen in g6_ds_quyen:
                g6_ma_quyen = g6_quyen_map.get(g6_ten_quyen)
                if g6_ma_quyen:
                    db.session.add(G6VaiTroQuyen(
                        g6_ma_vai_tro=g6_ma_vai_tro,
                        g6_ma_quyen=g6_ma_quyen,
                    ))
                    g6_dem += 1
        db.session.commit()
        print(f"[OK] G6VaiTroQuyen — đã seed {g6_dem} rows")

    # ------------------------------------------------------------------
    # 5. G6ChiNhanh
    # ------------------------------------------------------------------
    if G6ChiNhanh.query.first():
        print("[SKIP] G6ChiNhanh — đã có dữ liệu")
    else:
        g6_danh_sach_chi_nhanh = [
            {
                "g6_ten_chi_nhanh": "G6 Gym - Cầu Giấy",
                "g6_dia_chi": "123 Xuân Thủy, Cầu Giấy",
                "g6_thanh_pho": "Hà Nội",
                "g6_tinh": "Hà Nội",
                "g6_hotline": "024 3567 8901",
                "g6_email": "caugiay@g6gym.vn",
                "g6_gio_mo_cua": time(5, 0),
                "g6_gio_dong_cua": time(23, 0),
                "g6_suc_chua_toi_da": 120,
                "g6_co_sauna": True,
                "g6_co_ho_boi": False,
                "g6_vi_do": 21.036944,
                "g6_kinh_do": 105.782778,
            },
            {
                "g6_ten_chi_nhanh": "G6 Gym - Đống Đa",
                "g6_dia_chi": "45 Láng Hạ, Đống Đa",
                "g6_thanh_pho": "Hà Nội",
                "g6_tinh": "Hà Nội",
                "g6_hotline": "024 3678 9012",
                "g6_email": "dongda@g6gym.vn",
                "g6_gio_mo_cua": time(5, 30),
                "g6_gio_dong_cua": time(22, 30),
                "g6_suc_chua_toi_da": 80,
                "g6_co_sauna": True,
                "g6_co_ho_boi": True,
                "g6_vi_do": 21.022222,
                "g6_kinh_do": 105.841389,
            },
        ]
        for g6_cn in g6_danh_sach_chi_nhanh:
            db.session.add(G6ChiNhanh(**g6_cn))
        db.session.commit()
        print(f"[OK] G6ChiNhanh — đã seed {len(g6_danh_sach_chi_nhanh)} rows")

    # ------------------------------------------------------------------
    # 6. G6NguoiDung
    # ------------------------------------------------------------------
    if G6NguoiDung.query.first():
        print("[SKIP] G6NguoiDung — đã có dữ liệu")
    else:
        g6_cn_1 = G6ChiNhanh.query.first()
        g6_danh_sach_nguoi_dung = [
            {
                "g6_ten_dang_nhap": "quangtam",
                "g6_mat_khau": bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode(),
                "g6_ho_ten": "Nguyễn Quang Tâm",
                "g6_email": "nguyenquangtam6666@gmail.com",
                "g6_so_dien_thoai": "0961138440",
                "g6_ma_chi_nhanh": g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else None,
            },
            {
                "g6_ten_dang_nhap": "xuanvinh",
                "g6_mat_khau": bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode(),
                "g6_ho_ten": "Nguyễn Xuân Vinh",
                "g6_email": "realsteelworld2k5@gmail.com",
                "g6_so_dien_thoai": "0961138441",
                "g6_ma_chi_nhanh": g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else None,
            },
            {
                "g6_ten_dang_nhap": "hoainam",
                "g6_mat_khau": bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode(),
                "g6_ho_ten": "Nguyễn Hoài Nam",
                "g6_email": "siver1856@gmail.com",
                "g6_so_dien_thoai": "0961138442",
                "g6_ma_chi_nhanh": g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else None,
            },
            {
                "g6_ten_dang_nhap": "doanquan",
                "g6_mat_khau": bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode(),
                "g6_ho_ten": "Đoàn Anh Quân",
                "g6_email": "doanqu4n6805@gmail.com",
                "g6_so_dien_thoai": "0961138443",
                "g6_ma_chi_nhanh": g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else None,
            },
            {
                "g6_ten_dang_nhap": "manager_caugiay",
                "g6_mat_khau": bcrypt.hashpw("Manager@123".encode(), bcrypt.gensalt()).decode(),
                "g6_ho_ten": "Nguyễn Văn Quản",
                "g6_email": "manager@g6gym.vn",
                "g6_so_dien_thoai": "0901000002",
                "g6_ma_chi_nhanh": g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else None,
            },
            {
                "g6_ten_dang_nhap": "letan_01",
                "g6_mat_khau": bcrypt.hashpw("LeTan@123".encode(), bcrypt.gensalt()).decode(),
                "g6_ho_ten": "Trần Thị Lễ",
                "g6_email": "letan@g6gym.vn",
                "g6_so_dien_thoai": "0901000003",
                "g6_ma_chi_nhanh": g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else None,
            },
            
        ]
        for g6_nd in g6_danh_sach_nguoi_dung:
            db.session.add(G6NguoiDung(**g6_nd))
        db.session.commit()
        print(f"[OK] G6NguoiDung — đã seed {len(g6_danh_sach_nguoi_dung)} rows")
        # ------------------------------------------------------------------
        # 7. G6NguoiDungVaiTro (gán role)
        # ------------------------------------------------------------------
        if G6NguoiDungVaiTro.query.first():
            print("[SKIP] G6NguoiDungVaiTro — đã có dữ liệu")
        else:
            g6_nd_map = {u.g6_ten_dang_nhap: u.g6_ma_nguoi_dung for u in G6NguoiDung.query.all()}
            g6_vt_map = {v.g6_ten_vai_tro:   v.g6_ma_vai_tro    for v in G6VaiTro.query.all()}

            g6_gan_vai_tro = [
                # ADMIN
                ("quangtam",        "G6QuanTri"),

                # MANAGER
                ("manager_caugiay", "G6QuanLy"),

                # LỄ TÂN
                ("letan_01",        "G6LeTan"),

                # NHÂN VIÊN / STAFF
                ("xuanvinh",        "G6QuanTri"),
                ("hoainam",         "G6NhanVien"),
                ("doanquan",        "G6QuanTri"),
            ]

            g6_dem = 0
            for g6_ten_dang_nhap, g6_ten_vai_tro in g6_gan_vai_tro:
                g6_ma_nd = g6_nd_map.get(g6_ten_dang_nhap)
                g6_ma_vt = g6_vt_map.get(g6_ten_vai_tro)

                if not g6_ma_nd:
                    print(f"[WARN] Không tìm thấy user: {g6_ten_dang_nhap}")
                    continue
                if not g6_ma_vt:
                    print(f"[WARN] Không tìm thấy role: {g6_ten_vai_tro}")
                    continue

                db.session.add(G6NguoiDungVaiTro(
                    g6_ma_nguoi_dung=g6_ma_nd,
                    g6_ma_vai_tro=g6_ma_vt,
                ))
                g6_dem += 1

            db.session.commit()
            print(f"[OK] G6NguoiDungVaiTro — đã seed {g6_dem} rows")
    # ------------------------------------------------------------------
    # 8. G6NhanVien
    # ------------------------------------------------------------------
    if G6NhanVien.query.first():
        print("[SKIP] G6NhanVien — đã có dữ liệu")
    else:
        g6_nd_map = {u.g6_ten_dang_nhap: u.g6_ma_nguoi_dung for u in G6NguoiDung.query.all()}
        g6_cn_1   = G6ChiNhanh.query.first()
        g6_ma_cn  = g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else 1

        g6_danh_sach_nhan_vien = [
            {
                "g6_ma_nguoi_dung": g6_nd_map.get("admin"),
                "g6_ma_chi_nhanh": g6_ma_cn,
                "g6_ho_ten": "Quản Trị Viên",
                "g6_ngay_sinh": date(1990, 1, 1),
                "g6_gioi_tinh": "nam",
                "g6_so_dien_thoai": "0901000001",
                "g6_email": "admin@g6gym.vn",
                "g6_ngay_vao_lam": date(2023, 1, 1),
                "g6_luong_co_ban": 20_000_000,
            },
            {
                "g6_ma_nguoi_dung": g6_nd_map.get("manager_caugiay"),
                "g6_ma_chi_nhanh": g6_ma_cn,
                "g6_ho_ten": "Nguyễn Văn Quản",
                "g6_ngay_sinh": date(1992, 6, 15),
                "g6_gioi_tinh": "nam",
                "g6_so_dien_thoai": "0901000002",
                "g6_email": "manager@g6gym.vn",
                "g6_ngay_vao_lam": date(2023, 3, 1),
                "g6_luong_co_ban": 15_000_000,
            },
            {
                "g6_ma_nguoi_dung": g6_nd_map.get("letan_01"),
                "g6_ma_chi_nhanh": g6_ma_cn,
                "g6_ho_ten": "Trần Thị Lễ",
                "g6_ngay_sinh": date(1998, 9, 20),
                "g6_gioi_tinh": "nu",
                "g6_so_dien_thoai": "0901000003",
                "g6_email": "letan@g6gym.vn",
                "g6_ngay_vao_lam": date(2024, 1, 15),
                "g6_luong_co_ban": 8_000_000,
            },
        ]
        for g6_nv in g6_danh_sach_nhan_vien:
            db.session.add(G6NhanVien(**g6_nv))
        db.session.commit()
        print(f"[OK] G6NhanVien — đã seed {len(g6_danh_sach_nhan_vien)} rows")

    # ------------------------------------------------------------------
    # 9. G6GoiTap
    # ------------------------------------------------------------------
    if G6GoiTap.query.first():
        print("[SKIP] G6GoiTap — đã có dữ liệu")
    else:
        g6_danh_sach_goi = [
            {
                "g6_ten_goi": "Gói 1 Tháng",
                "g6_mo_ta": "Tập luyện tự do 1 tháng, 1 lượt/ngày",
                "g6_so_ngay": 30,
                "g6_gia": 500_000,
                "g6_gia_khuyen_mai": None,
                "g6_co_pt": False,
                "g6_so_buoi_pt": 0,
                "g6_co_sauna": False,
                "g6_mau_hien_thi": "#3B82F6",
                "g6_la_noi_bat": False,
                "g6_thu_tu_hien_thi": 1,
            },
            {
                "g6_ten_goi": "Gói 3 Tháng",
                "g6_mo_ta": "Tập luyện tự do 3 tháng — tiết kiệm 10%",
                "g6_so_ngay": 90,
                "g6_gia": 1_350_000,
                "g6_gia_khuyen_mai": 1_200_000,
                "g6_co_pt": False,
                "g6_so_buoi_pt": 0,
                "g6_co_sauna": False,
                "g6_mau_hien_thi": "#10B981",
                "g6_la_noi_bat": False,
                "g6_thu_tu_hien_thi": 2,
            },
            {
                "g6_ten_goi": "Gói 6 Tháng",
                "g6_mo_ta": "Tập luyện tự do 6 tháng — tiết kiệm 20%",
                "g6_so_ngay": 180,
                "g6_gia": 2_400_000,
                "g6_gia_khuyen_mai": None,
                "g6_co_pt": False,
                "g6_so_buoi_pt": 0,
                "g6_co_sauna": True,
                "g6_mau_hien_thi": "#F59E0B",
                "g6_la_noi_bat": True,
                "g6_thu_tu_hien_thi": 3,
            },
            {
                "g6_ten_goi": "Gói 1 Năm",
                "g6_mo_ta": "Tập luyện tự do 12 tháng — tiết kiệm 30%",
                "g6_so_ngay": 365,
                "g6_gia": 4_200_000,
                "g6_gia_khuyen_mai": None,
                "g6_co_pt": False,
                "g6_so_buoi_pt": 0,
                "g6_co_sauna": True,
                "g6_mau_hien_thi": "#8B5CF6",
                "g6_la_noi_bat": False,
                "g6_thu_tu_hien_thi": 4,
            },
            {
                "g6_ten_goi": "Gói PT 12 Buổi",
                "g6_mo_ta": "12 buổi tập cùng huấn luyện viên cá nhân",
                "g6_so_ngay": 60,
                "g6_gia": 3_600_000,
                "g6_gia_khuyen_mai": None,
                "g6_co_pt": True,
                "g6_so_buoi_pt": 12,
                "g6_co_sauna": False,
                "g6_mau_hien_thi": "#EF4444",
                "g6_la_noi_bat": False,
                "g6_thu_tu_hien_thi": 5,
            },
        ]
        for g6_gt in g6_danh_sach_goi:
            db.session.add(G6GoiTap(**g6_gt))
        db.session.commit()
        print(f"[OK] G6GoiTap — đã seed {len(g6_danh_sach_goi)} rows")

    # ------------------------------------------------------------------
    # 10. G6HangThanhVien
    # ------------------------------------------------------------------
    if G6HangThanhVien.query.first():
        print("[SKIP] G6HangThanhVien — đã có dữ liệu")
    else:
        g6_danh_sach_hang = [
            ("Đồng",        0,      1.0,  "#CD7F32"),
            ("Bạc",         5000,   1.2,  "#C0C0C0"),
            ("Vàng",        15000,  1.5,  "#FFD700"),
            ("Kim Cương",   50000,  2.0,  "#B9F2FF"),
        ]
        for g6_ten, g6_diem, g6_he_so, g6_mau in g6_danh_sach_hang:
            db.session.add(G6HangThanhVien(
                g6_ten_hang=g6_ten,
                g6_diem_toi_thieu=g6_diem,
                g6_he_so_tich_diem=g6_he_so,
                g6_mau_hien_thi=g6_mau,
            ))
        db.session.commit()
        print(f"[OK] G6HangThanhVien — đã seed {len(g6_danh_sach_hang)} rows")

    # ------------------------------------------------------------------
    # 11. G6HoiVien
    # ------------------------------------------------------------------
    if G6HoiVien.query.first():
        print("[SKIP] G6HoiVien — đã có dữ liệu")
    else:
        import uuid
        g6_cn_1  = G6ChiNhanh.query.first()
        g6_ma_cn = g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else 1

        g6_danh_sach_hoi_vien = [
            {
                "g6_ma_chi_nhanh": g6_ma_cn,
                "g6_ho_ten": "Nguyễn Thị Hoa",
                "g6_ngay_sinh": date(1995, 3, 12),
                "g6_gioi_tinh": "nu",
                "g6_so_dien_thoai": "0912345001",
                "g6_email": "hoa.nguyen@example.com",
                "g6_dia_chi": "12 Trần Duy Hưng, Cầu Giấy, Hà Nội",
                "g6_ngay_dang_ky": date(2026, 3, 28),
                "g6_ma_qr": f"G6-{uuid.uuid4().hex[:10].upper()}",
            },
            {
                "g6_ma_chi_nhanh": g6_ma_cn,
                "g6_ho_ten": "Trần Văn Mạnh",
                "g6_ngay_sinh": date(1990, 7, 25),
                "g6_gioi_tinh": "nam",
                "g6_so_dien_thoai": "0912345002",
                "g6_email": "manh.tran@example.com",
                "g6_dia_chi": "34 Hoàng Quốc Việt, Cầu Giấy, Hà Nội",
                "g6_ngay_dang_ky": date(2026, 4, 1),
                "g6_ma_qr": f"G6-{uuid.uuid4().hex[:10].upper()}",
            },
            {
                "g6_ma_chi_nhanh": g6_ma_cn,
                "g6_ho_ten": "Lê Thị Thu",
                "g6_ngay_sinh": date(1998, 11, 5),
                "g6_gioi_tinh": "nu",
                "g6_so_dien_thoai": "0912345003",
                "g6_email": "thu.le@example.com",
                "g6_dia_chi": "56 Nguyễn Phong Sắc, Cầu Giấy, Hà Nội",
                "g6_ngay_dang_ky": date(2026, 4, 5),
                "g6_ma_qr": f"G6-{uuid.uuid4().hex[:10].upper()}",
            },
            {
                "g6_ma_chi_nhanh": g6_ma_cn,
                "g6_ho_ten": "Phạm Đức Minh",
                "g6_ngay_sinh": date(1993, 5, 18),
                "g6_gioi_tinh": "nam",
                "g6_so_dien_thoai": "0912345004",
                "g6_email": "minh.pham@example.com",
                "g6_dia_chi": "78 Dịch Vọng, Cầu Giấy, Hà Nội",
                "g6_ngay_dang_ky": date(2026, 4, 8),
                "g6_ma_qr": f"G6-{uuid.uuid4().hex[:10].upper()}",
            },
            {
                "g6_ma_chi_nhanh": g6_ma_cn,
                "g6_ho_ten": "Hoàng Lan Anh",
                "g6_ngay_sinh": date(2000, 8, 30),
                "g6_gioi_tinh": "nu",
                "g6_so_dien_thoai": "0912345005",
                "g6_email": "lananh.hoang@example.com",
                "g6_dia_chi": "90 Mai Dịch, Cầu Giấy, Hà Nội",
                "g6_ngay_dang_ky": date(2026, 4, 12),
                "g6_ma_qr": f"G6-{uuid.uuid4().hex[:10].upper()}",
            },
        ]
        for g6_hv in g6_danh_sach_hoi_vien:
            db.session.add(G6HoiVien(**g6_hv))
        db.session.commit()
        print(f"[OK] G6HoiVien — đã seed {len(g6_danh_sach_hoi_vien)} rows")

    # ------------------------------------------------------------------
    # 12. G6KhachHang
    # ------------------------------------------------------------------
    from backend.app.models.g6_khach_hang import G6KhachHang
    if G6KhachHang.query.first():
        print("[SKIP] G6KhachHang — đã có dữ liệu")
    else:
        g6_danh_sach_khach_hang = [
            {
                "g6_ho_ten": "Nguyễn Văn An",
                "g6_email": "an.nguyen@email.com",
                "g6_so_dien_thoai": "0987654321",
                "g6_la_hoat_dong": True,
            },
            {
                "g6_ho_ten": "Trần Thị Bình",
                "g6_email": "binh.tran@email.com",
                "g6_so_dien_thoai": "0912345678",
                "g6_la_hoat_dong": True,
            },
            {
                "g6_ho_ten": "Lê Văn Cường",
                "g6_email": "cuong.le@email.com",
                "g6_so_dien_thoai": "0909123456",
                "g6_la_hoat_dong": True,
            },
            {
                "g6_ho_ten": "Phạm Thị Dung",
                "g6_email": "dung.pham@email.com",
                "g6_so_dien_thoai": "0933456789",
                "g6_la_hoat_dong": True,
            },
            {
                "g6_ho_ten": "Hoàng Văn Em",
                "g6_email": "em.hoang@email.com",
                "g6_so_dien_thoai": "0944567890",
                "g6_la_hoat_dong": True,
            },
        ]
        for g6_kh in g6_danh_sach_khach_hang:
            db.session.add(G6KhachHang(**g6_kh))
        db.session.commit()
        print(f"[OK] G6KhachHang — đã seed {len(g6_danh_sach_khach_hang)} rows")

    # ------------------------------------------------------------------
    # 13. G6DonHang + G6ChiTietDonHang + G6LichSuDonHang
    # ------------------------------------------------------------------
    from backend.app.models.g6_don_hang import G6DonHang, G6ChiTietDonHang, G6LichSuDonHang
    if G6DonHang.query.first():
        print("[SKIP] G6DonHang — đã có dữ liệu")
    else:
        from datetime import timedelta
        import random

        g6_khach_hangs = G6KhachHang.query.all()
        g6_nguoi_dung = G6NguoiDung.query.first()

        g6_san_pham_mau = [
            {"ten": "Whey Protein Isolate 2kg", "gia": 1_500_000},
            {"ten": "BCAA Amino Acid 300g", "gia": 450_000},
            {"ten": "Creatine Monohydrate 500g", "gia": 350_000},
            {"ten": "Pre-Workout Energy 400g", "gia": 680_000},
            {"ten": "Mass Gainer 3kg", "gia": 980_000},
            {"ten": "Găng tay tập gym", "gia": 180_000},
            {"ten": "Bình lắc shaker 700ml", "gia": 95_000},
            {"ten": "Đai lưng tập gym", "gia": 320_000},
            {"ten": "Dây kháng lực set 5 dây", "gia": 250_000},
            {"ten": "Áo tank top gym nam", "gia": 220_000},
        ]

        g6_danh_sach_don_hang = [
            # Đơn chờ xác nhận
            {
                "g6_ma_khach_hang": g6_khach_hangs[0].g6_ma_khach_hang if g6_khach_hangs else None,
                "g6_ho_ten_nguoi_nhan": "Nguyễn Văn An",
                "g6_so_dien_thoai": "0987654321",
                "g6_dia_chi_giao_hang": "123 Cầu Giấy, Hà Nội",
                "g6_tong_tien_hang": 2_130_000,
                "g6_phi_van_chuyen": 30_000,
                "g6_so_tien_giam": 0,
                "g6_tong_thanh_toan": 2_160_000,
                "g6_trang_thai": "cho_xac_nhan",
                "g6_phuong_thuc_thanh_toan": "cod",
                "g6_ghi_chu_khach": "Giao giờ hành chính",
                "g6_ngay_tao": datetime.utcnow() - timedelta(hours=2),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[1].g6_ma_khach_hang if len(g6_khach_hangs) > 1 else None,
                "g6_ho_ten_nguoi_nhan": "Trần Thị Bình",
                "g6_so_dien_thoai": "0912345678",
                "g6_dia_chi_giao_hang": "45 Láng Hạ, Đống Đa, Hà Nội",
                "g6_tong_tien_hang": 1_950_000,
                "g6_phi_van_chuyen": 25_000,
                "g6_so_tien_giam": 100_000,
                "g6_tong_thanh_toan": 1_875_000,
                "g6_trang_thai": "cho_xac_nhan",
                "g6_phuong_thuc_thanh_toan": "bank_transfer",
                "g6_ghi_chu_khach": "Gọi trước khi giao",
                "g6_ngay_tao": datetime.utcnow() - timedelta(hours=5),
            },
            # Đơn đã xác nhận
            {
                "g6_ma_khach_hang": g6_khach_hangs[2].g6_ma_khach_hang if len(g6_khach_hangs) > 2 else None,
                "g6_ho_ten_nguoi_nhan": "Lê Văn Cường",
                "g6_so_dien_thoai": "0909123456",
                "g6_dia_chi_giao_hang": "78 Nguyễn Trãi, Thanh Xuân, Hà Nội",
                "g6_tong_tien_hang": 800_000,
                "g6_phi_van_chuyen": 20_000,
                "g6_so_tien_giam": 50_000,
                "g6_tong_thanh_toan": 770_000,
                "g6_trang_thai": "da_xac_nhan",
                "g6_phuong_thuc_thanh_toan": "momo",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=1),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[3].g6_ma_khach_hang if len(g6_khach_hangs) > 3 else None,
                "g6_ho_ten_nguoi_nhan": "Phạm Thị Dung",
                "g6_so_dien_thoai": "0933456789",
                "g6_dia_chi_giao_hang": "90 Trần Phú, Hà Đông, Hà Nội",
                "g6_tong_tien_hang": 1_500_000,
                "g6_phi_van_chuyen": 30_000,
                "g6_so_tien_giam": 0,
                "g6_tong_thanh_toan": 1_530_000,
                "g6_trang_thai": "da_xac_nhan",
                "g6_phuong_thuc_thanh_toan": "vnpay",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=1, hours=3),
            },
            # Đơn đang giao
            {
                "g6_ma_khach_hang": g6_khach_hangs[4].g6_ma_khach_hang if len(g6_khach_hangs) > 4 else None,
                "g6_ho_ten_nguoi_nhan": "Hoàng Văn Em",
                "g6_so_dien_thoai": "0944567890",
                "g6_dia_chi_giao_hang": "56 Giải Phóng, Hai Bà Trưng, Hà Nội",
                "g6_tong_tien_hang": 2_480_000,
                "g6_phi_van_chuyen": 0,
                "g6_so_tien_giam": 200_000,
                "g6_tong_thanh_toan": 2_280_000,
                "g6_trang_thai": "dang_giao",
                "g6_phuong_thuc_thanh_toan": "cod",
                "g6_ghi_chu_khach": "Để ở bảo vệ nếu không có người nhận",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=2),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[0].g6_ma_khach_hang if g6_khach_hangs else None,
                "g6_ho_ten_nguoi_nhan": "Nguyễn Văn An",
                "g6_so_dien_thoai": "0987654321",
                "g6_dia_chi_giao_hang": "123 Cầu Giấy, Hà Nội",
                "g6_tong_tien_hang": 570_000,
                "g6_phi_van_chuyen": 25_000,
                "g6_so_tien_giam": 0,
                "g6_tong_thanh_toan": 595_000,
                "g6_trang_thai": "dang_giao",
                "g6_phuong_thuc_thanh_toan": "bank_transfer",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=2, hours=5),
            },
            # Đơn đã giao
            {
                "g6_ma_khach_hang": g6_khach_hangs[1].g6_ma_khach_hang if len(g6_khach_hangs) > 1 else None,
                "g6_ho_ten_nguoi_nhan": "Trần Thị Bình",
                "g6_so_dien_thoai": "0912345678",
                "g6_dia_chi_giao_hang": "45 Láng Hạ, Đống Đa, Hà Nội",
                "g6_tong_tien_hang": 980_000,
                "g6_phi_van_chuyen": 30_000,
                "g6_so_tien_giam": 0,
                "g6_tong_thanh_toan": 1_010_000,
                "g6_trang_thai": "da_giao",
                "g6_phuong_thuc_thanh_toan": "cod",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=5),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[2].g6_ma_khach_hang if len(g6_khach_hangs) > 2 else None,
                "g6_ho_ten_nguoi_nhan": "Lê Văn Cường",
                "g6_so_dien_thoai": "0909123456",
                "g6_dia_chi_giao_hang": "78 Nguyễn Trãi, Thanh Xuân, Hà Nội",
                "g6_tong_tien_hang": 1_850_000,
                "g6_phi_van_chuyen": 0,
                "g6_so_tien_giam": 150_000,
                "g6_tong_thanh_toan": 1_700_000,
                "g6_trang_thai": "da_giao",
                "g6_phuong_thuc_thanh_toan": "momo",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=7),
            },
            # Đơn đã hủy
            {
                "g6_ma_khach_hang": g6_khach_hangs[3].g6_ma_khach_hang if len(g6_khach_hangs) > 3 else None,
                "g6_ho_ten_nguoi_nhan": "Phạm Thị Dung",
                "g6_so_dien_thoai": "0933456789",
                "g6_dia_chi_giao_hang": "90 Trần Phú, Hà Đông, Hà Nội",
                "g6_tong_tien_hang": 350_000,
                "g6_phi_van_chuyen": 20_000,
                "g6_so_tien_giam": 0,
                "g6_tong_thanh_toan": 370_000,
                "g6_trang_thai": "da_huy",
                "g6_phuong_thuc_thanh_toan": "cod",
                "g6_ghi_chu_noi_bo": "Khách yêu cầu hủy",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=3),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[4].g6_ma_khach_hang if len(g6_khach_hangs) > 4 else None,
                "g6_ho_ten_nguoi_nhan": "Hoàng Văn Em",
                "g6_so_dien_thoai": "0944567890",
                "g6_dia_chi_giao_hang": "56 Giải Phóng, Hai Bà Trưng, Hà Nội",
                "g6_tong_tien_hang": 450_000,
                "g6_phi_van_chuyen": 25_000,
                "g6_so_tien_giam": 0,
                "g6_tong_thanh_toan": 475_000,
                "g6_trang_thai": "da_huy",
                "g6_phuong_thuc_thanh_toan": "bank_transfer",
                "g6_ghi_chu_noi_bo": "Hết hàng",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=4),
            },
        ]

        # Tạo đơn hàng
        for g6_dh in g6_danh_sach_don_hang:
            db.session.add(G6DonHang(**g6_dh))
        db.session.commit()
        print(f"[OK] G6DonHang — đã seed {len(g6_danh_sach_don_hang)} rows")

        # Tạo chi tiết đơn hàng
        g6_don_hangs = G6DonHang.query.all()
        g6_dem_ct = 0
        for g6_dh in g6_don_hangs:
            g6_so_sp = random.randint(2, 4)
            g6_san_pham_chon = random.sample(g6_san_pham_mau, g6_so_sp)
            for idx, g6_sp in enumerate(g6_san_pham_chon):
                g6_so_luong = random.randint(1, 3)
                g6_don_gia = g6_sp["gia"]
                g6_thanh_tien = g6_don_gia * g6_so_luong
                db.session.add(G6ChiTietDonHang(
                    g6_ma_don_hang=g6_dh.g6_ma_don_hang,
                    g6_ma_bien_the=idx + 1,
                    g6_ten_san_pham=g6_sp["ten"],
                    g6_sku=f"SKU-{random.randint(1000, 9999)}",
                    g6_so_luong=g6_so_luong,
                    g6_don_gia=g6_don_gia,
                    g6_thanh_tien=g6_thanh_tien,
                ))
                g6_dem_ct += 1
        db.session.commit()
        print(f"[OK] G6ChiTietDonHang — đã seed {g6_dem_ct} rows")

        # Tạo lịch sử đơn hàng
        g6_dem_ls = 0
        for g6_dh in g6_don_hangs:
            # Tạo bản ghi ban đầu
            db.session.add(G6LichSuDonHang(
                g6_ma_don_hang=g6_dh.g6_ma_don_hang,
                g6_trang_thai_cu=None,
                g6_trang_thai_moi="cho_xac_nhan",
                g6_ghi_chu="Đơn hàng mới",
                g6_nguoi_thay_doi=None,
                g6_ngay_tao=g6_dh.g6_ngay_tao,
            ))
            g6_dem_ls += 1

            # Thêm lịch sử theo trạng thái hiện tại
            if g6_dh.g6_trang_thai in ["da_xac_nhan", "dang_giao", "da_giao"]:
                db.session.add(G6LichSuDonHang(
                    g6_ma_don_hang=g6_dh.g6_ma_don_hang,
                    g6_trang_thai_cu="cho_xac_nhan",
                    g6_trang_thai_moi="da_xac_nhan",
                    g6_ghi_chu="Đã xác nhận đơn hàng",
                    g6_nguoi_thay_doi=g6_nguoi_dung.g6_ma_nguoi_dung if g6_nguoi_dung else None,
                    g6_ngay_tao=g6_dh.g6_ngay_tao + timedelta(hours=1),
                ))
                g6_dem_ls += 1

            if g6_dh.g6_trang_thai in ["dang_giao", "da_giao"]:
                db.session.add(G6LichSuDonHang(
                    g6_ma_don_hang=g6_dh.g6_ma_don_hang,
                    g6_trang_thai_cu="da_xac_nhan",
                    g6_trang_thai_moi="dang_giao",
                    g6_ghi_chu="Đã giao cho đơn vị vận chuyển",
                    g6_nguoi_thay_doi=g6_nguoi_dung.g6_ma_nguoi_dung if g6_nguoi_dung else None,
                    g6_ngay_tao=g6_dh.g6_ngay_tao + timedelta(hours=6),
                ))
                g6_dem_ls += 1

            if g6_dh.g6_trang_thai == "da_giao":
                db.session.add(G6LichSuDonHang(
                    g6_ma_don_hang=g6_dh.g6_ma_don_hang,
                    g6_trang_thai_cu="dang_giao",
                    g6_trang_thai_moi="da_giao",
                    g6_ghi_chu="Giao hàng thành công",
                    g6_nguoi_thay_doi=g6_nguoi_dung.g6_ma_nguoi_dung if g6_nguoi_dung else None,
                    g6_ngay_tao=g6_dh.g6_ngay_tao + timedelta(days=2),
                ))
                g6_dem_ls += 1

            if g6_dh.g6_trang_thai == "da_huy":
                db.session.add(G6LichSuDonHang(
                    g6_ma_don_hang=g6_dh.g6_ma_don_hang,
                    g6_trang_thai_cu="cho_xac_nhan",
                    g6_trang_thai_moi="da_huy",
                    g6_ghi_chu=g6_dh.g6_ghi_chu_noi_bo or "Đơn hàng bị hủy",
                    g6_nguoi_thay_doi=g6_nguoi_dung.g6_ma_nguoi_dung if g6_nguoi_dung else None,
                    g6_ngay_tao=g6_dh.g6_ngay_tao + timedelta(hours=2),
                ))
                g6_dem_ls += 1

        db.session.commit()
        print(f"[OK] G6LichSuDonHang — đã seed {g6_dem_ls} rows")

    # ------------------------------------------------------------------
    # 14. G6ThanhToan + G6HoaDon
    # ------------------------------------------------------------------
    from backend.app.models.g6_thanh_toan import G6ThanhToan, G6HoaDon
    if G6ThanhToan.query.first():
        print("[SKIP] G6ThanhToan — đã có dữ liệu")
    else:
        from datetime import timedelta
        import random

        g6_khach_hangs = G6KhachHang.query.all()

        g6_danh_sach_thanh_toan = [
            # Thanh toán thành công - Đơn hàng
            {
                "g6_ma_khach_hang": g6_khach_hangs[0].g6_ma_khach_hang if g6_khach_hangs else None,
                "g6_loai_giao_dich": "don_hang",
                "g6_so_tien": 2_160_000,
                "g6_phuong_thuc": "cod",
                "g6_trang_thai": "thanh_cong",
                "g6_ghi_chu": "Thanh toán đơn hàng #1",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=5),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=5),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[1].g6_ma_khach_hang if len(g6_khach_hangs) > 1 else None,
                "g6_loai_giao_dich": "don_hang",
                "g6_so_tien": 1_875_000,
                "g6_phuong_thuc": "bank_transfer",
                "g6_trang_thai": "thanh_cong",
                "g6_ma_giao_dich_cong": "VCB202604100001",
                "g6_ghi_chu": "Thanh toán đơn hàng #2",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=4),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=4),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[2].g6_ma_khach_hang if len(g6_khach_hangs) > 2 else None,
                "g6_loai_giao_dich": "don_hang",
                "g6_so_tien": 770_000,
                "g6_phuong_thuc": "momo",
                "g6_trang_thai": "thanh_cong",
                "g6_ma_giao_dich_cong": "MOMO202604100023",
                "g6_ghi_chu": "Thanh toán đơn hàng #3",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=3),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=3),
            },
            # Thanh toán thành công - Gói tập
            {
                "g6_ma_khach_hang": g6_khach_hangs[0].g6_ma_khach_hang if g6_khach_hangs else None,
                "g6_loai_giao_dich": "goi_tap",
                "g6_so_tien": 1_200_000,
                "g6_phuong_thuc": "vnpay",
                "g6_trang_thai": "thanh_cong",
                "g6_ma_giao_dich_cong": "VNPAY202604080045",
                "g6_ghi_chu": "Đăng ký gói 3 tháng",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=7),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=7),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[3].g6_ma_khach_hang if len(g6_khach_hangs) > 3 else None,
                "g6_loai_giao_dich": "goi_tap",
                "g6_so_tien": 4_200_000,
                "g6_phuong_thuc": "bank_transfer",
                "g6_trang_thai": "thanh_cong",
                "g6_ma_giao_dich_cong": "TCB202604050012",
                "g6_ghi_chu": "Đăng ký gói 1 năm",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=10),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=10),
            },
            # Chờ xử lý
            {
                "g6_ma_khach_hang": g6_khach_hangs[1].g6_ma_khach_hang if len(g6_khach_hangs) > 1 else None,
                "g6_loai_giao_dich": "don_hang",
                "g6_so_tien": 1_530_000,
                "g6_phuong_thuc": "vnpay",
                "g6_trang_thai": "cho_xu_ly",
                "g6_ghi_chu": "Đang chờ xác nhận từ VNPay",
                "g6_ngay_tao": datetime.utcnow() - timedelta(hours=2),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[4].g6_ma_khach_hang if len(g6_khach_hangs) > 4 else None,
                "g6_loai_giao_dich": "goi_tap",
                "g6_so_tien": 500_000,
                "g6_phuong_thuc": "momo",
                "g6_trang_thai": "cho_xu_ly",
                "g6_ghi_chu": "Đang chờ xác nhận từ MoMo",
                "g6_ngay_tao": datetime.utcnow() - timedelta(hours=1),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[2].g6_ma_khach_hang if len(g6_khach_hangs) > 2 else None,
                "g6_loai_giao_dich": "don_hang",
                "g6_so_tien": 2_280_000,
                "g6_phuong_thuc": "bank_transfer",
                "g6_trang_thai": "cho_xu_ly",
                "g6_ghi_chu": "Chờ xác nhận chuyển khoản",
                "g6_ngay_tao": datetime.utcnow() - timedelta(hours=5),
            },
            # Thất bại
            {
                "g6_ma_khach_hang": g6_khach_hangs[3].g6_ma_khach_hang if len(g6_khach_hangs) > 3 else None,
                "g6_loai_giao_dich": "don_hang",
                "g6_so_tien": 595_000,
                "g6_phuong_thuc": "vnpay",
                "g6_trang_thai": "that_bai",
                "g6_ghi_chu": "Giao dịch bị hủy do timeout",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=2),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[0].g6_ma_khach_hang if g6_khach_hangs else None,
                "g6_loai_giao_dich": "goi_tap",
                "g6_so_tien": 3_600_000,
                "g6_phuong_thuc": "momo",
                "g6_trang_thai": "that_bai",
                "g6_ghi_chu": "Số dư không đủ",
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=1),
            },
            # Hoàn tiền
            {
                "g6_ma_khach_hang": g6_khach_hangs[4].g6_ma_khach_hang if len(g6_khach_hangs) > 4 else None,
                "g6_loai_giao_dich": "don_hang",
                "g6_so_tien": 475_000,
                "g6_phuong_thuc": "momo",
                "g6_trang_thai": "hoan_tien",
                "g6_ma_giao_dich_cong": "MOMO-REFUND-001",
                "g6_ghi_chu": "Hoàn tiền do hết hàng",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=3),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=4),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[1].g6_ma_khach_hang if len(g6_khach_hangs) > 1 else None,
                "g6_loai_giao_dich": "goi_tap",
                "g6_so_tien": 500_000,
                "g6_phuong_thuc": "vnpay",
                "g6_trang_thai": "hoan_tien",
                "g6_ma_giao_dich_cong": "VNPAY-REFUND-002",
                "g6_ghi_chu": "Khách yêu cầu hủy gói",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=6),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=8),
            },
            # Thêm thanh toán dịch vụ và nạp điểm
            {
                "g6_ma_khach_hang": g6_khach_hangs[2].g6_ma_khach_hang if len(g6_khach_hangs) > 2 else None,
                "g6_loai_giao_dich": "dich_vu",
                "g6_so_tien": 300_000,
                "g6_phuong_thuc": "cod",
                "g6_trang_thai": "thanh_cong",
                "g6_ghi_chu": "Thuê PT 1 buổi",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=2),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=2),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[3].g6_ma_khach_hang if len(g6_khach_hangs) > 3 else None,
                "g6_loai_giao_dich": "nap_diem",
                "g6_so_tien": 1_000_000,
                "g6_phuong_thuc": "bank_transfer",
                "g6_trang_thai": "thanh_cong",
                "g6_ma_giao_dich_cong": "VCB202604120099",
                "g6_ghi_chu": "Nạp điểm tích lũy",
                "g6_ngay_thanh_toan": datetime.utcnow() - timedelta(days=1),
                "g6_ngay_tao": datetime.utcnow() - timedelta(days=1),
            },
            {
                "g6_ma_khach_hang": g6_khach_hangs[4].g6_ma_khach_hang if len(g6_khach_hangs) > 4 else None,
                "g6_loai_giao_dich": "dich_vu",
                "g6_so_tien": 150_000,
                "g6_phuong_thuc": "momo",
                "g6_trang_thai": "cho_xu_ly",
                "g6_ghi_chu": "Thuê tủ đồ 1 tháng",
                "g6_ngay_tao": datetime.utcnow() - timedelta(hours=3),
            },
        ]

        # Tạo thanh toán
        for g6_tt in g6_danh_sach_thanh_toan:
            db.session.add(G6ThanhToan(**g6_tt))
        db.session.commit()
        print(f"[OK] G6ThanhToan — đã seed {len(g6_danh_sach_thanh_toan)} rows")

        # Tạo hóa đơn cho các giao dịch thành công
        g6_thanh_toans = G6ThanhToan.query.filter_by(g6_trang_thai='thanh_cong').all()
        g6_dem_hd = 0
        for idx, g6_tt in enumerate(g6_thanh_toans):
            g6_tien_truoc_thue = int(float(g6_tt.g6_so_tien) / 1.1)
            g6_tien_thue = int(float(g6_tt.g6_so_tien)) - g6_tien_truoc_thue
            g6_so_hd = f"HD{datetime.now().strftime('%Y%m')}{str(idx + 1).zfill(4)}"

            db.session.add(G6HoaDon(
                g6_ma_thanh_toan=g6_tt.g6_ma_thanh_toan,
                g6_so_hoa_don=g6_so_hd,
                g6_tien_truoc_thue=g6_tien_truoc_thue,
                g6_tien_thue=g6_tien_thue,
                g6_tong_cong=int(float(g6_tt.g6_so_tien)),
                g6_ngay_xuat=g6_tt.g6_ngay_thanh_toan or datetime.utcnow(),
            ))
            g6_dem_hd += 1
        db.session.commit()
        print(f"[OK] G6HoaDon — đã seed {g6_dem_hd} rows")

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
