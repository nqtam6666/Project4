from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_thanh_toan import G6ThanhToan, G6HoaDon
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen
from datetime import datetime
import random
import string

nqt_thanh_toan_bp = Blueprint('g6_thanh_toan', __name__, url_prefix='/api')


@nqt_thanh_toan_bp.route('/nqt-thanh-toan', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_KHO')
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
@nqt_yeu_cau_quyen('QL_KHO')
def nqt_tao_thanh_toan():
    nqt_data = request.get_json() or {}
    nqt_so_tien = nqt_data.get('g6_so_tien', 0)
    nqt_loai = nqt_data.get('g6_loai_giao_dich', 'don_hang')
    nqt_phuong_thuc = nqt_data.get('g6_phuong_thuc', 'cod')

    if float(nqt_so_tien) <= 0:
        return nqt_loi('Số tiền không hợp lệ')

    nqt_row = G6ThanhToan(
        g6_ma_nguoi_dung=nqt_data.get('g6_ma_khach_hang') or nqt_data.get('g6_ma_nguoi_dung'),
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
    nqt_vat = float(NqtDichVuCauHinh.g6_lay('g6_thue_vat_phan_tram', nqt_mac_dinh=0) or 0)
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
@nqt_yeu_cau_quyen('QL_KHO')
def nqt_lay_thanh_toan(nqt_id):
    nqt_row = G6ThanhToan.query.get_or_404(nqt_id)
    nqt_result = nqt_row.g6_to_dict()
    if nqt_row.g6_hoa_don:
        nqt_result['g6_hoa_don'] = nqt_row.g6_hoa_don.g6_to_dict()
    return nqt_ok(nqt_result)


@nqt_thanh_toan_bp.route('/nqt-thanh-toan/<int:nqt_id>/nqt-huy', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_KHO')
def nqt_huy_thanh_toan(nqt_id):
    nqt_row = G6ThanhToan.query.get_or_404(nqt_id)
    if nqt_row.g6_trang_thai == 'thanh_cong':
        return nqt_loi('Không thể huỷ thanh toán đã hoàn thành', nqt_ma_trang=400)
    if nqt_row.g6_trang_thai == 'da_huy':
        return nqt_loi('Thanh toán đã bị huỷ trước đó', nqt_ma_trang=400)
    nqt_data = request.get_json() or {}
    nqt_row.g6_trang_thai = 'da_huy'
    nqt_row.g6_ghi_chu = nqt_data.get('g6_ly_do_huy') or nqt_row.g6_ghi_chu
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Đã huỷ thanh toán')


@nqt_thanh_toan_bp.route('/nqt-thanh-toan/<int:nqt_id>/nqt-hoan-tien', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_KHO')
def nqt_hoan_tien(nqt_id):
    nqt_row = G6ThanhToan.query.get_or_404(nqt_id)
    if nqt_row.g6_trang_thai != 'thanh_cong':
        return nqt_loi('Chỉ hoàn tiền được cho thanh toán đã thành công', nqt_ma_trang=400)
    nqt_data = request.get_json() or {}
    nqt_row.g6_trang_thai = 'hoan_tien'
    nqt_row.g6_ghi_chu = nqt_data.get('g6_ly_do_hoan') or nqt_row.g6_ghi_chu
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Đã ghi nhận hoàn tiền')


@nqt_thanh_toan_bp.route('/nqt-thanh-toan/<int:nqt_id>/nqt-xac-nhan', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_KHO')
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


@nqt_thanh_toan_bp.route('/nqt-thanh-toan/nqt-check-transactions', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_KHO')
def nqt_check_transactions():
    import urllib.request
    import json
    from backend.app.models.g6_don_hang import G6DonHang, G6LichSuDonHang
    from backend.app.models.g6_thanh_toan import G6ThanhToan

    import os
    domain = os.environ.get('DOMAIN_CHECK', '')
    api_key = os.environ.get('API_KEY_CHECK', '')
    url = f"{domain}/api/v1/bank-transactions?api_key={api_key}&bank=MB&type=IN&page=1&limit=50"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return nqt_loi(f"Lỗi khi kết nối tới checkgd.vn: {str(e)}")

    if not res_data.get('status'):
        return nqt_loi(f"API checkgd.vn báo lỗi: {res_data.get('messages')}")

    transactions = res_data.get('transactions', [])
    matched_orders = []
    matched_payments = []

    pending_payments = G6ThanhToan.query.filter_by(g6_trang_thai='cho_xu_ly').all()
    pending_orders = G6DonHang.query.filter_by(g6_trang_thai='cho_xac_nhan').all()

    for trans in transactions:
        desc = trans.get('description', '')
        amount = float(trans.get('amount', 0))
        tx_id = trans.get('transaction_id')

        # 1. Match G6ThanhToan
        for tt in pending_payments:
            if float(tt.g6_so_tien) == amount:
                if str(tt.g6_ma_thanh_toan) in desc or f"HD{tt.g6_ma_thanh_toan}" in desc or f"GD{tt.g6_ma_thanh_toan}" in desc:
                    tt.g6_trang_thai = 'thanh_cong'
                    tt.g6_ngay_thanh_toan = datetime.utcnow()
                    tt.g6_ma_giao_dich_cong = tx_id
                    tt.g6_du_lieu_tra_ve = trans
                    if not tt.g6_hoa_don:
                        nqt_xuat_hoa_don(tt)
                    matched_payments.append(tt.g6_ma_thanh_toan)

        # 2. Match G6DonHang
        for o in pending_orders:
            if float(o.g6_tong_thanh_toan) == amount:
                if str(o.g6_ma_don_hang) in desc or f"DH{o.g6_ma_don_hang}" in desc or f"DH-{o.g6_ma_don_hang}" in desc:
                    o.g6_trang_thai = 'dang_xu_ly'
                    ls = G6LichSuDonHang(
                        g6_ma_don_hang=o.g6_ma_don_hang,
                        g6_trang_thai_moi='dang_xu_ly',
                        g6_ghi_chu=f"Xác nhận thanh toán tự động qua MBBank, mã GD: {tx_id}",
                    )
                    db.session.add(ls)

                    new_tt = G6ThanhToan(
                        g6_ma_nguoi_dung=o.g6_ma_nguoi_dung,
                        g6_loai_giao_dich='don_hang',
                        g6_so_tien=amount,
                        g6_phuong_thuc='bank_transfer',
                        g6_trang_thai='thanh_cong',
                        g6_ma_giao_dich_cong=tx_id,
                        g6_du_lieu_tra_ve=trans,
                        g6_ngay_thanh_toan=datetime.utcnow(),
                        g6_ghi_chu=f"Tự động tạo từ đơn hàng #{o.g6_ma_don_hang}",
                    )
                    db.session.add(new_tt)
                    db.session.flush()
                    nqt_xuat_hoa_don(new_tt)
                    matched_orders.append(o.g6_ma_don_hang)

    if matched_orders or matched_payments:
        db.session.commit()

    return nqt_ok({
        'matched_orders': matched_orders,
        'matched_payments': matched_payments,
        'total_scanned': len(transactions)
    }, "Đã đồng bộ giao dịch ngân hàng thành công")
