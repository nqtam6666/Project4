from backend.app import nqt_tao_app, db
from backend.app.models.g6_nguoi_dung import G6VaiTro, G6QuyenHan, G6VaiTroQuyen

app = nqt_tao_app()
with app.app_context():
    pt_role = G6VaiTro.query.filter_by(g6_ten_vai_tro="G6PT").first()
    if pt_role:
        print(f"Role: {pt_role.g6_ten_vai_tro}")
        mappings = G6VaiTroQuyen.query.filter_by(g6_ma_vai_tro=pt_role.g6_ma_vai_tro).all()
        print("Permissions:")
        for m in mappings:
            q = G6QuyenHan.query.get(m.g6_ma_quyen)
            if q:
                print(f" - {q.g6_ten_quyen}")
    else:
        print("PT role not found!")
