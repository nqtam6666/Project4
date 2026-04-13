from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_nhan_vien import NqtNhanVien, NqtLichLamViec
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_nhan_vien_bp = Blueprint('nqt_nhan_vien', __name__, url_prefix='/api')


@nqt_nhan_vien_bp.route('/nqt-nhan-vien', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_tat_ca_nhan_vien():
    nqt_chi_nhanh = request.args.get('nqt_ma_chi_nhanh', type=int)
    nqt_trang_thai = request.args.get('nqt_trang_thai')
    nqt_q = NqtNhanVien.query
    if nqt_chi_nhanh:
        nqt_q = nqt_q.filter_by(nqt_ma_chi_nhanh=nqt_chi_nhanh)
    if nqt_trang_thai:
        nqt_q = nqt_q.filter_by(nqt_trang_thai=nqt_trang_thai)
    else:
        nqt_q = nqt_q.filter_by(nqt_trang_thai='dang_lam')
    return nqt_ok([n.nqt_to_dict() for n in nqt_q.all()])


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_nhan_vien(nqt_id):
    nqt_row = NqtNhanVien.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_nhan_vien_bp.route('/nqt-nhan-vien', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_quan_ly_nhan_vien')
def nqt_tao_nhan_vien():
    nqt_data = request.get_json() or {}
    nqt_ho_ten = nqt_data.get('nqt_ho_ten', '').strip()
    nqt_chi_nhanh = nqt_data.get('nqt_ma_chi_nhanh')
    nqt_ngay_vao = nqt_data.get('nqt_ngay_vao_lam')
    if not nqt_ho_ten or not nqt_chi_nhanh or not nqt_ngay_vao:
        return nqt_loi('Thiếu họ tên, chi nhánh hoặc ngày vào làm')
    nqt_row = NqtNhanVien(
        nqt_ho_ten=nqt_ho_ten,
        nqt_ma_chi_nhanh=nqt_chi_nhanh,
        nqt_ngay_vao_lam=nqt_ngay_vao,
        nqt_ma_nguoi_dung=nqt_data.get('nqt_ma_nguoi_dung'),
        nqt_ngay_sinh=nqt_data.get('nqt_ngay_sinh'),
        nqt_gioi_tinh=nqt_data.get('nqt_gioi_tinh'),
        nqt_so_dien_thoai=nqt_data.get('nqt_so_dien_thoai'),
        nqt_email=nqt_data.get('nqt_email'),
        nqt_luong_co_ban=nqt_data.get('nqt_luong_co_ban', 0),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo nhân viên thành công', 201)


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_quan_ly_nhan_vien')
def nqt_cap_nhat_nhan_vien(nqt_id):
    nqt_row = NqtNhanVien.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['nqt_ho_ten', 'nqt_so_dien_thoai', 'nqt_email', 'nqt_trang_thai', 'nqt_luong_co_ban']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>/nqt-lich-lam', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_lich_lam(nqt_id):
    NqtNhanVien.query.get_or_404(nqt_id)
    nqt_list = NqtLichLamViec.query.filter_by(nqt_ma_nhan_vien=nqt_id).all()
    return nqt_ok([l.nqt_to_dict() for l in nqt_list])


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>/nqt-lich-lam', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_them_lich_lam(nqt_id):
    NqtNhanVien.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_row = NqtLichLamViec(
        nqt_ma_nhan_vien=nqt_id,
        nqt_ma_chi_nhanh=nqt_data.get('nqt_ma_chi_nhanh'),
        nqt_thu_trong_tuan=nqt_data.get('nqt_thu_trong_tuan'),
        nqt_gio_bat_dau=nqt_data.get('nqt_gio_bat_dau'),
        nqt_gio_ket_thuc=nqt_data.get('nqt_gio_ket_thuc'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Thêm lịch thành công', 201)
