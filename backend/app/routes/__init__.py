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
