import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def _nqt_tao_pyodbc_connection():
    """Tạo pyodbc connection với encoding UTF-16-LE cho tiếng Việt."""
    driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server').replace('+', ' ')
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={os.getenv('DB_SERVER', 'localhost')};"
        f"DATABASE={os.getenv('DB_NAME', 'nqtam_project4')};"
        f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION', 'yes')};"
    )
    conn = pyodbc.connect(conn_str)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-16-le')
    conn.setencoding(encoding='utf-16-le')
    return conn


class NqtCauHinhFlask:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    # Dùng dialect mssql+pyodbc:// với creator function
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'creator': _nqt_tao_pyodbc_connection,
        'use_setinputsizes': False,
    }
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'backend/static/uploads')


class NqtCauHinhDevelopment(NqtCauHinhFlask):
    DEBUG = True


class NqtCauHinhProduction(NqtCauHinhFlask):
    DEBUG = False


nqt_cau_hinh_map = {
    'development': NqtCauHinhDevelopment,
    'production': NqtCauHinhProduction,
    'default': NqtCauHinhDevelopment,
}
