import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import db, nqt_tao_app
from backend.app.models import G6DichVuPhu, G6LopHoc, G6CauHinh, G6GoiTap, G6ChiNhanh

app = nqt_tao_app()
with app.app_context():
    # 0. Ensure a branch exists
    branch = G6ChiNhanh.query.first()
    if not branch:
        branch = G6ChiNhanh(g6_ten_chi_nhanh="IRONCORE FLAGSHIP", g6_dia_chi="123 Luxury Blvd, Q1, TP.HCM", g6_so_dien_thoai="0901234567")
        db.session.add(branch)
        db.session.flush()

    # 1. Add Services
    if G6DichVuPhu.query.count() == 0:
        s1 = G6DichVuPhu(g6_ma_chi_nhanh=branch.g6_ma_chi_nhanh, g6_ten_dich_vu="Sauna & Cryotherapy", g6_loai_dich_vu="Recovery", g6_mo_ta="Phục hồi cơ bắp đỉnh cao với công nghệ lạnh và xông hơi hồng ngoại.")
        s2 = G6DichVuPhu(g6_ma_chi_nhanh=branch.g6_ma_chi_nhanh, g6_ten_dich_vu="VIP Lounge", g6_loai_dich_vu="Social", g6_mo_ta="Không gian thư giãn đẳng cấp với thức uống dinh dưỡng miễn phí.")
        s3 = G6DichVuPhu(g6_ma_chi_nhanh=branch.g6_ma_chi_nhanh, g6_ten_dich_vu="Private Pool", g6_loai_dich_vu="Leisure", g6_mo_ta="Hồ bơi nước tràn chuẩn Olympic, chỉ dành riêng cho hội viên Elite.")
        db.session.add_all([s1, s2, s3])
        print("Added 3 services.")

    # 2. Add Classes
    if G6LopHoc.query.count() <= 1:
        c1 = G6LopHoc(g6_ma_chi_nhanh=branch.g6_ma_chi_nhanh, g6_ten_lop="Iron Boxing", g6_loai_lop="Boxing", g6_mo_ta="Rèn luyện bản lĩnh và phản xạ với các võ sĩ chuyên nghiệp.", g6_hinh_anh="https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?q=80&w=2070")
        c2 = G6LopHoc(g6_ma_chi_nhanh=branch.g6_ma_chi_nhanh, g6_ten_lop="Zen Yoga", g6_loai_lop="Yoga", g6_mo_ta="Cân bằng tâm trí và cơ thể trong không gian tĩnh lặng, sang trọng.", g6_hinh_anh="https://images.unsplash.com/photo-1518611012118-2960c8bad84a?q=80&w=2070")
        db.session.add_all([c1, c2])
        print("Added 2 classes.")

    # 3. Add Config Slogan if missing
    slogan = G6CauHinh.query.filter_by(g6_khoa='g6_slogan').first()
    if not slogan:
        db.session.add(G6CauHinh(g6_khoa='g6_slogan', g6_gia_tri='Forge Your Legacy', g6_nhom='landing_page', g6_mo_ta='Landing page slogan'))
        print("Added slogan config.")
    
    # 4. Ensure some packages are featured
    pkgs = G6GoiTap.query.all()
    if pkgs:
        for p in pkgs:
            if 'Elite' in p.g6_ten_goi or 'Pro' in p.g6_ten_goi:
                p.g6_la_noi_bat = True
        print("Updated featured packages.")

    db.session.commit()
    print("Seeding completed successfully.")
