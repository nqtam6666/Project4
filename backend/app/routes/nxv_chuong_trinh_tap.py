from flask import Blueprint, request
from backend.app import db
from backend.app.models.nxv_chuong_trinh_tap import NxvChuongTrinhTapLuyen, NxvBaiTapTrongNgay
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap
from datetime import datetime

nxv_chuong_trinh_tap_bp = Blueprint('nxv_chuong_trinh_tap', __name__, url_prefix='/api')


# ---- CHƯƠNG TRÌNH TẬP LUYỆN ----

@nxv_chuong_trinh_tap_bp.route('/nxv-chuong-trinh-tap', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chuong_trinh_tap():
    nxv_hv_id = request.args.get('nxv_ma_hoi_vien', type=int)
    nxv_hlv_id = request.args.get('nxv_ma_hlv', type=int)
    nxv_trang_thai = request.args.get('nxv_trang_thai')

    nxv_q = NxvChuongTrinhTapLuyen.query.filter(NxvChuongTrinhTapLuyen.g6_deleted_at == None)
    if nxv_hv_id:
        nxv_q = nxv_q.filter_by(nxv_ma_hoi_vien=nxv_hv_id)
    if nxv_hlv_id:
        nxv_q = nxv_q.filter_by(nxv_ma_hlv=nxv_hlv_id)
    if nxv_trang_thai:
        nxv_q = nxv_q.filter_by(nxv_trang_thai=nxv_trang_thai)

    nxv_list = nxv_q.order_by(NxvChuongTrinhTapLuyen.nxv_ngay_tao.desc()).all()
    return nqt_ok([c.nxv_to_dict() for c in nxv_list])


@nxv_chuong_trinh_tap_bp.route('/nxv-chuong-trinh-tap/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chuong_trinh_chi_tiet(nxv_id):
    nxv_row = NxvChuongTrinhTapLuyen.query.get_or_404(nxv_id)
    nxv_result = nxv_row.nxv_to_dict()
    nxv_result['nxv_bai_tap'] = [
        b.nxv_to_dict() for b in nxv_row.nxv_bai_tap
        if b.g6_deleted_at is None
    ]
    return nqt_ok(nxv_result)


@nxv_chuong_trinh_tap_bp.route('/nxv-chuong-trinh-tap', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_chuong_trinh_tap():
    nxv_data = request.get_json() or {}
    nxv_hv_id = nxv_data.get('nxv_ma_hoi_vien')
    nxv_ten = nxv_data.get('nxv_ten', '').strip()
    nxv_ngay_bd = nxv_data.get('nxv_ngay_bat_dau')
    if not nxv_hv_id or not nxv_ten or not nxv_ngay_bd:
        return nqt_loi('Thiếu mã hội viên, tên hoặc ngày bắt đầu')
    nxv_row = NxvChuongTrinhTapLuyen(
        nxv_ma_hoi_vien=nxv_hv_id,
        nxv_ma_hlv=nxv_data.get('nxv_ma_hlv'),
        nxv_ten=nxv_ten,
        nxv_muc_tieu=nxv_data.get('nxv_muc_tieu'),
        nxv_so_tuan=nxv_data.get('nxv_so_tuan', 4),
        nxv_ngay_bat_dau=nxv_ngay_bd,
        nxv_ghi_chu=nxv_data.get('nxv_ghi_chu'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Tạo chương trình tập thành công', 201)


@nxv_chuong_trinh_tap_bp.route('/nxv-chuong-trinh-tap/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_chuong_trinh(nxv_id):
    nxv_row = NxvChuongTrinhTapLuyen.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['nxv_ten', 'nxv_muc_tieu', 'nxv_so_tuan', 'nxv_ngay_ket_thuc', 'nxv_ghi_chu', 'nxv_trang_thai']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Cập nhật chương trình tập thành công')


@nxv_chuong_trinh_tap_bp.route('/nxv-chuong-trinh-tap/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_chuong_trinh(nxv_id):
    nxv_row = NxvChuongTrinhTapLuyen.query.get_or_404(nxv_id)
    nxv_row.g6_deleted_at = datetime.utcnow()
    db.session.commit()
    return nqt_ok(None, 'Đã xoá chương trình tập')


# ---- BÀI TẬP TRONG NGÀY ----

@nxv_chuong_trinh_tap_bp.route('/nxv-chuong-trinh-tap/<int:nxv_ct_id>/nxv-bai-tap', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_them_bai_tap(nxv_ct_id):
    NxvChuongTrinhTapLuyen.query.get_or_404(nxv_ct_id)
    nxv_data = request.get_json() or {}
    nxv_ten = nxv_data.get('nxv_ten_bai_tap', '').strip()
    if not nxv_ten:
        return nqt_loi('Thiếu tên bài tập')
    nxv_row = NxvBaiTapTrongNgay(
        nxv_ma_chuong_trinh=nxv_ct_id,
        nxv_tuan=nxv_data.get('nxv_tuan', 1),
        nxv_ngay_trong_tuan=nxv_data.get('nxv_ngay_trong_tuan', 1),
        nxv_ten_bai_tap=nxv_ten,
        nxv_nhom_co=nxv_data.get('nxv_nhom_co'),
        nxv_so_hieu=nxv_data.get('nxv_so_hieu'),
        nxv_so_set=nxv_data.get('nxv_so_set'),
        nxv_so_rep=nxv_data.get('nxv_so_rep'),
        nxv_trong_luong_kg=nxv_data.get('nxv_trong_luong_kg'),
        nxv_thoi_gian_nghi_giay=nxv_data.get('nxv_thoi_gian_nghi_giay'),
        nxv_ghi_chu=nxv_data.get('nxv_ghi_chu'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Thêm bài tập thành công', 201)


@nxv_chuong_trinh_tap_bp.route('/nxv-bai-tap/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_bai_tap(nxv_id):
    nxv_row = NxvBaiTapTrongNgay.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in [
        'nxv_ten_bai_tap', 'nxv_nhom_co', 'nxv_so_hieu', 'nxv_so_set',
        'nxv_so_rep', 'nxv_trong_luong_kg', 'nxv_thoi_gian_nghi_giay',
        'nxv_ghi_chu', 'nxv_la_hoan_thanh',
    ]:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict())


@nxv_chuong_trinh_tap_bp.route('/nxv-bai-tap/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_bai_tap(nxv_id):
    nxv_row = NxvBaiTapTrongNgay.query.get_or_404(nxv_id)
    nxv_row.g6_deleted_at = datetime.utcnow()
    db.session.commit()
    return nqt_ok(None, 'Đã xoá bài tập')
