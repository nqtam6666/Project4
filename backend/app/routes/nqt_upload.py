import os
import uuid
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_upload_bp = Blueprint('g6_upload', __name__, url_prefix='/api')

NQT_DUOI_FILE_CHO_PHEP = {'png', 'jpg', 'jpeg', 'gif', 'ico', 'svg', 'webp'}


def _nqt_kiem_tra_duoi_file(nqt_ten_file: str) -> bool:
    if '.' not in nqt_ten_file:
        return False
    nqt_duoi = nqt_ten_file.rsplit('.', 1)[1].lower()
    return nqt_duoi in NQT_DUOI_FILE_CHO_PHEP


def _nqt_tao_ten_file_an_toan(nqt_ten_goc: str) -> str:
    """Tạo tên file unique để tránh trùng."""
    nqt_ten_an_toan = secure_filename(nqt_ten_goc)
    nqt_duoi = nqt_ten_an_toan.rsplit('.', 1)[1].lower() if '.' in nqt_ten_an_toan else 'png'
    nqt_ten_moi = f"{uuid.uuid4().hex}.{nqt_duoi}"
    return nqt_ten_moi


@nqt_upload_bp.route('/nqt-upload', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_sua_cau_hinh')
def nqt_upload_file():
    """Upload file ảnh (favicon, logo, avatar mặc định, ...)."""
    if 'file' not in request.files:
        return nqt_loi('Không tìm thấy file trong request')

    nqt_file = request.files['file']
    if nqt_file.filename == '':
        return nqt_loi('Chưa chọn file')

    if not _nqt_kiem_tra_duoi_file(nqt_file.filename):
        return nqt_loi(f'Định dạng không hợp lệ. Chỉ chấp nhận: {", ".join(NQT_DUOI_FILE_CHO_PHEP)}')

    # Tạo thư mục uploads nếu chưa có
    nqt_thu_muc_upload = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(nqt_thu_muc_upload, exist_ok=True)

    # Tạo tên file unique
    nqt_ten_file = _nqt_tao_ten_file_an_toan(nqt_file.filename)
    nqt_duong_dan = os.path.join(nqt_thu_muc_upload, nqt_ten_file)

    # Lưu file
    nqt_file.save(nqt_duong_dan)

    # Trả về URL tương đối
    nqt_url = f'/static/uploads/{nqt_ten_file}'

    return nqt_ok({
        'g6_url': nqt_url,
        'g6_ten_file': nqt_ten_file
    }, 'Upload thành công')
