"""
Seed du lieu mau cho G6 Gym Management System (Cau truc G6NguoiDung hop nhat).
Idempotent: moi nhom kiem tra xem da co du lieu chua truoc khi insert.

Chay qua Flask CLI:
    flask seed

Hoac chay truc tiep:
    python -m backend.app.seeds.nqt_seed
"""

from datetime import date, time, datetime, timedelta
import bcrypt
import uuid
import random

def nqt_chay_seed():
    from backend.app import db
    from backend.app.models.g6_cau_hinh import G6CauHinh
    from backend.app.models.g6_nguoi_dung import (
        G6VaiTro, G6QuyenHan, G6NguoiDung,
        G6NguoiDungVaiTro, G6VaiTroQuyen,
    )
    from backend.app.models.g6_chi_nhanh import G6ChiNhanh, G6ThietBi
    from backend.app.models.g6_nhan_vien import G6NhanVien
    from backend.app.models.g6_hoi_vien import G6GoiTap, G6DangKyGoiTap, G6DiemDanh, G6ChiSoCoThe
    from backend.app.models.g6_khach_hang import G6HangThanhVien, G6DiemKhachHang
    from backend.app.models.g6_don_hang import G6DonHang, G6ChiTietDonHang

    print("=== Bat dau seed du lieu ===")

    db.create_all()
    print("[INFO] Da kiem tra/tao schema database")

    # 1. G6CauHinh
    if G6CauHinh.query.first():
        print("[SKIP] G6CauHinh - da co du lieu")
    else:
        g6_danh_sach_cau_hinh = [
            ("g6_ten_website", "IronCore Gym", "string", "website", "Ten website"),
            ("g6_jwt_het_han_phut", "60", "int", "security", "JWT access token het han"),
            ("g6_so_lan_dang_nhap_sai", "5", "int", "security", "So lan dang nhap sai toi da"),
        ]
        for g6_nd in g6_danh_sach_cau_hinh:
            db.session.add(G6CauHinh(g6_khoa=g6_nd[0], g6_gia_tri=g6_nd[1], g6_kieu_du_lieu=g6_nd[2], g6_nhom=g6_nd[3], g6_mo_ta=g6_nd[4]))
        db.session.commit()
        print("[OK] G6CauHinh")

    # 2. G6VaiTro
    if G6VaiTro.query.first():
        print("[SKIP] G6VaiTro")
    else:
        vaitros = [("G6QuanTri", "Quan tri"), ("G6QuanLy", "Quan ly"), ("G6NhanVien", "Nhan vien"), ("G6HoiVien", "Hoi vien"), ("G6KhachHang", "Khach hang")]
        for ten, mo_ta in vaitros:
            db.session.add(G6VaiTro(g6_ten_vai_tro=ten, g6_mo_ta=mo_ta))
        db.session.commit()
        print("[OK] G6VaiTro")

    # 3. G6ChiNhanh
    if G6ChiNhanh.query.first():
        print("[SKIP] G6ChiNhanh")
    else:
        db.session.add(G6ChiNhanh(g6_ten_chi_nhanh="IronCore Cau Giay", g6_dia_chi="123 Xuan Thuy", g6_thanh_pho="Ha Noi", g6_suc_chua_toi_da=100))
        db.session.commit()
        print("[OK] G6ChiNhanh")

    g6_cn_1 = G6ChiNhanh.query.first()
    g6_ma_cn = g6_cn_1.g6_ma_chi_nhanh if g6_cn_1 else 1

    # 4. G6NguoiDung
    if G6NguoiDung.query.first():
        print("[SKIP] G6NguoiDung")
    else:
        mat_khau_hash = bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode()
        users = [
            {"g6_ten_dang_nhap": "quangtam", "g6_ho_ten": "Nguyen Quang Tam", "g6_la_nhan_vien": True},
            {"g6_ten_dang_nhap": "hoainam", "g6_ho_ten": "Nguyen Hoai Nam", "g6_la_nhan_vien": True},
            {"g6_ten_dang_nhap": "hoamember", "g6_ho_ten": "Nguyen Thi Hoa", "g6_la_hoi_vien": True, "g6_ma_qr": "QR-HOA-001"},
            {"g6_ten_dang_nhap": "vinhkhach", "g6_ho_ten": "Le Xuan Vinh", "g6_la_khach_hang": True},
        ]
        for u in users:
            nd = G6NguoiDung(
                g6_ten_dang_nhap=u["g6_ten_dang_nhap"],
                g6_mat_khau=mat_khau_hash,
                g6_ho_ten=u["g6_ho_ten"],
                g6_la_nhan_vien=u.get("g6_la_nhan_vien", False),
                g6_la_hoi_vien=u.get("g6_la_hoi_vien", False),
                g6_la_khach_hang=u.get("g6_la_khach_hang", False),
                g6_ma_qr=u.get("g6_ma_qr"),
                g6_ma_chi_nhanh=g6_ma_cn,
                g6_ngay_dang_ky=date.today()
            )
            db.session.add(nd)
        db.session.commit()
        print("[OK] G6NguoiDung")

    # 5. G6NhanVien
    if G6NhanVien.query.first():
        print("[SKIP] G6NhanVien")
    else:
        nd_tam = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="quangtam").first()
        if nd_tam:
            db.session.add(G6NhanVien(g6_ma_nguoi_dung=nd_tam.g6_ma_nguoi_dung, g6_ma_chi_nhanh=g6_ma_cn, g6_ho_ten=nd_tam.g6_ho_ten, g6_luong_co_ban=20000000))
        db.session.commit()
        print("[OK] G6NhanVien")

    # 6. G6GoiTap
    if G6GoiTap.query.first():
        print("[SKIP] G6GoiTap")
    else:
        goi = G6GoiTap(g6_ten_goi="Goi VIP 1 Thang", g6_so_ngay=30, g6_gia=500000)
        db.session.add(goi)
        db.session.commit()
        
        nd_hoa = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="hoamember").first()
        if nd_hoa:
            db.session.add(G6DangKyGoiTap(
                g6_ma_nguoi_dung=nd_hoa.g6_ma_nguoi_dung, 
                g6_ma_goi_tap=goi.g6_ma_goi_tap, 
                g6_ma_chi_nhanh=g6_ma_cn,
                g6_ngay_bat_dau=date.today(), 
                g6_ngay_het_han=date.today()+timedelta(days=30), 
                g6_gia_thuc_te=500000
            ))
        db.session.commit()
        print("[OK] G6GoiTap & DangKy")

    # 7. HangThanhVien & Diem
    if G6HangThanhVien.query.first():
        print("[SKIP] G6HangThanhVien")
    else:
        hang = G6HangThanhVien(g6_ten_hang="Dong", g6_diem_toi_thieu=0)
        db.session.add(hang)
        db.session.commit()
        
        nd_vinh = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="vinhkhach").first()
        if nd_vinh:
            db.session.add(G6DiemKhachHang(g6_ma_nguoi_dung=nd_vinh.g6_ma_nguoi_dung, g6_tong_diem=100, g6_diem_kha_dung=100, g6_ma_hang=hang.g6_ma_hang))
        db.session.commit()
        print("[OK] HangThanhVien & Diem")

    # 8. DonHang
    if G6DonHang.query.first():
        print("[SKIP] G6DonHang")
    else:
        nd_vinh = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="vinhkhach").first()
        if nd_vinh:
            db.session.add(G6DonHang(
                g6_ma_nguoi_dung=nd_vinh.g6_ma_nguoi_dung, 
                g6_ho_ten_nguoi_nhan="Le Xuan Vinh", 
                g6_so_dien_thoai="0912345678", 
                g6_dia_chi_giao_hang="Ha Noi", 
                g6_tong_tien_hang=1500000,
                g6_tong_thanh_toan=1500000, 
                g6_trang_thai="da_giao"
            ))
        db.session.commit()
        print("[OK] G6DonHang")

    print("=== Hoan tat seed du lieu ===")

def nqt_chay_drop_va_seed():
    from backend.app import db
    print("=== Dang DROP ALL tables ===")
    db.drop_all()
    print("[OK] Da drop")
    nqt_chay_seed()

if __name__ == "__main__":
    nqt_chay_seed()
