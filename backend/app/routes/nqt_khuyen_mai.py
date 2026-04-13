from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_khuyen_mai import NqtMaGiamGia, NqtKhuyenMaiMuaKem, NqtBanner
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_khuyen_mai_bp = Blueprint('nqt_khuyen_mai', __name__, url_prefix='/api')


@nqt_khuyen_mai_bp.route('/nqt-ma-giam-gia', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_ma_giam_gia():
    nqt_list = NqtMaGiamGia.query.order_by(NqtMaGiamGia.nqt_ngay_tao.desc()).all()
    return nqt_ok([m.nqt_to_dict() for m in nqt_list])


@nqt_khuyen_mai_bp.route('/nqt-ma-giam-gia/nqt-kiem-tra', methods=['POST'])
def nqt_kiem_tra_ma_giam_gia():
    from datetime import datetime
    nqt_data = request.get_json() or {}
    nqt_ma = nqt_data.get('nqt_ma', '').strip().upper()
    nqt_tong = float(nqt_data.get('nqt_tong_tien', 0))
    nqt_row = NqtMaGiamGia.query.filter_by(nqt_ma=nqt_ma, nqt_la_hoat_dong=True).first()
    if not nqt_row:
        return nqt_loi('Mã giảm giá không hợp lệ', nqt_ma_trang=404)
    nqt_now = datetime.utcnow()
    if nqt_row.nqt_ngay_bat_dau > nqt_now:
        return nqt_loi('Mã giảm giá chưa có hiệu lực')
    if nqt_row.nqt_ngay_ket_thuc and nqt_row.nqt_ngay_ket_thuc < nqt_now:
        return nqt_loi('Mã giảm giá đã hết hạn')
    if nqt_row.nqt_so_luong_tong and nqt_row.nqt_so_luong_da_dung >= nqt_row.nqt_so_luong_tong:
        return nqt_loi('Mã giảm giá đã hết lượt sử dụng')
    if nqt_tong < float(nqt_row.nqt_don_hang_toi_thieu):
        return nqt_loi(f'Đơn hàng tối thiểu {int(nqt_row.nqt_don_hang_toi_thieu):,}đ')
    nqt_giam = 0
    if nqt_row.nqt_loai == 'phan_tram':
        nqt_giam = nqt_tong * float(nqt_row.nqt_gia_tri) / 100
        if nqt_row.nqt_gia_tri_toi_da:
            nqt_giam = min(nqt_giam, float(nqt_row.nqt_gia_tri_toi_da))
    else:
        nqt_giam = float(nqt_row.nqt_gia_tri)
    return nqt_ok({
        'nqt_ma_ma_giam_gia': nqt_row.nqt_ma_ma_giam_gia,
        'nqt_so_tien_giam': round(nqt_giam),
        'nqt_loai': nqt_row.nqt_loai,
    })


@nqt_khuyen_mai_bp.route('/nqt-ma-giam-gia', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_ma_giam_gia():
    nqt_data = request.get_json() or {}
    nqt_row = NqtMaGiamGia(
        nqt_ma=nqt_data.get('nqt_ma', '').upper(),
        nqt_loai=nqt_data.get('nqt_loai', 'phan_tram'),
        nqt_gia_tri=nqt_data.get('nqt_gia_tri', 0),
        nqt_don_hang_toi_thieu=nqt_data.get('nqt_don_hang_toi_thieu', 0),
        nqt_so_luong_tong=nqt_data.get('nqt_so_luong_tong'),
        nqt_ngay_bat_dau=nqt_data.get('nqt_ngay_bat_dau'),
        nqt_ngay_ket_thuc=nqt_data.get('nqt_ngay_ket_thuc'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo mã giảm giá thành công', 201)


@nqt_khuyen_mai_bp.route('/nqt-banner', methods=['GET'])
def nqt_lay_banner():
    nqt_vi_tri = request.args.get('nqt_vi_tri', 'slider')
    nqt_list = NqtBanner.query.filter_by(nqt_la_hoat_dong=True, nqt_vi_tri=nqt_vi_tri).order_by(
        NqtBanner.nqt_thu_tu
    ).all()
    return nqt_ok([b.nqt_to_dict() for b in nqt_list])


@nqt_khuyen_mai_bp.route('/nqt-banner', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_banner():
    nqt_data = request.get_json() or {}
    nqt_row = NqtBanner(
        nqt_tieu_de=nqt_data.get('nqt_tieu_de'),
        nqt_hinh_anh=nqt_data.get('nqt_hinh_anh', ''),
        nqt_duong_dan=nqt_data.get('nqt_duong_dan'),
        nqt_vi_tri=nqt_data.get('nqt_vi_tri', 'slider'),
        nqt_thu_tu=nqt_data.get('nqt_thu_tu', 0),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo banner thành công', 201)
