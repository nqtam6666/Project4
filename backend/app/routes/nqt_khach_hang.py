import bcrypt
from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_nguoi_dung import G6NguoiDung
from backend.app.models.g6_khach_hang import (
    G6DiaChiGiaoHang, G6HangThanhVien,
    G6DiemKhachHang, G6GiaoDichDiem,
)
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_khach_hang_bp = Blueprint('g6_khach_hang', __name__, url_prefix='/api')


@nqt_khach_hang_bp.route('/nqt-khach-hang', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_HOI_VIEN')
def nqt_lay_tat_ca_khach_hang():
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nqt_tim = request.args.get('g6_tim_kiem', '').strip()
    nqt_q = G6NguoiDung.query.filter_by(g6_la_khach_hang=True)
    if nqt_tim:
        nqt_q = nqt_q.filter(
            G6NguoiDung.g6_ho_ten.ilike(f'%{nqt_tim}%') |
            G6NguoiDung.g6_email.ilike(f'%{nqt_tim}%')
        )
    nqt_phan_trang = nqt_q.order_by(G6NguoiDung.g6_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [k.g6_to_dict() for k in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
    })


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_khach_hang(nqt_id):
    nqt_row = G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_id, g6_la_khach_hang=True).first_or_404()
    nqt_result = nqt_row.g6_to_dict()
    if nqt_row.g6_diem:
        nqt_result['g6_diem'] = nqt_row.g6_diem.g6_to_dict()
    return nqt_ok(nqt_result)


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_HOI_VIEN')
def nqt_cap_nhat_khach_hang(nqt_id):
    nqt_row = G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_id, g6_la_khach_hang=True).first_or_404()
    nqt_data = request.get_json() or {}

    if 'g6_ho_ten' in nqt_data:
        nqt_row.g6_ho_ten = nqt_data['g6_ho_ten']
    if 'g6_email' in nqt_data:
        nqt_row.g6_email = nqt_data['g6_email']
    if 'g6_so_dien_thoai' in nqt_data:
        nqt_row.g6_so_dien_thoai = nqt_data['g6_so_dien_thoai']
    if 'g6_la_hoat_dong' in nqt_data:
        nqt_row.g6_la_hoat_dong = nqt_data['g6_la_hoat_dong']
    if 'g6_ngay_sinh' in nqt_data:
        nqt_row.g6_ngay_sinh = nqt_data['g6_ngay_sinh']

    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Cập nhật khách hàng thành công')


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_HOI_VIEN')
def nqt_xoa_khach_hang(nqt_id):
    nqt_row = G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_id, g6_la_khach_hang=True).first_or_404()
    # Xóa điểm liên quan
    if nqt_row.g6_diem:
        db.session.delete(nqt_row.g6_diem)
    # Xóa địa chỉ giao hàng
    G6DiaChiGiaoHang.query.filter_by(g6_ma_nguoi_dung=nqt_id).delete()
    # Xóa giao dịch điểm
    G6GiaoDichDiem.query.filter_by(g6_ma_nguoi_dung=nqt_id).delete()
    db.session.delete(nqt_row)
    db.session.commit()
    return nqt_ok(None, 'Xóa khách hàng thành công')


@nqt_khach_hang_bp.route('/nqt-khach-hang/nqt-dang-ky', methods=['POST'])
def nqt_dang_ky_khach_hang():
    nqt_data = request.get_json() or {}
    nqt_email = nqt_data.get('g6_email', '').strip()
    nqt_mk = nqt_data.get('g6_mat_khau', '')
    nqt_ho_ten = nqt_data.get('g6_ho_ten', '').strip()
    if not nqt_email or not nqt_mk or not nqt_ho_ten:
        return nqt_loi('Thiếu thông tin bắt buộc')
    if G6NguoiDung.query.filter_by(g6_email=nqt_email).first():
        return nqt_loi('Email đã được đăng ký')
    
    nqt_row = G6NguoiDung(
        g6_ho_ten=nqt_ho_ten,
        g6_email=nqt_email,
        g6_la_khach_hang=True,
        g6_so_dien_thoai=nqt_data.get('g6_so_dien_thoai'),
    )
    nqt_row.nqt_dat_mat_khau(nqt_mk)
    db.session.add(nqt_row)
    db.session.flush()
    nqt_hang_dau = G6HangThanhVien.query.order_by(G6HangThanhVien.g6_diem_toi_thieu).first()
    nqt_diem = G6DiemKhachHang(
        g6_ma_nguoi_dung=nqt_row.g6_ma_nguoi_dung,
        g6_ma_hang=nqt_hang_dau.g6_ma_hang if nqt_hang_dau else None,
    )
    db.session.add(nqt_diem)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Đăng ký thành công', 201)


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>/nqt-dia-chi', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_dia_chi(nqt_id):
    G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_id, g6_la_khach_hang=True).first_or_404()
    nqt_list = G6DiaChiGiaoHang.query.filter_by(g6_ma_nguoi_dung=nqt_id).all()
    return nqt_ok([d.g6_to_dict() for d in nqt_list])


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>/nqt-dia-chi', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_them_dia_chi(nqt_id):
    G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_id, g6_la_khach_hang=True).first_or_404()
    nqt_data = request.get_json() or {}
    nqt_row = G6DiaChiGiaoHang(
        g6_ma_nguoi_dung=nqt_id,
        g6_ho_ten_nguoi_nhan=nqt_data.get('g6_ho_ten_nguoi_nhan', ''),
        g6_so_dien_thoai=nqt_data.get('g6_so_dien_thoai', ''),
        g6_dia_chi_chi_tiet=nqt_data.get('g6_dia_chi_chi_tiet', ''),
        g6_phuong_xa=nqt_data.get('g6_phuong_xa'),
        g6_quan_huyen=nqt_data.get('g6_quan_huyen'),
        g6_tinh_thanh=nqt_data.get('g6_tinh_thanh'),
        g6_la_mac_dinh=nqt_data.get('g6_la_mac_dinh', False),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Thêm địa chỉ thành công', 201)


@nqt_khach_hang_bp.route('/nqt-khach-hang/<int:nqt_id>/nqt-diem', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_diem(nqt_id):
    G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_id, g6_la_khach_hang=True).first_or_404()
    nqt_diem = G6DiemKhachHang.query.get(nqt_id)
    nqt_lich_su = G6GiaoDichDiem.query.filter_by(g6_ma_nguoi_dung=nqt_id).order_by(
        G6GiaoDichDiem.g6_ngay_tao.desc()
    ).limit(20).all()
    return nqt_ok({
        'g6_diem': nqt_diem.g6_to_dict() if nqt_diem else None,
        'g6_lich_su': [g.g6_to_dict() for g in nqt_lich_su],
    })


@nqt_khach_hang_bp.route('/nqt-hang-thanh-vien', methods=['GET'])
def nqt_lay_hang_thanh_vien():
    nqt_list = G6HangThanhVien.query.order_by(G6HangThanhVien.g6_diem_toi_thieu).all()
    return nqt_ok([h.g6_to_dict() for h in nqt_list])
