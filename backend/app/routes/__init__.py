def nqt_dang_ky_routes(app):
    from backend.app.routes.nqt_auth import nqt_auth_bp
    from backend.app.routes.nqt_cau_hinh import nqt_cau_hinh_bp
    from backend.app.routes.nqt_chi_nhanh import nqt_chi_nhanh_bp
    from backend.app.routes.nqt_nguoi_dung import nqt_nguoi_dung_bp
    from backend.app.routes.nqt_nhan_vien import nqt_nhan_vien_bp
    from backend.app.routes.nqt_hoi_vien import nqt_hoi_vien_bp
    from backend.app.routes.nqt_khach_hang import nqt_khach_hang_bp
    from backend.app.routes.nqt_don_hang import nqt_don_hang_bp
    from backend.app.routes.nqt_khuyen_mai import nqt_khuyen_mai_bp
    from backend.app.routes.nqt_thanh_toan import nqt_thanh_toan_bp
    from backend.app.routes.nqt_van_chuyen import nqt_van_chuyen_bp
    from backend.app.routes.nqt_blog import nqt_blog_bp
    from backend.app.routes.nqt_thong_bao import nqt_thong_bao_bp
    from backend.app.routes.nqt_admin_views import nqt_admin_views_bp
    from backend.app.routes.nqt_upload import nqt_upload_bp
    from backend.app.routes.nqt_bao_cao import nqt_bao_cao_bp
    from backend.app.routes.nqt_quan_tri import nqt_quan_tri_bp
    from backend.app.routes.nqt_public import nqt_public_bp
    from backend.app.routes.nqt_hoi_vien_auth import nqt_hv_auth_bp
    from backend.app.routes.nqt_phan_quyen import nqt_phan_quyen_bp
    from backend.app.routes.nqt_api_docs import nqt_api_docs_bp
    # nxv routes
    from backend.app.routes.nxv_huan_luyen_vien import nxv_huan_luyen_vien_bp
    from backend.app.routes.nxv_lop_hoc import nxv_lop_hoc_bp
    from backend.app.routes.nxv_dich_vu_phu import nxv_dich_vu_phu_bp
    from backend.app.routes.nxv_san_pham import nxv_san_pham_bp
    from backend.app.routes.nxv_danh_gia import nxv_danh_gia_bp
    from backend.app.routes.nxv_chuong_trinh_tap import nxv_chuong_trinh_tap_bp
    from backend.app.routes.nxv_bao_tri import nxv_bao_tri_bp
    from backend.app.routes.nxv_su_kien import nxv_su_kien_bp

    app.register_blueprint(nqt_auth_bp)
    app.register_blueprint(nqt_cau_hinh_bp)
    app.register_blueprint(nqt_chi_nhanh_bp)
    app.register_blueprint(nqt_nguoi_dung_bp)
    app.register_blueprint(nqt_nhan_vien_bp)
    app.register_blueprint(nqt_hoi_vien_bp)
    app.register_blueprint(nqt_khach_hang_bp)
    app.register_blueprint(nqt_don_hang_bp)
    app.register_blueprint(nqt_khuyen_mai_bp)
    app.register_blueprint(nqt_thanh_toan_bp)
    app.register_blueprint(nqt_van_chuyen_bp)
    app.register_blueprint(nqt_blog_bp)
    app.register_blueprint(nqt_thong_bao_bp)
    app.register_blueprint(nqt_admin_views_bp)
    app.register_blueprint(nqt_upload_bp)
    app.register_blueprint(nqt_bao_cao_bp)
    app.register_blueprint(nqt_quan_tri_bp)
    app.register_blueprint(nqt_public_bp)
    app.register_blueprint(nqt_hv_auth_bp)
    app.register_blueprint(nqt_phan_quyen_bp)
    app.register_blueprint(nqt_api_docs_bp)
    # nxv blueprints
    app.register_blueprint(nxv_huan_luyen_vien_bp)
    app.register_blueprint(nxv_lop_hoc_bp)
    app.register_blueprint(nxv_dich_vu_phu_bp)
    app.register_blueprint(nxv_san_pham_bp)
    app.register_blueprint(nxv_danh_gia_bp)
    app.register_blueprint(nxv_chuong_trinh_tap_bp)
    app.register_blueprint(nxv_bao_tri_bp)
    app.register_blueprint(nxv_su_kien_bp)
