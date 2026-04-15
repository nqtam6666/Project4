from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_nhan_vien import G6NhanVien, G6LichLamViec
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_nhan_vien_bp = Blueprint('g6_nhan_vien', __name__, url_prefix='/api')


@nqt_nhan_vien_bp.route('/nqt-nhan-vien', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_tat_ca_nhan_vien():
    nqt_chi_nhanh = request.args.get('g6_ma_chi_nhanh', type=int)
    nqt_trang_thai = request.args.get('g6_trang_thai')
    nqt_q = G6NhanVien.query
    if nqt_chi_nhanh:
        nqt_q = nqt_q.filter_by(g6_ma_chi_nhanh=nqt_chi_nhanh)
    if nqt_trang_thai:
        nqt_q = nqt_q.filter_by(g6_trang_thai=nqt_trang_thai)
    else:
        nqt_q = nqt_q.filter_by(g6_trang_thai='dang_lam')
    return nqt_ok([n.g6_to_dict() for n in nqt_q.all()])


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_nhan_vien(nqt_id):
    nqt_row = G6NhanVien.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_nhan_vien_bp.route('/nqt-nhan-vien', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_ly_nhan_vien')
def nqt_tao_nhan_vien():
    nqt_data = request.get_json() or {}
    nqt_ho_ten = nqt_data.get('g6_ho_ten', '').strip()
    nqt_chi_nhanh = nqt_data.get('g6_ma_chi_nhanh')
    nqt_ngay_vao = nqt_data.get('g6_ngay_vao_lam')
    if not nqt_ho_ten or not nqt_chi_nhanh or not nqt_ngay_vao:
        return nqt_loi('Thiếu họ tên, chi nhánh hoặc ngày vào làm')
    nqt_row = G6NhanVien(
        g6_ho_ten=nqt_ho_ten,
        g6_ma_chi_nhanh=nqt_chi_nhanh,
        g6_ngay_vao_lam=nqt_ngay_vao,
        g6_ma_nguoi_dung=nqt_data.get('g6_ma_nguoi_dung'),
        g6_ngay_sinh=nqt_data.get('g6_ngay_sinh'),
        g6_gioi_tinh=nqt_data.get('g6_gioi_tinh'),
        g6_so_dien_thoai=nqt_data.get('g6_so_dien_thoai'),
        g6_email=nqt_data.get('g6_email'),
        g6_luong_co_ban=nqt_data.get('g6_luong_co_ban', 0),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo nhân viên thành công', 201)


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_ly_nhan_vien')
def nqt_cap_nhat_nhan_vien(nqt_id):
    nqt_row = G6NhanVien.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_ho_ten', 'g6_so_dien_thoai', 'g6_email', 'g6_trang_thai', 'g6_luong_co_ban']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>/nqt-lich-lam', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_lich_lam(nqt_id):
    G6NhanVien.query.get_or_404(nqt_id)
    nqt_list = G6LichLamViec.query.filter_by(g6_ma_nhan_vien=nqt_id).all()
    return nqt_ok([l.g6_to_dict() for l in nqt_list])


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>/nqt-lich-lam', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_them_lich_lam(nqt_id):
    G6NhanVien.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_row = G6LichLamViec(
        g6_ma_nhan_vien=nqt_id,
        g6_ma_chi_nhanh=nqt_data.get('g6_ma_chi_nhanh'),
        g6_thu_trong_tuan=nqt_data.get('g6_thu_trong_tuan'),
        g6_gio_bat_dau=nqt_data.get('g6_gio_bat_dau'),
        g6_gio_ket_thuc=nqt_data.get('g6_gio_ket_thuc'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Thêm lịch thành công', 201)


@nqt_nhan_vien_bp.route('/nqt-nhan-vien/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_ly_nhan_vien')
def nqt_xoa_nhan_vien(nqt_id):
    from datetime import date
    nqt_row = G6NhanVien.query.get_or_404(nqt_id)
    nqt_row.g6_trang_thai = 'nghi_viec'
    nqt_row.g6_ngay_nghi_viec = date.today()
    db.session.commit()
    return nqt_ok(None, 'Đã cho nhân viên nghỉ việc')
