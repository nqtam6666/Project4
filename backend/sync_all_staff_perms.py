import sys
from backend.app import nqt_tao_app, db
from backend.app.models.g6_nguoi_dung import G6VaiTro, G6QuyenHan, G6VaiTroQuyen

# Fix unicode for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = nqt_tao_app()
with app.app_context():
    view_perms = ["XEM_BAO_CAO", "g6_xem_hoi_vien", "g6_xem_cau_hinh", "g6_xem_goi_tap", "QL_KHO", "QL_HOI_VIEN"]
    
    for p_ten in view_perms:
        if not G6QuyenHan.query.filter_by(g6_ten_quyen=p_ten).first():
            db.session.add(G6QuyenHan(g6_ten_quyen=p_ten, g6_nhom_quyen="Xem dữ liệu"))
    db.session.commit()

    target_roles = ["G6QuanTri", "G6QuanLy", "G6NhanVien", "G6PT"]
    for r_ten in target_roles:
        role = G6VaiTro.query.filter_by(g6_ten_vai_tro=r_ten).first()
        if role:
            print(f"Syncing perms for Role: {r_ten}")
            for p_ten in view_perms:
                q = G6QuyenHan.query.filter_by(g6_ten_quyen=p_ten).first()
                if q:
                    exists = G6VaiTroQuyen.query.filter_by(g6_ma_vai_tro=role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen).first()
                    if not exists:
                        db.session.add(G6VaiTroQuyen(g6_ma_vai_tro=role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen))
                        print(f"  + Added {p_ten}")
    
    db.session.commit()
    print("DONE! Permissions synced for all staff roles.")
