from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_thong_bao import NqtThongBao, NqtLichGuiThongBao
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_thong_bao_bp = Blueprint('nqt_thong_bao', __name__, url_prefix='/api')


@nqt_thong_bao_bp.route('/nqt-thong-bao', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_thong_bao():
    nqt_loai_nd = request.args.get('nqt_loai_nguoi_nhan')
    nqt_nd_id = request.args.get('nqt_ma_nguoi_nhan', type=int)
    nqt_q = NqtThongBao.query
    if nqt_loai_nd and nqt_nd_id:
        nqt_q = nqt_q.filter(
            (NqtThongBao.nqt_la_quang_ba == True) |
            ((NqtThongBao.nqt_loai_nguoi_nhan == nqt_loai_nd) &
             (NqtThongBao.nqt_ma_nguoi_nhan == nqt_nd_id))
        )
    else:
        nqt_q = nqt_q.filter_by(nqt_la_quang_ba=True)
    nqt_list = nqt_q.order_by(NqtThongBao.nqt_ngay_tao.desc()).limit(50).all()
    return nqt_ok([t.nqt_to_dict() for t in nqt_list])


@nqt_thong_bao_bp.route('/nqt-thong-bao', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_thong_bao():
    nqt_data = request.get_json() or {}
    nqt_row = NqtThongBao(
        nqt_tieu_de=nqt_data.get('nqt_tieu_de', ''),
        nqt_noi_dung=nqt_data.get('nqt_noi_dung', ''),
        nqt_loai=nqt_data.get('nqt_loai', 'in_app'),
        nqt_la_quang_ba=nqt_data.get('nqt_la_quang_ba', False),
        nqt_ma_nguoi_nhan=nqt_data.get('nqt_ma_nguoi_nhan'),
        nqt_loai_nguoi_nhan=nqt_data.get('nqt_loai_nguoi_nhan'),
        nqt_du_lieu_them=nqt_data.get('nqt_du_lieu_them'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Gửi thông báo thành công', 201)


@nqt_thong_bao_bp.route('/nqt-thong-bao/<int:nqt_id>/nqt-doc', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_danh_dau_da_doc(nqt_id):
    nqt_row = NqtThongBao.query.get_or_404(nqt_id)
    nqt_row.nqt_la_da_doc = True
    db.session.commit()
    return nqt_ok(None, 'Đã đánh dấu là đã đọc')


@nqt_thong_bao_bp.route('/nqt-lich-gui-thong-bao', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_lich_gui():
    nqt_list = NqtLichGuiThongBao.query.all()
    return nqt_ok([l.nqt_to_dict() for l in nqt_list])


@nqt_thong_bao_bp.route('/nqt-lich-gui-thong-bao/<int:nqt_id>/nqt-bat-tat', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_bat_tat_lich_gui(nqt_id):
    nqt_row = NqtLichGuiThongBao.query.get_or_404(nqt_id)
    nqt_row.nqt_la_hoat_dong = not nqt_row.nqt_la_hoat_dong
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())
