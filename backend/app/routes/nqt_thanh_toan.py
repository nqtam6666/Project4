from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_thanh_toan import G6ThanhToan, G6HoaDon
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap
from datetime import datetime
import random
import string

nqt_thanh_toan_bp = Blueprint('g6_thanh_toan', __name__, url_prefix='/api')


@nqt_thanh_toan_bp.route('/nqt-thanh-toan', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_tat_ca_thanh_toan():
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nqt_trang_thai = request.args.get('g6_trang_thai')
    nqt_phuong_thuc = request.args.get('g6_phuong_thuc')
    nqt_kh_id = request.args.get('g6_ma_khach_hang', type=int)

    nqt_q = G6ThanhToan.query
    if nqt_trang_thai:
        nqt_q = nqt_q.filter_by(g6_trang_thai=nqt_trang_thai)
    if nqt_phuong_thuc:
        nqt_q = nqt_q.filter_by(g6_phuong_thuc=nqt_phuong_thuc)
    if nqt_kh_id:
        nqt_q = nqt_q.filter_by(g6_ma_khach_hang=nqt_kh_id)

    nqt_phan_trang = nqt_q.order_by(G6ThanhToan.g6_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [t.g6_to_dict() for t in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
    })


def _nqt_tao_so_hoa_don():
    nqt_prefix = datetime.utcnow().strftime('HD%Y%m%d')
    nqt_suffix = ''.join(random.choices(string.digits, k=5))
    return f'{nqt_prefix}{nqt_suffix}'


@nqt_thanh_toan_bp.route('/nqt-thanh-toan', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_thanh_toan():
    nqt_data = request.get_json() or {}
    nqt_so_tien = nqt_data.get('g6_so_tien', 0)
    nqt_loai = nqt_data.get('g6_loai_giao_dich', 'don_hang')
    nqt_phuong_thuc = nqt_data.get('g6_phuong_thuc', 'cod')

    if float(nqt_so_tien) <= 0:
        return nqt_loi('Số tiền không hợp lệ')

    nqt_row = G6ThanhToan(
        g6_ma_khach_hang=nqt_data.get('g6_ma_khach_hang'),
        g6_loai_giao_dich=nqt_loai,
        g6_so_tien=nqt_so_tien,
        g6_phuong_thuc=nqt_phuong_thuc,
        g6_trang_thai='cho_xu_ly',
        g6_ghi_chu=nqt_data.get('g6_ghi_chu'),
    )
    db.session.add(nqt_row)
    db.session.flush()

    # COD xác nhận ngay
    if nqt_phuong_thuc == 'cod':
        nqt_row.g6_trang_thai = 'thanh_cong'
        nqt_row.g6_ngay_thanh_toan = datetime.utcnow()
        nqt_xuat_hoa_don(nqt_row)

    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo thanh toán thành công', 201)


def nqt_xuat_hoa_don(nqt_tt: G6ThanhToan):
    from backend.app.services.g6_dich_vu_cau_hinh import NqtDichVuCauHinh
    nqt_vat = NqtDichVuCauHinh.g6_lay('g6_thue_vat_phan_tram', nqt_mac_dinh=0)
    nqt_tien_thue = float(nqt_tt.g6_so_tien) * nqt_vat / 100
    nqt_hd = G6HoaDon(
        g6_ma_thanh_toan=nqt_tt.g6_ma_thanh_toan,
        g6_so_hoa_don=_nqt_tao_so_hoa_don(),
        g6_tien_truoc_thue=nqt_tt.g6_so_tien,
        g6_tien_thue=nqt_tien_thue,
        g6_tong_cong=float(nqt_tt.g6_so_tien) + nqt_tien_thue,
    )
    db.session.add(nqt_hd)


@nqt_thanh_toan_bp.route('/nqt-thanh-toan/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_thanh_toan(nqt_id):
    nqt_row = G6ThanhToan.query.get_or_404(nqt_id)
    nqt_result = nqt_row.g6_to_dict()
    if nqt_row.g6_hoa_don:
        nqt_result['g6_hoa_don'] = nqt_row.g6_hoa_don.g6_to_dict()
    return nqt_ok(nqt_result)


@nqt_thanh_toan_bp.route('/nqt-thanh-toan/<int:nqt_id>/nqt-xac-nhan', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_xac_nhan_thanh_toan(nqt_id):
    nqt_row = G6ThanhToan.query.get_or_404(nqt_id)
    if nqt_row.g6_trang_thai == 'thanh_cong':
        return nqt_loi('Thanh toán đã được xác nhận trước đó')
    nqt_row.g6_trang_thai = 'thanh_cong'
    nqt_row.g6_ngay_thanh_toan = datetime.utcnow()
    if not nqt_row.g6_hoa_don:
        nqt_xuat_hoa_don(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Xác nhận thanh toán thành công')
