from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_dich_vu_phu import G6DichVuPhu, G6DatDichVu
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nxv_dich_vu_phu_bp = Blueprint('nxv_dich_vu_phu', __name__, url_prefix='/api')


# ============================================================
# DỊCH VỤ PHỤ
# ============================================================

@nxv_dich_vu_phu_bp.route('/nxv-dich-vu-phu', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_dich_vu():
    nxv_cn = request.args.get('g6_ma_chi_nhanh', type=int)
    nxv_loai = request.args.get('g6_loai_dich_vu', '').strip()

    nxv_q = G6DichVuPhu.query.filter_by(g6_la_hoat_dong=True)
    if nxv_cn:
        nxv_q = nxv_q.filter_by(g6_ma_chi_nhanh=nxv_cn)
    if nxv_loai:
        nxv_q = nxv_q.filter_by(g6_loai_dich_vu=nxv_loai)

    return nqt_ok([d.g6_to_dict() for d in nxv_q.all()])


@nxv_dich_vu_phu_bp.route('/nxv-dich-vu-phu/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chi_tiet_dv(nxv_id):
    nxv_row = G6DichVuPhu.query.get_or_404(nxv_id)
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_dich_vu_phu_bp.route('/nxv-dich-vu-phu', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_dich_vu():
    nxv_data = request.get_json() or {}
    nxv_ten = nxv_data.get('g6_ten_dich_vu', '').strip()
    nxv_loai = nxv_data.get('g6_loai_dich_vu', '').strip()
    nxv_cn = nxv_data.get('g6_ma_chi_nhanh')
    if not nxv_ten or not nxv_loai or not nxv_cn:
        return nqt_loi('Thiếu tên dịch vụ, loại hoặc chi nhánh')

    nxv_row = G6DichVuPhu(
        g6_ma_chi_nhanh=nxv_cn,
        g6_ten_dich_vu=nxv_ten,
        g6_loai_dich_vu=nxv_loai,
        g6_mo_ta=nxv_data.get('g6_mo_ta'),
        g6_gia_theo_luot=nxv_data.get('g6_gia_theo_luot', 0),
        g6_thoi_luong_phut=nxv_data.get('g6_thoi_luong_phut', 60),
        g6_suc_chua=nxv_data.get('g6_suc_chua'),
        g6_la_mien_phi_goi=nxv_data.get('g6_la_mien_phi_goi', False),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo dịch vụ phụ thành công', 201)


@nxv_dich_vu_phu_bp.route('/nxv-dich-vu-phu/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_dv(nxv_id):
    nxv_row = G6DichVuPhu.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_ten_dich_vu', 'g6_loai_dich_vu', 'g6_mo_ta', 'g6_gia_theo_luot',
                  'g6_thoi_luong_phut', 'g6_suc_chua', 'g6_la_mien_phi_goi', 'g6_la_hoat_dong']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_dich_vu_phu_bp.route('/nxv-dich-vu-phu/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_dv(nxv_id):
    nxv_row = G6DichVuPhu.query.get_or_404(nxv_id)
    nxv_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn dịch vụ phụ')


# ============================================================
# ĐẶT DỊCH VỤ
# ============================================================

@nxv_dich_vu_phu_bp.route('/nxv-dat-dich-vu', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_dat_dv():
    nxv_dv_id = request.args.get('g6_ma_dich_vu', type=int)
    nxv_hv_id = request.args.get('g6_ma_hoi_vien', type=int)
    nxv_tt = request.args.get('g6_trang_thai', '').strip()

    nxv_q = G6DatDichVu.query
    if nxv_dv_id:
        nxv_q = nxv_q.filter_by(g6_ma_dich_vu=nxv_dv_id)
    if nxv_hv_id:
        nxv_q = nxv_q.filter_by(g6_ma_hoi_vien=nxv_hv_id)
    if nxv_tt:
        nxv_q = nxv_q.filter_by(g6_trang_thai=nxv_tt)

    return nqt_ok([d.g6_to_dict() for d in nxv_q.order_by(G6DatDichVu.g6_ngay_tao.desc()).all()])


@nxv_dich_vu_phu_bp.route('/nxv-dat-dich-vu', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_dat_dv():
    nxv_data = request.get_json() or {}
    nxv_dv_id = nxv_data.get('g6_ma_dich_vu')
    nxv_hv_id = nxv_data.get('g6_ma_hoi_vien')
    nxv_bd = nxv_data.get('g6_thoi_gian_bat_dau')
    nxv_kt = nxv_data.get('g6_thoi_gian_ket_thuc')
    if not all([nxv_dv_id, nxv_hv_id, nxv_bd, nxv_kt]):
        return nqt_loi('Thiếu thông tin đặt dịch vụ')

    G6DichVuPhu.query.get_or_404(nxv_dv_id)
    nxv_row = G6DatDichVu(
        g6_ma_dich_vu=nxv_dv_id,
        g6_ma_hoi_vien=nxv_hv_id,
        g6_thoi_gian_bat_dau=nxv_bd,
        g6_thoi_gian_ket_thuc=nxv_kt,
        g6_la_mien_phi=nxv_data.get('g6_la_mien_phi', False),
        g6_ghi_chu=nxv_data.get('g6_ghi_chu'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Đặt dịch vụ thành công', 201)


@nxv_dich_vu_phu_bp.route('/nxv-dat-dich-vu/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_dat_dv(nxv_id):
    nxv_row = G6DatDichVu.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_trang_thai', 'g6_ghi_chu', 'g6_ma_thanh_toan']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())
