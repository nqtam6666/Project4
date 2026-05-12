from flask import Blueprint, request
from backend.app import db
from backend.app.models.nxv_bao_tri import NxvLichSuBaoTri, NxvPhieuSuaChua
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_ghi_nhat_ky
from datetime import datetime
import random
import string

nxv_bao_tri_bp = Blueprint('nxv_bao_tri', __name__, url_prefix='/api')


def _nxv_tao_so_phieu():
    nxv_prefix = datetime.utcnow().strftime('PT%Y%m%d')
    nxv_suffix = ''.join(random.choices(string.digits, k=4))
    return f'{nxv_prefix}{nxv_suffix}'


# ---- LỊCH SỬ BẢO TRÌ ----

@nxv_bao_tri_bp.route('/nxv-bao-tri', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_bao_tri():
    nxv_tb_id = request.args.get('nxv_ma_thiet_bi', type=int)
    nxv_cn_id = request.args.get('nxv_ma_chi_nhanh', type=int)
    nxv_loai = request.args.get('nxv_loai')
    nxv_trang = request.args.get('g6_trang', 1, type=int)

    nxv_q = NxvLichSuBaoTri.query.filter(NxvLichSuBaoTri.g6_deleted_at == None)
    if nxv_tb_id:
        nxv_q = nxv_q.filter_by(nxv_ma_thiet_bi=nxv_tb_id)
    if nxv_cn_id:
        nxv_q = nxv_q.filter_by(nxv_ma_chi_nhanh=nxv_cn_id)
    if nxv_loai:
        nxv_q = nxv_q.filter_by(nxv_loai=nxv_loai)

    nxv_phan_trang = nxv_q.order_by(NxvLichSuBaoTri.nxv_ngay_bao_tri.desc()).paginate(
        page=nxv_trang, per_page=20, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [b.nxv_to_dict() for b in nxv_phan_trang.items],
        'g6_tong': nxv_phan_trang.total,
        'g6_trang': nxv_trang,
    })


