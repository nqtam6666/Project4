import os
from dotenv import load_dotenv

load_dotenv()


class NqtCauHinhFlask:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{pw}@{host}/{db}?charset=utf8mb4'.format(
            user=os.getenv('DB_USER', 'root'),
            pw=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_SERVER', 'localhost'),
            db=os.getenv('DB_NAME', 'nqt_gym'),
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
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
