import bcrypt
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from backend.app import db
from backend.app.models.g6_nguoi_dung import G6NguoiDung, G6VaiTro, G6NguoiDungVaiTro
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_nguoi_dung_bp = Blueprint('g6_nguoi_dung', __name__, url_prefix='/api')


@nqt_nguoi_dung_bp.route('/nqt-nguoi-dung', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_ly_nhan_vien')
def nqt_lay_tat_ca_nguoi_dung():
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nqt_q = G6NguoiDung.query.order_by(G6NguoiDung.g6_ngay_tao.desc())
    nqt_phan_trang = nqt_q.paginate(page=nqt_trang, per_page=nqt_gioi_han, error_out=False)
    return nqt_ok({
        'g6_danh_sach': [u.g6_to_dict() for u in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
        'g6_tong_trang': nqt_phan_trang.pages,
    })


@nqt_nguoi_dung_bp.route('/nqt-nguoi-dung/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_nguoi_dung(nqt_id):
    nqt_row = G6NguoiDung.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_nguoi_dung_bp.route('/nqt-nguoi-dung', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_ly_nhan_vien')
def nqt_tao_nguoi_dung():
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('g6_ten_dang_nhap', '').strip()
    nqt_mk = nqt_data.get('g6_mat_khau', '')
    nqt_ho_ten = nqt_data.get('g6_ho_ten', '').strip()

    if not nqt_ten or not nqt_mk or not nqt_ho_ten:
        return nqt_loi('Thiếu thông tin bắt buộc')

    if G6NguoiDung.query.filter_by(g6_ten_dang_nhap=nqt_ten).first():
        return nqt_loi('Tên đăng nhập đã tồn tại')

    nqt_mk_hash = bcrypt.hashpw(nqt_mk.encode(), bcrypt.gensalt()).decode()
    nqt_row = G6NguoiDung(
        g6_ten_dang_nhap=nqt_ten,
        g6_mat_khau=nqt_mk_hash,
        g6_ho_ten=nqt_ho_ten,
        g6_email=nqt_data.get('g6_email'),
        g6_so_dien_thoai=nqt_data.get('g6_so_dien_thoai'),
        g6_ma_chi_nhanh=nqt_data.get('g6_ma_chi_nhanh'),
    )
    db.session.add(nqt_row)
    db.session.flush()

    nqt_vai_tro_ids = nqt_data.get('g6_vai_tro_ids', [])
    for nqt_vt_id in nqt_vai_tro_ids:
        if G6VaiTro.query.get(nqt_vt_id):
            db.session.add(G6NguoiDungVaiTro(
                g6_ma_nguoi_dung=nqt_row.g6_ma_nguoi_dung,
                g6_ma_vai_tro=nqt_vt_id,
            ))
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo tài khoản thành công', 201)


@nqt_nguoi_dung_bp.route('/nqt-nguoi-dung/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_nguoi_dung(nqt_id):
    nqt_row = G6NguoiDung.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_ho_ten', 'g6_email', 'g6_so_dien_thoai', 'g6_la_hoat_dong']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    if 'g6_mat_khau_moi' in nqt_data:
        nqt_row.g6_mat_khau = bcrypt.hashpw(
            nqt_data['g6_mat_khau_moi'].encode(), bcrypt.gensalt()
        ).decode()
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_nguoi_dung_bp.route('/nqt-vai-tro', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_vai_tro():
    nqt_list = G6VaiTro.query.all()
    return nqt_ok([v.g6_to_dict() for v in nqt_list])
