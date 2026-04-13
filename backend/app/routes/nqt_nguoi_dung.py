import bcrypt
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from backend.app import db
from backend.app.models.nqt_nguoi_dung import NqtNguoiDung, NqtVaiTro, NqtNguoiDungVaiTro
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_nguoi_dung_bp = Blueprint('nqt_nguoi_dung', __name__, url_prefix='/api')


@nqt_nguoi_dung_bp.route('/nqt-nguoi-dung', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_quan_ly_nhan_vien')
def nqt_lay_tat_ca_nguoi_dung():
    nqt_trang = request.args.get('nqt_trang', 1, type=int)
    nqt_gioi_han = request.args.get('nqt_gioi_han', 20, type=int)
    nqt_q = NqtNguoiDung.query.order_by(NqtNguoiDung.nqt_ngay_tao.desc())
    nqt_phan_trang = nqt_q.paginate(page=nqt_trang, per_page=nqt_gioi_han, error_out=False)
    return nqt_ok({
        'nqt_danh_sach': [u.nqt_to_dict() for u in nqt_phan_trang.items],
        'nqt_tong': nqt_phan_trang.total,
        'nqt_trang': nqt_trang,
        'nqt_tong_trang': nqt_phan_trang.pages,
    })


@nqt_nguoi_dung_bp.route('/nqt-nguoi-dung/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_nguoi_dung(nqt_id):
    nqt_row = NqtNguoiDung.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_nguoi_dung_bp.route('/nqt-nguoi-dung', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_quan_ly_nhan_vien')
def nqt_tao_nguoi_dung():
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('nqt_ten_dang_nhap', '').strip()
    nqt_mk = nqt_data.get('nqt_mat_khau', '')
    nqt_ho_ten = nqt_data.get('nqt_ho_ten', '').strip()

    if not nqt_ten or not nqt_mk or not nqt_ho_ten:
        return nqt_loi('Thiếu thông tin bắt buộc')

    if NqtNguoiDung.query.filter_by(nqt_ten_dang_nhap=nqt_ten).first():
        return nqt_loi('Tên đăng nhập đã tồn tại')

    nqt_mk_hash = bcrypt.hashpw(nqt_mk.encode(), bcrypt.gensalt()).decode()
    nqt_row = NqtNguoiDung(
        nqt_ten_dang_nhap=nqt_ten,
        nqt_mat_khau=nqt_mk_hash,
        nqt_ho_ten=nqt_ho_ten,
        nqt_email=nqt_data.get('nqt_email'),
        nqt_so_dien_thoai=nqt_data.get('nqt_so_dien_thoai'),
        nqt_ma_chi_nhanh=nqt_data.get('nqt_ma_chi_nhanh'),
    )
    db.session.add(nqt_row)
    db.session.flush()

    nqt_vai_tro_ids = nqt_data.get('nqt_vai_tro_ids', [])
    for nqt_vt_id in nqt_vai_tro_ids:
        if NqtVaiTro.query.get(nqt_vt_id):
            db.session.add(NqtNguoiDungVaiTro(
                nqt_ma_nguoi_dung=nqt_row.nqt_ma_nguoi_dung,
                nqt_ma_vai_tro=nqt_vt_id,
            ))
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo tài khoản thành công', 201)


@nqt_nguoi_dung_bp.route('/nqt-nguoi-dung/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_nguoi_dung(nqt_id):
    nqt_row = NqtNguoiDung.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['nqt_ho_ten', 'nqt_email', 'nqt_so_dien_thoai', 'nqt_la_hoat_dong']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    if 'nqt_mat_khau_moi' in nqt_data:
        nqt_row.nqt_mat_khau = bcrypt.hashpw(
            nqt_data['nqt_mat_khau_moi'].encode(), bcrypt.gensalt()
        ).decode()
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_nguoi_dung_bp.route('/nqt-vai-tro', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_vai_tro():
    nqt_list = NqtVaiTro.query.all()
    return nqt_ok([v.nqt_to_dict() for v in nqt_list])
