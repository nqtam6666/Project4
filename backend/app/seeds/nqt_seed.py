"""
Seed dữ liệu mẫu đầy đủ cho G6 Gym Management System.
Bao gồm 4 thành viên nhóm: Nguyễn Quang Tâm, Nguyễn Hoài Nam, Đoàn Anh Quân, Nguyễn Xuân Vinh.
"""

from datetime import date, time, datetime, timedelta
import bcrypt
import random

def nqt_chay_seed():
    from backend.app import db
    from backend.app.models.g6_cau_hinh import G6CauHinh
    from backend.app.models.g6_nguoi_dung import G6VaiTro, G6QuyenHan, G6NguoiDung, G6NguoiDungVaiTro
    from backend.app.models.g6_chi_nhanh import G6ChiNhanh, G6ThietBi
    from backend.app.models.g6_nhan_vien import G6NhanVien
    from backend.app.models.g6_huan_luyen_vien import G6HuanLuyenVien, G6GoiPT
    from backend.app.models.g6_hoi_vien import G6GoiTap, G6DangKyGoiTap, G6ChiSoCoThe
    from backend.app.models.g6_khach_hang import G6HangThanhVien, G6DiemKhachHang
    from backend.app.models.g6_san_pham import G6DanhMucSanPham, G6ThuongHieu, G6SanPham, G6BienTheSanPham
    from backend.app.models.g6_blog import G6DanhMucBaiViet, G6BaiViet
    from backend.app.models.g6_dich_vu_phu import G6DichVuPhu
    from backend.app.models.g6_lop_hoc import G6LopHoc, G6LichLopHoc, G6DatChoLopHoc
    from backend.app.models.nxv_su_kien import NxvSuKien, NxvDangKySuKien
    from backend.app.models.g6_van_chuyen import G6DonViVanChuyen
    from backend.app.models.g6_thanh_toan import G6ThanhToan, G6HoaDon
    from backend.app.models.g6_don_hang import G6DonHang, G6ChiTietDonHang
    from backend.app.models.g6_thong_bao import G6ThongBao
    from backend.app.models.nxv_bao_tri import NxvLichSuBaoTri
    from backend.app.models.nxv_chuong_trinh_tap import NxvChuongTrinhTapLuyen, NxvBaiTapTrongNgay
    from backend.app.models.nxv_danh_gia import NxvDanhGiaHLV, NxvDanhGiaLopHoc
    from backend.app.models.g6_nguoi_dung import G6VaiTroQuyen

    print("=== Bat dau seed du lieu toan dien ===")
    db.create_all()

    # 1. Cau hinh
    if not G6CauHinh.query.first():
        configs = [
            ("g6_ten_website", "IronCore Gym", "string", "website", "Tên website"),
            ("g6_jwt_het_han_phut", "1440", "int", "security", "JWT expiration (mins)"),
            ("g6_phi_ship_mac_dinh", "30000", "int", "shipping", "Default shipping fee"),
        ]
        for k, v, t, g, d in configs:
            db.session.add(G6CauHinh(g6_khoa=k, g6_gia_tri=v, g6_kieu_du_lieu=t, g6_nhom=g, g6_mo_ta=d))
        db.session.commit()
        print("[OK] Cau hinh")

    # 2. Vai tro & Quyen han
    if not G6VaiTro.query.first():
        vaitros = [
            ("G6QuanTri", "Quản trị hệ thống"),
            ("G6QuanLy", "Quản lý chi nhánh"),
            ("G6NhanVien", "Nhân viên bán hàng"),
            ("G6PT", "Huấn luyện viên (PT)"),
            ("G6HoiVien", "Hội viên"),
            ("G6KhachHang", "Khách hàng online")
        ]
        for ten, mo_ta in vaitros:
            db.session.add(G6VaiTro(g6_ten_vai_tro=ten, g6_mo_ta=mo_ta))
        
        quyens = [
            # Thống kê & Báo cáo
            ("XEM_BAO_CAO", "Thống kê"),
            ("g6_xem_bao_cao", "Thống kê"),
            
            # Nhân sự
            ("QL_NHAN_VIEN", "Quản lý nhân sự"),
            ("g6_xem_nhan_vien", "Quản lý nhân sự"),
            ("g6_tao_nhan_vien", "Quản lý nhân sự"),
            ("g6_sua_nhan_vien", "Quản lý nhân sự"),
            ("g6_xoa_nhan_vien", "Quản lý nhân sự"),
            
            # Hội viên
            ("QL_HOI_VIEN", "Quản lý hội viên"),
            ("g6_xem_hoi_vien", "Quản lý hội viên"),
            ("g6_tao_hoi_vien", "Quản lý hội viên"),
            ("g6_sua_hoi_vien", "Quản lý hội viên"),
            ("g6_xoa_hoi_vien", "Quản lý hội viên"),
            ("g6_checkin_hoi_vien", "Quản lý hội viên"),
            
            # Sản phẩm & Kho
            ("QL_KHO", "Quản lý kho hàng"),
            ("g6_xem_san_pham", "Quản lý kho hàng"),
            ("g6_tao_san_pham", "Quản lý kho hàng"),
            ("g6_sua_san_pham", "Quản lý kho hàng"),
            ("g6_xoa_san_pham", "Quản lý kho hàng"),
            
            # Hệ thống
            ("g6_quan_tri_he_thong", "Hệ thống"),
            ("QL_HE_THONG", "Hệ thống"),
            ("g6_xem_cau_hinh", "Hệ thống"),
            ("g6_sua_cau_hinh", "Hệ thống"),
            
            # Gói tập
            ("g6_xem_goi_tap", "Gói tập"),
        ]
        for ten, nhom in quyens:
            db.session.add(G6QuyenHan(g6_ten_quyen=ten, g6_nhom_quyen=nhom))
        
        db.session.commit()
        
        # --- Map quyen cho cac vai tro ---
        
        # 1. Admin: Toàn quyền
        admin_role = G6VaiTro.query.filter_by(g6_ten_vai_tro="G6QuanTri").first()
        all_quyens = G6QuyenHan.query.all()
        for q in all_quyens:
            db.session.add(G6VaiTroQuyen(g6_ma_vai_tro=admin_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen))
            
        # 2. PT (Huấn luyện viên): Chỉ xem dashboard và hội viên
        pt_role = G6VaiTro.query.filter_by(g6_ten_vai_tro="G6PT").first()
        if pt_role:
            pt_perms = ["XEM_BAO_CAO", "g6_xem_hoi_vien", "g6_checkin_hoi_vien", "QL_HOI_VIEN", "g6_xem_cau_hinh", "QL_KHO", "g6_xem_goi_tap"]
            for p_ten in pt_perms:
                q = G6QuyenHan.query.filter_by(g6_ten_quyen=p_ten).first()
                if q:
                    exists = G6VaiTroQuyen.query.filter_by(g6_ma_vai_tro=pt_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen).first()
                    if not exists:
                        db.session.add(G6VaiTroQuyen(g6_ma_vai_tro=pt_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen))

        # 3. Quản lý: Hầu hết các quyền trừ hệ thống
        ql_role = G6VaiTro.query.filter_by(g6_ten_vai_tro="G6QuanLy").first()
        if ql_role:
            for q in all_quyens:
                if q.g6_nhom_quyen != "Hệ thống":
                    exists = G6VaiTroQuyen.query.filter_by(g6_ma_vai_tro=ql_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen).first()
                    if not exists:
                        db.session.add(G6VaiTroQuyen(g6_ma_vai_tro=ql_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen))

        db.session.commit()
        print("[OK] Vai tro & Quyen han (Mapped roles)")

    # 3. Chi nhanh & Thiet bi
    if not G6ChiNhanh.query.first():
        cn = G6ChiNhanh(
            g6_ten_chi_nhanh="IronCore Cầu Giấy", 
            g6_dia_chi="123 Xuân Thủy, Cầu Giấy, Hà Nội", 
            g6_thanh_pho="Hà Nội",
            g6_hotline="0987654321",
            g6_suc_chua_toi_da=200
        )
        db.session.add(cn)
        db.session.flush()
        
        # Thiet bi
        db.session.add(G6ThietBi(
            g6_ma_chi_nhanh=cn.g6_ma_chi_nhanh, g6_ten_thiet_bi="Máy chạy bộ Matrix T7", 
            g6_thuong_hieu="Matrix", g6_trang_thai="hoat_dong"
        ))
        db.session.commit()
        print("[OK] Chi nhanh & Thiet bi")
    
    cn = G6ChiNhanh.query.first()
    ma_cn = cn.g6_ma_chi_nhanh

    # 4. Nguoi dung (4 thanh vien nhom)
    if not G6NguoiDung.query.filter_by(g6_ten_dang_nhap="quangtam").first():
        mk = bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode()
        members = [
            {"un": "quangtam", "name": "Nguyễn Quang Tâm", "role": "G6QuanTri", "is_nv": True},
            {"un": "hoainam", "name": "Nguyễn Hoài Nam", "role": "G6QuanLy", "is_nv": True},
            {"un": "doanquan", "name": "Đoàn Anh Quân", "role": "G6PT", "is_nv": True},
            {"un": "xuanvinh", "name": "Nguyễn Xuân Vinh", "role": "G6NhanVien", "is_nv": True},
        ]
        for m in members:
            nd = G6NguoiDung(
                g6_ten_dang_nhap=m["un"], g6_mat_khau=mk, g6_ho_ten=m["name"],
                g6_la_nhan_vien=m["is_nv"], g6_ma_chi_nhanh=ma_cn, g6_la_hoat_dong=True
            )
            db.session.add(nd)
            db.session.flush()
            vt = G6VaiTro.query.filter_by(g6_ten_vai_tro=m["role"]).first()
            if vt:
                db.session.add(G6NguoiDungVaiTro(g6_ma_nguoi_dung=nd.g6_ma_nguoi_dung, g6_ma_vai_tro=vt.g6_ma_vai_tro))
            
            # Tao ban ghi NhanVien
            nv = G6NhanVien(
                g6_ma_nguoi_dung=nd.g6_ma_nguoi_dung, g6_ma_chi_nhanh=ma_cn, 
                g6_ho_ten=nd.g6_ho_ten, g6_luong_co_ban=15000000, g6_ngay_vao_lam=date.today()
            )
            db.session.add(nv)
            db.session.flush()
            
            # Neu la PT, tao ban ghi HLV
            if m["role"] == "G6PT":
                hlv = G6HuanLuyenVien(
                    g6_ma_nhan_vien=nv.g6_ma_nhan_vien, g6_ma_chi_nhanh=ma_cn,
                    g6_chuyen_mon="Gym, Bodybuilding, Fitness", g6_so_nam_kinh_nghiem=5,
                    g6_tieu_su="Chuyên gia hình thể với 5 năm kinh nghiệm."
                )
                db.session.add(hlv)
                db.session.flush()
                # Goi PT
                db.session.add(G6GoiPT(
                    g6_ma_hlv=hlv.g6_ma_hlv, g6_ten_goi="PT 1:1 12 Buổi", 
                    g6_so_buoi=12, g6_thoi_luong_buoi=60, g6_gia=3600000
                ))

        db.session.commit()
        print("[OK] Nguoi dung & Nhan vien (4 thanh vien)")

    # 5. Goi tap & Dich vu phu
    if not G6GoiTap.query.first():
        gois = [
            ("Gói Classic 1 Tháng", 30, 500000),
            ("Gói Silver 6 Tháng", 180, 2500000),
            ("Gói Gold 12 Tháng", 365, 4500000),
        ]
        for ten, ngay, gia in gois:
            db.session.add(G6GoiTap(g6_ten_goi=ten, g6_so_ngay=ngay, g6_gia=gia))
        
        db.session.add(G6DichVuPhu(
            g6_ma_chi_nhanh=ma_cn, g6_ten_dich_vu="Sauna & Steam", 
            g6_loai_dich_vu="relaxation", g6_gia_theo_luot=50000
        ))
        db.session.commit()
        
        # Dang ky goi tap cho mot vai nguoi (gia su co them users)
        nd_vinh = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="xuanvinh").first()
        goi_classic = G6GoiTap.query.filter_by(g6_ten_goi="Gói Classic 1 Tháng").first()
        if nd_vinh and goi_classic:
            db.session.add(G6DangKyGoiTap(
                g6_ma_nguoi_dung=nd_vinh.g6_ma_nguoi_dung, g6_ma_goi_tap=goi_classic.g6_ma_goi_tap,
                g6_ma_chi_nhanh=ma_cn, g6_ngay_bat_dau=date.today(), g6_ngay_het_han=date.today()+timedelta(days=30),
                g6_gia_thuc_te=goi_classic.g6_gia
            ))
            db.session.add(G6ChiSoCoThe(
                g6_ma_nguoi_dung=nd_vinh.g6_ma_nguoi_dung, g6_ngay_do=date.today(),
                g6_can_nang=75.5, g6_chieu_cao=175.0, g6_chi_so_bmi=24.6
            ))
        db.session.commit()
        print("[OK] Goi tap, Dang ky & Chi so co the")

    # 6. San pham & Kho
    if not G6DanhMucSanPham.query.first():
        dm = G6DanhMucSanPham(g6_ten_danh_muc="Thực phẩm bổ sung", g6_slug="thuc-pham-bo-sung")
        db.session.add(dm)
        th = G6ThuongHieu(g6_ten_thuong_hieu="IronMax", g6_slug="ironmax")
        db.session.add(th)
        db.session.flush()
        
        sp = G6SanPham(
            g6_ma_danh_muc=dm.g6_ma_danh_muc, g6_ma_thuong_hieu=th.g6_ma_thuong_hieu,
            g6_ten_san_pham="Whey Protein Gold", g6_slug="whey-protein-gold",
            g6_mo_ta_ngan="Sản phẩm tăng cơ chất lượng cao."
        )
        db.session.add(sp)
        db.session.flush()
        
        db.session.add(G6BienTheSanPham(
            g6_ma_san_pham=sp.g6_ma_san_pham, g6_sku="WHEY-G-01", 
            g6_ten_bien_the="Hộp 2kg - Socola", g6_gia=1200000, g6_la_mac_dinh=True
        ))
        
        db.session.add(G6DonViVanChuyen(g6_ten="Giao Hàng Nhanh", g6_ma="GHN"))
        db.session.commit()
        print("[OK] San pham & Van chuyen")

        db.session.add(G6DanhMucBaiViet(g6_ten="Kiến thức tập luyện", g6_slug="kien-thuc-tap-luyen"))
        db.session.commit()
        
        dm_blog = G6DanhMucBaiViet.query.first()
        nd_tam = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="quangtam").first()
        if dm_blog and nd_tam:
            db.session.add(G6BaiViet(
                g6_ma_danh_muc=dm_blog.g6_ma_danh_muc, g6_tieu_de="Cách tập Squat đúng cách",
                g6_slug="cach-tap-squat-dung-cach", g6_noi_dung="Nội dung hướng dẫn chi tiết...",
                g6_tac_gia=nd_tam.g6_ma_nguoi_dung, g6_trang_thai="da_xuat_ban"
            ))

        db.session.add(NxvSuKien(
            nxv_ma_chi_nhanh=ma_cn, nxv_ten="Thử thách 7 ngày Squat", 
            nxv_ngay_bat_dau=datetime.now(), nxv_ngay_ket_thuc=datetime.now()+timedelta(days=7),
            nxv_mo_ta="Tham gia thử thách để nhận quà hấp dẫn."
        ))
        db.session.commit()
        
        # Loyalty
        if not G6HangThanhVien.query.first():
            db.session.add(G6HangThanhVien(g6_ten_hang="Đồng", g6_diem_toi_thieu=0, g6_he_so_tich_diem=1.0))
            db.session.add(G6HangThanhVien(g6_ten_hang="Bạc", g6_diem_toi_thieu=1000, g6_he_so_tich_diem=1.1))
            db.session.commit()
            
        print("[OK] Blog, Su kien & Loyalty")

    # 8. Lop hoc
    if not G6LopHoc.query.first():
        db.session.add(G6LopHoc(g6_ma_chi_nhanh=ma_cn, g6_ten_lop="Yoga Flow", g6_loai_lop="yoga"))
        db.session.commit()
        
        lop = G6LopHoc.query.first()
        hlv = G6HuanLuyenVien.query.first()
        if lop and hlv:
            db.session.add(G6LichLopHoc(
                g6_ma_lop_hoc=lop.g6_ma_lop_hoc, g6_ma_hlv=hlv.g6_ma_hlv,
                g6_thu_trong_tuan=1, g6_gio_bat_dau=time(8,0), g6_thoi_luong=60,
                g6_ngay_ap_dung_tu=date.today()
            ))
            db.session.commit()
            
            lich = G6LichLopHoc.query.first()
            nd_nam = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="hoainam").first()
            if lich and nd_nam:
                db.session.add(G6DatChoLopHoc(
                    g6_ma_lich_lop=lich.g6_ma_lich_lop, g6_ma_nguoi_dung=nd_nam.g6_ma_nguoi_dung,
                    g6_ngay_tap=date.today()
                ))
        db.session.commit()
        print("[OK] Lop hoc & Lich hoc")

    # 9. E-commerce: Don hang & Thanh toan
    if not G6DonHang.query.first():
        nd_vinh = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="xuanvinh").first()
        if nd_vinh:
            dh = G6DonHang(
                g6_ma_nguoi_dung=nd_vinh.g6_ma_nguoi_dung, g6_ho_ten_nguoi_nhan=nd_vinh.g6_ho_ten,
                g6_so_dien_thoai="0912345678", g6_dia_chi_giao_hang="123 ABC, Ha Noi",
                g6_tong_tien_hang=1200000, g6_tong_thanh_toan=1200000, g6_trang_thai="cho_xac_nhan"
            )
            db.session.add(dh)
            db.session.flush()
            
            bt = G6BienTheSanPham.query.first()
            if bt:
                db.session.add(G6ChiTietDonHang(
                    g6_ma_don_hang=dh.g6_ma_don_hang, g6_ma_bien_the=bt.g6_ma_bien_the,
                    g6_ten_san_pham="Sản phẩm mẫu", g6_so_luong=1, g6_don_gia=1200000, g6_thanh_tien=1200000
                ))
            
            tt = G6ThanhToan(
                g6_ma_nguoi_dung=nd_vinh.g6_ma_nguoi_dung, g6_loai_giao_dich="thanh_toan_don_hang",
                g6_so_tien=1200000, g6_phuong_thuc="cod", g6_trang_thai="cho_xu_ly"
            )
            db.session.add(tt)
        db.session.commit()
        print("[OK] Don hang & Thanh toan")

    # 10. Thong bao & Khac
    if not G6ThongBao.query.first():
        nd_tam = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="quangtam").first()
        if nd_tam:
            db.session.add(G6ThongBao(
                g6_tieu_de="Chào mừng", g6_noi_dung="Chào mừng bạn đến với hệ thống!",
                g6_ma_nguoi_nhan=nd_tam.g6_ma_nguoi_dung, g6_loai="in_app"
            ))
        db.session.commit()
        print("[OK] Thong bao")

    print("=== Hoan tat seed du lieu ===")

def nqt_chay_drop_va_seed():
    from backend.app import db
    db.drop_all()
    nqt_chay_seed()

if __name__ == "__main__":
    nqt_chay_seed()
