import sys
from backend.app import nqt_tao_app, db
from backend.app.models.g6_nguoi_dung import G6NguoiDung

# Fix unicode output for Windows terminal
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = nqt_tao_app()
with app.app_context():
    user = G6NguoiDung.query.filter_by(g6_ten_dang_nhap="doanquan").first()
    if user:
        print(f"User ID: {user.g6_ma_nguoi_dung}")
        print(f"User: {user.g6_ten_dang_nhap}")
        roles = [ndvt.g6_vai_tro.g6_ten_vai_tro for ndvt in user.g6_vai_tro]
        print(f"Roles: {roles}")
        
        all_perms = []
        for ndvt in user.g6_vai_tro:
            for vtq in ndvt.g6_vai_tro.g6_quyen:
                all_perms.append(vtq.g6_quyen.g6_ten_quyen)
        print(f"Permissions count: {len(all_perms)}")
        print(f"Unique Permissions: {list(set(all_perms))}")
    else:
        print("User 'doanquan' not found!")