@nxv_bao_tri_bp.route('/nxv-bao-tri/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_bao_tri_chi_tiet(nxv_id):
    nxv_row = NxvLichSuBaoTri.query.get_or_404(nxv_id)
    return nqt_ok(nxv_row.nxv_to_dict())


@nxv_bao_tri_bp.route('/nxv-bao-tri', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_ghi_nhat_ky('Thêm lịch bảo trì', 'NxvLichSuBaoTri')
def nxv_tao_bao_tri():
    nxv_data = request.get_json() or {}
    nxv_tb_id = nxv_data.get('nxv_ma_thiet_bi')
    nxv_ngay = nxv_data.get('nxv_ngay_bao_tri')
    nxv_noi_dung = nxv_data.get('nxv_noi_dung', '').strip()
    if not nxv_tb_id or not nxv_ngay or not nxv_noi_dung:
        return nqt_loi('Thiếu mã thiết bị, ngày bảo trì hoặc nội dung')
    nxv_row = NxvLichSuBaoTri(
        nxv_ma_thiet_bi=nxv_tb_id,
        nxv_ma_chi_nhanh=nxv_data.get('nxv_ma_chi_nhanh'),
        nxv_loai=nxv_data.get('nxv_loai', 'dinh_ky'),
        nxv_ngay_bao_tri=nxv_ngay,
        nxv_nguoi_thuc_hien=nxv_data.get('nxv_nguoi_thuc_hien'),
        nxv_noi_dung=nxv_noi_dung,
        nxv_chi_phi=nxv_data.get('nxv_chi_phi', 0),
        nxv_ngay_bao_tri_tiep_theo=nxv_data.get('nxv_ngay_bao_tri_tiep_theo'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Tạo lịch bảo trì thành công', 201)


@nxv_bao_tri_bp.route('/nxv-bao-tri/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_ghi_nhat_ky('Cập nhật lịch bảo trì', 'NxvLichSuBaoTri')
def nxv_cap_nhat_bao_tri(nxv_id):
    nxv_row = NxvLichSuBaoTri.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in [
        'nxv_ngay_hoan_thanh', 'nxv_nguoi_thuc_hien', 'nxv_noi_dung',
        'nxv_chi_phi', 'nxv_ket_qua', 'nxv_ghi_chu', 'nxv_ngay_bao_tri_tiep_theo',
    ]:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Cập nhật bảo trì thành công')


@nxv_bao_tri_bp.route('/nxv-bao-tri/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
@nqt_ghi_nhat_ky('Xóa lịch bảo trì', 'NxvLichSuBaoTri')
def nxv_xoa_bao_tri(nxv_id):
    nxv_row = NxvLichSuBaoTri.query.get_or_404(nxv_id)
    nxv_row.g6_deleted_at = datetime.utcnow()
    db.session.commit()
    return nqt_ok(None, 'Đã xoá lịch bảo trì')


# ---- PHIẾU SỬA CHỮA ----

@nxv_bao_tri_bp.route('/nxv-phieu-sua-chua', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_phieu_sua_chua():
    nxv_tb_id = request.args.get('nxv_ma_thiet_bi', type=int)
    nxv_trang_thai = request.args.get('nxv_trang_thai')
    nxv_trang = request.args.get('g6_trang', 1, type=int)

    nxv_q = NxvPhieuSuaChua.query.filter(NxvPhieuSuaChua.g6_deleted_at == None)
    if nxv_tb_id:
        nxv_q = nxv_q.filter_by(nxv_ma_thiet_bi=nxv_tb_id)
    if nxv_trang_thai:
        nxv_q = nxv_q.filter_by(nxv_trang_thai=nxv_trang_thai)

    nxv_phan_trang = nxv_q.order_by(NxvPhieuSuaChua.nxv_ngay_tao.desc()).paginate(
        page=nxv_trang, per_page=20, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [p.nxv_to_dict() for p in nxv_phan_trang.items],
        'g6_tong': nxv_phan_trang.total,
        'g6_trang': nxv_trang,
    })


@nxv_bao_tri_bp.route('/nxv-phieu-sua-chua/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_phieu_chi_tiet(nxv_id):
    nxv_row = NxvPhieuSuaChua.query.get_or_404(nxv_id)
    return nqt_ok(nxv_row.nxv_to_dict())


@nxv_bao_tri_bp.route('/nxv-phieu-sua-chua', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_ghi_nhat_ky('Tạo phiếu sửa chữa', 'NxvPhieuSuaChua')
def nxv_tao_phieu_sua_chua():
    nxv_data = request.get_json() or {}
    nxv_tb_id = nxv_data.get('nxv_ma_thiet_bi')
    nxv_mo_ta = nxv_data.get('nxv_mo_ta_su_co', '').strip()
    nxv_ngay = nxv_data.get('nxv_ngay_tao_phieu')
    if not nxv_tb_id or not nxv_mo_ta or not nxv_ngay:
        return nqt_loi('Thiếu mã thiết bị, mô tả sự cố hoặc ngày')
    nxv_row = NxvPhieuSuaChua(
        nxv_ma_thiet_bi=nxv_tb_id,
        nxv_ma_chi_nhanh=nxv_data.get('nxv_ma_chi_nhanh'),
        nxv_so_phieu=_nxv_tao_so_phieu(),
        nxv_ngay_tao_phieu=nxv_ngay,
        nxv_mo_ta_su_co=nxv_mo_ta,
        nxv_don_vi_sua_chua=nxv_data.get('nxv_don_vi_sua_chua'),
        nxv_chi_phi_du_kien=nxv_data.get('nxv_chi_phi_du_kien'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Tạo phiếu sửa chữa thành công', 201)


@nxv_bao_tri_bp.route('/nxv-phieu-sua-chua/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_ghi_nhat_ky('Cập nhật phiếu sửa chữa', 'NxvPhieuSuaChua')
def nxv_cap_nhat_phieu(nxv_id):
    nxv_row = NxvPhieuSuaChua.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in [
        'nxv_don_vi_sua_chua', 'nxv_chi_phi_du_kien', 'nxv_chi_phi_thuc_te',
        'nxv_ngay_gui_sua', 'nxv_ngay_nhan_lai', 'nxv_trang_thai', 'nxv_ket_qua_sua_chua',
    ]:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Cập nhật phiếu sửa chữa thành công')


@nxv_bao_tri_bp.route('/nxv-phieu-sua-chua/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
@nqt_ghi_nhat_ky('Xóa phiếu sửa chữa', 'NxvPhieuSuaChua')
def nxv_xoa_phieu(nxv_id):
    nxv_row = NxvPhieuSuaChua.query.get_or_404(nxv_id)
    nxv_row.g6_deleted_at = datetime.utcnow()
    db.session.commit()
    return nqt_ok(None, 'Đã xoá phiếu sửa chữa')
