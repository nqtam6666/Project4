from flask import jsonify


def nqt_ok(nqt_du_lieu=None, nqt_thong_diep: str = 'Thành công', nqt_ma_trang: int = 200):
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': nqt_du_lieu,
        'nqt_thong_diep': nqt_thong_diep,
        'nqt_loi': [],
    }), nqt_ma_trang


def nqt_loi(nqt_thong_diep: str = 'Lỗi', nqt_loi=None, nqt_ma_trang: int = 400):
    return jsonify({
        'nqt_thanh_cong': False,
        'nqt_du_lieu': None,
        'nqt_thong_diep': nqt_thong_diep,
        'nqt_loi': nqt_loi if isinstance(nqt_loi, list) else ([nqt_loi] if nqt_loi else []),
    }), nqt_ma_trang
