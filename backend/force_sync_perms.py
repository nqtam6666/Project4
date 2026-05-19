from backend.app import nqt_tao_app, db
from backend.app.models.g6_nguoi_dung import G6VaiTro, G6QuyenHan, G6VaiTroQuyen

app = nqt_tao_app()
with app.app_context():
    # 1. Danh sách quyền cần thiết
    all_needed_quyens = [
        ("XEM_BAO_CAO", "Thống kê"),
        ("g6_xem_hoi_vien", "Hội viên"),
        ("g6_checkin_hoi_vien", "Hội viên"),
        ("QL_HOI_VIEN", "Hội viên"),
        ("g6_xem_cau_hinh", "Hệ thống"),
        ("QL_KHO", "Kho hàng"),
        ("g6_xem_goi_tap", "Gói tập"),
        ("g6_xem_nhan_vien", "Nhân sự")
    ]
    
    for ten, nhom in all_needed_quyens:
        q = G6QuyenHan.query.filter_by(g6_ten_quyen=ten).first()
        if not q:
            db.session.add(G6QuyenHan(g6_ten_quyen=ten, g6_nhom_quyen=nhom))
            print(f"Created perm: {ten}")
    db.session.commit()

    # 2. Gán cho PT
    pt_role = G6VaiTro.query.filter_by(g6_ten_vai_tro="G6PT").first()
    if pt_role:
        pt_perms = ["XEM_BAO_CAO", "g6_xem_hoi_vien", "g6_checkin_hoi_vien", "QL_HOI_VIEN", "g6_xem_cau_hinh", "QL_KHO", "g6_xem_goi_tap"]
        for p_ten in pt_perms:
            q = G6QuyenHan.query.filter_by(g6_ten_quyen=p_ten).first()
            if q:
                exists = G6VaiTroQuyen.query.filter_by(g6_ma_vai_tro=pt_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen).first()
                if not exists:
                    db.session.add(G6VaiTroQuyen(g6_ma_vai_tro=pt_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen))
                    print(f"Mapped {p_ten} to PT")
        db.session.commit()
    
    # 3. Gán cho QuanLy (Full perms for now to be safe)
    ql_role = G6VaiTro.query.filter_by(g6_ten_vai_tro="G6QuanLy").first()
    if ql_role:
        all_qs = G6QuyenHan.query.all()
        for q in all_qs:
            exists = G6VaiTroQuyen.query.filter_by(g6_ma_vai_tro=ql_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen).first()
            if not exists:
                db.session.add(G6VaiTroQuyen(g6_ma_vai_tro=ql_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen))
        db.session.commit()
        print("Updated QuanLy permissions")

    print("DONE! Please RELOGIN on the website.")
