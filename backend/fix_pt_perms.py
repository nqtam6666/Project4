from backend.app import nqt_tao_app, db
from backend.app.models.g6_nguoi_dung import G6VaiTro, G6QuyenHan, G6VaiTroQuyen

app = nqt_tao_app()
with app.app_context():
    pt_role = G6VaiTro.query.filter_by(g6_ten_vai_tro="G6PT").first()
    if pt_role:
        new_perms = ["g6_xem_cau_hinh", "QL_KHO", "g6_xem_goi_tap"]
        for p_ten in new_perms:
            q = G6QuyenHan.query.filter_by(g6_ten_quyen=p_ten).first()
            if q:
                # Check if exists
                exists = G6VaiTroQuyen.query.filter_by(g6_ma_vai_tro=pt_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen).first()
                if not exists:
                    db.session.add(G6VaiTroQuyen(g6_ma_vai_tro=pt_role.g6_ma_vai_tro, g6_ma_quyen=q.g6_ma_quyen))
        db.session.commit()
        print("PT permissions updated!")
    else:
        print("PT role not found!")
