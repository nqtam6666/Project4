import sys
import os

# Add the project root (the directory containing 'backend') to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db
from backend.app.models.g6_nguoi_dung import G6QuyenHan, G6VaiTro, G6NguoiDung, G6NguoiDungVaiTro

app = create_app()

PERMISSIONS = [
    # Nhóm Hội viên
    {'ten': 'Xem danh sách Hội viên', 'nhom': 'Hội viên'},
    {'ten': 'Thêm mới Hội viên', 'nhom': 'Hội viên'},
    {'ten': 'Chỉnh sửa Hội viên', 'nhom': 'Hội viên'},
    {'ten': 'Xóa Hội viên', 'nhom': 'Hội viên'},
    
    # Nhóm Đơn hàng
    {'ten': 'Xem danh sách Đơn hàng', 'nhom': 'Đơn hàng'},
    {'ten': 'Tạo Đơn hàng mới', 'nhom': 'Đơn hàng'},
    {'ten': 'Chỉnh sửa Đơn hàng', 'nhom': 'Đơn hàng'},
    {'ten': 'Xóa Đơn hàng', 'nhom': 'Đơn hàng'},

    # Nhóm Gói tập
    {'ten': 'Xem danh sách Gói tập', 'nhom': 'Gói tập'},
    {'ten': 'Thêm mới Gói tập', 'nhom': 'Gói tập'},
    {'ten': 'Chỉnh sửa Gói tập', 'nhom': 'Gói tập'},
    {'ten': 'Xóa Gói tập', 'nhom': 'Gói tập'},

    # Nhóm Sản phẩm
    {'ten': 'Xem danh sách Sản phẩm', 'nhom': 'Sản phẩm'},
    {'ten': 'Thêm mới Sản phẩm', 'nhom': 'Sản phẩm'},
    {'ten': 'Chỉnh sửa Sản phẩm', 'nhom': 'Sản phẩm'},
    {'ten': 'Xóa Sản phẩm', 'nhom': 'Sản phẩm'},

    # Nhóm Hệ thống
    {'ten': 'g6_quan_tri_he_thong', 'nhom': 'Hệ thống'},
    {'ten': 'Cấu hình giao diện', 'nhom': 'Hệ thống'},
]

ROLES = [
    {'ten': 'G6QuanTri', 'mota': 'Quản trị viên cấp cao nhất'},
    {'ten': 'G6QuanLy', 'mota': 'Quản lý cửa hàng / chi nhánh'},
    {'ten': 'G6HuanLuyenVien', 'mota': 'Huấn luyện viên cá nhân'},
    {'ten': 'G6LeTan', 'mota': 'Nhân viên lễ tân'},
]

def seed():
    with app.app_context():
        # 1. Seed Permissions
        print("Đang thêm danh sách quyền...")
        for p_data in PERMISSIONS:
            existing = G6QuyenHan.query.filter_by(g6_ten_quyen=p_data['ten']).first()
            if not existing:
                new_quyen = G6QuyenHan(
                    g6_ten_quyen=p_data['ten'],
                    g6_nhom_quyen=p_data['nhom']
                )
                db.session.add(new_quyen)
        
        # 2. Seed Roles
        print("Đang kiểm tra và thêm vai trò mặc định...")
        for r_data in ROLES:
            existing_role = G6VaiTro.query.filter_by(g6_ten_vai_tro=r_data['ten']).first()
            if not existing_role:
                new_role = G6VaiTro(
                    g6_ten_vai_tro=r_data['ten'],
                    g6_mo_ta=r_data['mota']
                )
                db.session.add(new_role)

        db.session.commit()
        print("✅ Hoàn tất Seed dữ liệu Phân Quyền!")

if __name__ == '__main__':
    seed()
