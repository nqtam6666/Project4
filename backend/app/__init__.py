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
        nqt_cau_hinh, nqt_nguoi_dung, nqt_chi_nhanh,
        nqt_nhan_vien, nqt_hoi_vien, nqt_khach_hang,
        nqt_don_hang, nqt_khuyen_mai, nqt_thanh_toan,
        nqt_van_chuyen, nqt_blog, nqt_thong_bao, nqt_xac_thuc,
    )

    # Đăng ký blueprints
    from backend.app.routes import nqt_dang_ky_routes
    nqt_dang_ky_routes(app)

    # CLI: flask seed
    from backend.app.seeds.nqt_seed import nqt_chay_seed

    @app.cli.command('seed')
    def nqt_lenh_seed():
        """Seed dữ liệu mẫu vào database (idempotent)."""
        nqt_chay_seed()

    return app
