from flask import Blueprint, request
from backend.app import db
from backend.app.models.nxv_danh_gia import NxvDanhGiaHLV, NxvDanhGiaLopHoc
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nxv_danh_gia_bp = Blueprint('nxv_danh_gia', __name__, url_prefix='/api')


# ---- ĐÁNH GIÁ HLV ----

@nxv_danh_gia_bp.route('/nxv-danh-gia-hlv', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_danh_gia_hlv():
    nxv_hlv_id = request.args.get('g6_ma_hlv', type=int)
    nxv_trang_thai = request.args.get('nxv_trang_thai')
    nxv_trang = request.args.get('g6_trang', 1, type=int)

    nxv_q = NxvDanhGiaHLV.query.filter(NxvDanhGiaHLV.g6_deleted_at == None)
    if nxv_hlv_id:
        nxv_q = nxv_q.filter_by(nxv_ma_hlv=nxv_hlv_id)
    if nxv_trang_thai:
        nxv_q = nxv_q.filter_by(nxv_trang_thai=nxv_trang_thai)

    nxv_phan_trang = nxv_q.order_by(NxvDanhGiaHLV.nxv_ngay_tao.desc()).paginate(
        page=nxv_trang, per_page=20, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [d.nxv_to_dict() for d in nxv_phan_trang.items],
        'g6_tong': nxv_phan_trang.total,
        'g6_trang': nxv_trang,
    })


@nxv_danh_gia_bp.route('/nxv-danh-gia-hlv', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_danh_gia_hlv():
    nxv_data = request.get_json() or {}
    nxv_hlv_id = nxv_data.get('nxv_ma_hlv')
    nxv_sao = nxv_data.get('nxv_sao', 5)
    if not nxv_hlv_id:
        return nqt_loi('Thiếu mã HLV')
    if not (1 <= int(nxv_sao) <= 5):
        return nqt_loi('Số sao không hợp lệ (1-5)')
    nxv_row = NxvDanhGiaHLV(
        nxv_ma_hlv=nxv_hlv_id,
        nxv_ma_hoi_vien=nxv_data.get('nxv_ma_hoi_vien'),
        nxv_ma_dang_ky_pt=nxv_data.get('nxv_ma_dang_ky_pt'),
        nxv_sao=nxv_sao,
        nxv_noi_dung=nxv_data.get('nxv_noi_dung'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Cảm ơn bạn đã đánh giá HLV', 201)


@nxv_danh_gia_bp.route('/nxv-danh-gia-hlv/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_danh_gia_hlv(nxv_id):
    nxv_row = NxvDanhGiaHLV.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['nxv_trang_thai', 'nxv_phan_hoi_hlv']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict())


@nxv_danh_gia_bp.route('/nxv-danh-gia-hlv/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_danh_gia_hlv(nxv_id):
    from datetime import datetime
    nxv_row = NxvDanhGiaHLV.query.get_or_404(nxv_id)
    nxv_row.g6_deleted_at = datetime.utcnow()
    db.session.commit()
    return nqt_ok(None, 'Đã xoá đánh giá HLV')


# ---- ĐÁNH GIÁ LỚP HỌC ----

@nxv_danh_gia_bp.route('/nxv-danh-gia-lop-hoc', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_danh_gia_lop_hoc():
    nxv_lop_id = request.args.get('nxv_ma_lop_hoc', type=int)
    nxv_trang_thai = request.args.get('nxv_trang_thai')
    nxv_trang = request.args.get('g6_trang', 1, type=int)

    nxv_q = NxvDanhGiaLopHoc.query.filter(NxvDanhGiaLopHoc.g6_deleted_at == None)
    if nxv_lop_id:
        nxv_q = nxv_q.filter_by(nxv_ma_lop_hoc=nxv_lop_id)
    if nxv_trang_thai:
        nxv_q = nxv_q.filter_by(nxv_trang_thai=nxv_trang_thai)

    nxv_phan_trang = nxv_q.order_by(NxvDanhGiaLopHoc.nxv_ngay_tao.desc()).paginate(
        page=nxv_trang, per_page=20, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [d.nxv_to_dict() for d in nxv_phan_trang.items],
        'g6_tong': nxv_phan_trang.total,
        'g6_trang': nxv_trang,
    })


@nxv_danh_gia_bp.route('/nxv-danh-gia-lop-hoc', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_danh_gia_lop_hoc():
    nxv_data = request.get_json() or {}
    nxv_lop_id = nxv_data.get('nxv_ma_lop_hoc')
    nxv_sao = nxv_data.get('nxv_sao', 5)
    if not nxv_lop_id:
        return nqt_loi('Thiếu mã lớp học')
    if not (1 <= int(nxv_sao) <= 5):
        return nqt_loi('Số sao không hợp lệ (1-5)')
    nxv_row = NxvDanhGiaLopHoc(
        nxv_ma_lop_hoc=nxv_lop_id,
        nxv_ma_hoi_vien=nxv_data.get('nxv_ma_hoi_vien'),
        nxv_ma_dat_cho=nxv_data.get('nxv_ma_dat_cho'),
        nxv_sao=nxv_sao,
        nxv_noi_dung=nxv_data.get('nxv_noi_dung'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Cảm ơn bạn đã đánh giá lớp học', 201)


@nxv_danh_gia_bp.route('/nxv-danh-gia-lop-hoc/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_danh_gia_lop_hoc(nxv_id):
    nxv_row = NxvDanhGiaLopHoc.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['nxv_trang_thai', 'nxv_phan_hoi_hlv']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict())


@nxv_danh_gia_bp.route('/nxv-danh-gia-lop-hoc/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_danh_gia_lop_hoc(nxv_id):
    from datetime import datetime
    nxv_row = NxvDanhGiaLopHoc.query.get_or_404(nxv_id)
    nxv_row.g6_deleted_at = datetime.utcnow()
    db.session.commit()
    return nqt_ok(None, 'Đã xoá đánh giá lớp học')
