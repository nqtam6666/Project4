import bcrypt
from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_khach_hang import (
    NqtKhachHang, NqtDiaChiGiaoHang, NqtHangThanhVien,
    NqtDiemKhachHang, NqtGiaoDichDiem,
)
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_khach_hang_bp = Blueprint('nqt_khach_hang', __name__, url_prefix='/api')


@nqt_khach_hang_bp.route('/nqt-khach-hang', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_tat_ca_khach_hang():
    nqt_trang = request.args.get('nqt_trang', 1, type=int)
    nqt_gioi_han = request.args.get('nqt_gioi_han', 20, type=int)
    nqt_tim = request.args.get('nqt_tim_kiem', '').strip()
    nqt_q = NqtKhachHang.query
    if nqt_tim:
        nqt_q = nqt_q.filter(
            NqtKhachHang.nqt_ho_ten.ilike(f'%{nqt_tim}%') |
            NqtKhachHang.nqt_email.ilike(f'%{nqt_tim}%')
        )
    nqt_phan_trang = nqt_q.order_by(NqtKhachHang.nqt_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'nqt_danh_sach': [k.nqt_to_dict() for k in nqt_phan_trang.items],
        'nqt_tong': nqt_phan_trang.total,
        'nqt_trang': nqt_trang,
    })


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_khach_hang(nqt_id):
    nqt_row = NqtKhachHang.query.get_or_404(nqt_id)
    nqt_result = nqt_row.nqt_to_dict()
    if nqt_row.nqt_diem:
        nqt_result['nqt_diem'] = nqt_row.nqt_diem.nqt_to_dict()
    return nqt_ok(nqt_result)


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_khach_hang(nqt_id):
    nqt_row = NqtKhachHang.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}

    if 'nqt_ho_ten' in nqt_data:
        nqt_row.nqt_ho_ten = nqt_data['nqt_ho_ten']
    if 'nqt_email' in nqt_data:
        nqt_row.nqt_email = nqt_data['nqt_email']
    if 'nqt_so_dien_thoai' in nqt_data:
        nqt_row.nqt_so_dien_thoai = nqt_data['nqt_so_dien_thoai']
    if 'nqt_la_hoat_dong' in nqt_data:
        nqt_row.nqt_la_hoat_dong = nqt_data['nqt_la_hoat_dong']
    if 'nqt_ngay_sinh' in nqt_data:
        nqt_row.nqt_ngay_sinh = nqt_data['nqt_ngay_sinh']

    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Cập nhật khách hàng thành công')


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_khach_hang(nqt_id):
    nqt_row = NqtKhachHang.query.get_or_404(nqt_id)
    # Xóa điểm liên quan
    if nqt_row.nqt_diem:
        db.session.delete(nqt_row.nqt_diem)
    # Xóa địa chỉ giao hàng
    NqtDiaChiGiaoHang.query.filter_by(nqt_ma_khach_hang=nqt_id).delete()
    # Xóa giao dịch điểm
    NqtGiaoDichDiem.query.filter_by(nqt_ma_khach_hang=nqt_id).delete()
    db.session.delete(nqt_row)
    db.session.commit()
    return nqt_ok(None, 'Xóa khách hàng thành công')


@nqt_khach_hang_bp.route('/nqt-khach-hang/nqt-dang-ky', methods=['POST'])
def nqt_dang_ky_khach_hang():
    nqt_data = request.get_json() or {}
    nqt_email = nqt_data.get('nqt_email', '').strip()
    nqt_mk = nqt_data.get('nqt_mat_khau', '')
    nqt_ho_ten = nqt_data.get('nqt_ho_ten', '').strip()
    if not nqt_email or not nqt_mk or not nqt_ho_ten:
        return nqt_loi('Thiếu thông tin bắt buộc')
    if NqtKhachHang.query.filter_by(nqt_email=nqt_email).first():
        return nqt_loi('Email đã được đăng ký')
    nqt_mk_hash = bcrypt.hashpw(nqt_mk.encode(), bcrypt.gensalt()).decode()
    nqt_row = NqtKhachHang(
        nqt_ho_ten=nqt_ho_ten,
        nqt_email=nqt_email,
        nqt_mat_khau=nqt_mk_hash,
        nqt_so_dien_thoai=nqt_data.get('nqt_so_dien_thoai'),
    )
    db.session.add(nqt_row)
    db.session.flush()
    nqt_hang_dau = NqtHangThanhVien.query.order_by(NqtHangThanhVien.nqt_diem_toi_thieu).first()
    nqt_diem = NqtDiemKhachHang(
        nqt_ma_khach_hang=nqt_row.nqt_ma_khach_hang,
        nqt_ma_hang=nqt_hang_dau.nqt_ma_hang if nqt_hang_dau else None,
    )
    db.session.add(nqt_diem)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Đăng ký thành công', 201)


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>/nqt-dia-chi', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_dia_chi(nqt_id):
    NqtKhachHang.query.get_or_404(nqt_id)
    nqt_list = NqtDiaChiGiaoHang.query.filter_by(nqt_ma_khach_hang=nqt_id).all()
    return nqt_ok([d.nqt_to_dict() for d in nqt_list])


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>/nqt-dia-chi', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_them_dia_chi(nqt_id):
    NqtKhachHang.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_row = NqtDiaChiGiaoHang(
        nqt_ma_khach_hang=nqt_id,
        nqt_ho_ten_nguoi_nhan=nqt_data.get('nqt_ho_ten_nguoi_nhan', ''),
        nqt_so_dien_thoai=nqt_data.get('nqt_so_dien_thoai', ''),
        nqt_dia_chi_chi_tiet=nqt_data.get('nqt_dia_chi_chi_tiet', ''),
        nqt_phuong_xa=nqt_data.get('nqt_phuong_xa'),
        nqt_quan_huyen=nqt_data.get('nqt_quan_huyen'),
        nqt_tinh_thanh=nqt_data.get('nqt_tinh_thanh'),
        nqt_la_mac_dinh=nqt_data.get('nqt_la_mac_dinh', False),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Thêm địa chỉ thành công', 201)


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>/nqt-diem', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_diem(nqt_id):
    NqtKhachHang.query.get_or_404(nqt_id)
    nqt_diem = NqtDiemKhachHang.query.get(nqt_id)
    nqt_lich_su = NqtGiaoDichDiem.query.filter_by(nqt_ma_khach_hang=nqt_id).order_by(
        NqtGiaoDichDiem.nqt_ngay_tao.desc()
    ).limit(20).all()
    return nqt_ok({
        'nqt_diem': nqt_diem.nqt_to_dict() if nqt_diem else None,
        'nqt_lich_su': [g.nqt_to_dict() for g in nqt_lich_su],
    })


@nqt_khach_hang_bp.route('/nqt-hang-thanh-vien', methods=['GET'])
def nqt_lay_hang_thanh_vien():
    nqt_list = NqtHangThanhVien.query.order_by(NqtHangThanhVien.nqt_diem_toi_thieu).all()
    return nqt_ok([h.nqt_to_dict() for h in nqt_list])
