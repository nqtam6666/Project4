from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_thanh_toan import NqtThanhToan, NqtHoaDon
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap
from datetime import datetime
import random
import string

nqt_thanh_toan_bp = Blueprint('nqt_thanh_toan', __name__, url_prefix='/api')


@nqt_thanh_toan_bp.route('/nqt-thanh-toan', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_tat_ca_thanh_toan():
    nqt_trang = request.args.get('nqt_trang', 1, type=int)
    nqt_gioi_han = request.args.get('nqt_gioi_han', 20, type=int)
    nqt_trang_thai = request.args.get('nqt_trang_thai')
    nqt_phuong_thuc = request.args.get('nqt_phuong_thuc')
    nqt_kh_id = request.args.get('nqt_ma_khach_hang', type=int)

    nqt_q = NqtThanhToan.query
    if nqt_trang_thai:
        nqt_q = nqt_q.filter_by(nqt_trang_thai=nqt_trang_thai)
    if nqt_phuong_thuc:
        nqt_q = nqt_q.filter_by(nqt_phuong_thuc=nqt_phuong_thuc)
    if nqt_kh_id:
        nqt_q = nqt_q.filter_by(nqt_ma_khach_hang=nqt_kh_id)

    nqt_phan_trang = nqt_q.order_by(NqtThanhToan.nqt_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'nqt_danh_sach': [t.nqt_to_dict() for t in nqt_phan_trang.items],
        'nqt_tong': nqt_phan_trang.total,
        'nqt_trang': nqt_trang,
    })


def _nqt_tao_so_hoa_don():
    nqt_prefix = datetime.utcnow().strftime('HD%Y%m%d')
    nqt_suffix = ''.join(random.choices(string.digits, k=5))
    return f'{nqt_prefix}{nqt_suffix}'


@nqt_thanh_toan_bp.route('/nqt-thanh-toan', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_thanh_toan():
    nqt_data = request.get_json() or {}
    nqt_so_tien = nqt_data.get('nqt_so_tien', 0)
    nqt_loai = nqt_data.get('nqt_loai_giao_dich', 'don_hang')
    nqt_phuong_thuc = nqt_data.get('nqt_phuong_thuc', 'cod')

    if float(nqt_so_tien) <= 0:
        return nqt_loi('Số tiền không hợp lệ')

    nqt_row = NqtThanhToan(
        nqt_ma_khach_hang=nqt_data.get('nqt_ma_khach_hang'),
        nqt_loai_giao_dich=nqt_loai,
        nqt_so_tien=nqt_so_tien,
        nqt_phuong_thuc=nqt_phuong_thuc,
        nqt_trang_thai='cho_xu_ly',
        nqt_ghi_chu=nqt_data.get('nqt_ghi_chu'),
    )
    db.session.add(nqt_row)
    db.session.flush()

    # COD xác nhận ngay
    if nqt_phuong_thuc == 'cod':
        nqt_row.nqt_trang_thai = 'thanh_cong'
        nqt_row.nqt_ngay_thanh_toan = datetime.utcnow()
        nqt_xuat_hoa_don(nqt_row)

    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo thanh toán thành công', 201)


def nqt_xuat_hoa_don(nqt_tt: NqtThanhToan):
    from backend.app.services.nqt_dich_vu_cau_hinh import NqtDichVuCauHinh
    nqt_vat = NqtDichVuCauHinh.nqt_lay('nqt_thue_vat_phan_tram', nqt_mac_dinh=0)
    nqt_tien_thue = float(nqt_tt.nqt_so_tien) * nqt_vat / 100
    nqt_hd = NqtHoaDon(
        nqt_ma_thanh_toan=nqt_tt.nqt_ma_thanh_toan,
        nqt_so_hoa_don=_nqt_tao_so_hoa_don(),
        nqt_tien_truoc_thue=nqt_tt.nqt_so_tien,
        nqt_tien_thue=nqt_tien_thue,
        nqt_tong_cong=float(nqt_tt.nqt_so_tien) + nqt_tien_thue,
    )
    db.session.add(nqt_hd)


@nqt_thanh_toan_bp.route('/nqt-thanh-toan/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_thanh_toan(nqt_id):
    nqt_row = NqtThanhToan.query.get_or_404(nqt_id)
    nqt_result = nqt_row.nqt_to_dict()
    if nqt_row.nqt_hoa_don:
        nqt_result['nqt_hoa_don'] = nqt_row.nqt_hoa_don.nqt_to_dict()
    return nqt_ok(nqt_result)


@nqt_thanh_toan_bp.route('/nqt-thanh-toan/<int:nqt_id>/nqt-xac-nhan', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_xac_nhan_thanh_toan(nqt_id):
    nqt_row = NqtThanhToan.query.get_or_404(nqt_id)
    if nqt_row.nqt_trang_thai == 'thanh_cong':
        return nqt_loi('Thanh toán đã được xác nhận trước đó')
    nqt_row.nqt_trang_thai = 'thanh_cong'
    nqt_row.nqt_ngay_thanh_toan = datetime.utcnow()
    if not nqt_row.nqt_hoa_don:
        nqt_xuat_hoa_don(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Xác nhận thanh toán thành công')
