import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

# ── Fix encoding tiếng Việt trên SQL Server ──────────────
# Rule: mọi String/Text tự động dùng NVARCHAR thay vì VARCHAR
from sqlalchemy import String, Text
from sqlalchemy.ext.compiler import compiles

@compiles(String, "mssql")
def _compile_string_mssql(element, compiler, **kw):
    return compiler.visit_NVARCHAR(element, **kw)

@compiles(Text, "mssql")
def _compile_text_mssql(element, compiler, **kw):
    return "NVARCHAR(MAX)"
# ──────────────────────────────────────────────────────────

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    nqt_scheduler = BackgroundScheduler(timezone='Asia/Ho_Chi_Minh')
except ImportError:
    nqt_scheduler = None


def nqt_tao_app(nqt_moi_truong: str = None):
    from backend.config import nqt_cau_hinh_map

    app = Flask(__name__, template_folder='../../frontend/templates',
                static_folder='../../frontend/static')

    nqt_moi_truong = nqt_moi_truong or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(nqt_cau_hinh_map.get(nqt_moi_truong, nqt_cau_hinh_map['default']))

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    # Import models để Migrate nhận diện
    from backend.app.models import (  # noqa: F401
        g6_cau_hinh, g6_nguoi_dung, g6_chi_nhanh,
        g6_nhan_vien, g6_hoi_vien, g6_khach_hang,
        g6_don_hang, g6_khuyen_mai, g6_thanh_toan,
        g6_van_chuyen, g6_blog, g6_thong_bao, g6_xac_thuc,
        g6_huan_luyen_vien, g6_lop_hoc, g6_dich_vu_phu, g6_san_pham,
        nxv_danh_gia, nxv_chuong_trinh_tap, nxv_bao_tri, nxv_su_kien,
    )

    # Đăng ký blueprints
    from backend.app.routes import nqt_dang_ky_routes
    nqt_dang_ky_routes(app)

    # Khởi động APScheduler + đăng ký jobs
    if nqt_scheduler is not None:
        from backend.app.jobs.nqt_kiem_tra_het_han import nqt_dang_ky_jobs
        nqt_dang_ky_jobs(nqt_scheduler, app)
        if not nqt_scheduler.running:
            nqt_scheduler.start()
            import atexit
            atexit.register(lambda: nqt_scheduler.shutdown(wait=False))

    # CLI: flask seed
    from backend.app.seeds.nqt_seed import nqt_chay_seed, nqt_chay_drop_va_seed

    @app.cli.command('seed')
    def nqt_lenh_seed():
        """Seed dữ liệu mẫu vào database (idempotent)."""
        nqt_chay_seed()

    @app.cli.command('seed-fresh')
    def nqt_lenh_seed_fresh():
        """Drop toàn bộ bảng → tạo lại NVARCHAR → seed. Dùng khi bảng cũ bị VARCHAR."""
        nqt_chay_drop_va_seed()

    return app
