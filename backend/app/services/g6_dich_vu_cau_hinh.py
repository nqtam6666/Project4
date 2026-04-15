from backend.app import db


class NqtDichVuCauHinh:
    _nqt_bo_nho_cache = {}

    @classmethod
    def g6_lay(cls, nqt_khoa: str, nqt_mac_dinh=None):
        from backend.app.models.g6_cau_hinh import G6CauHinh
        if nqt_khoa in cls._nqt_bo_nho_cache:
            return cls._nqt_bo_nho_cache[nqt_khoa]
        nqt_row = G6CauHinh.query.filter_by(g6_khoa=nqt_khoa).first()
        if not nqt_row:
            return nqt_mac_dinh
        nqt_gia_tri = cls._nqt_ep_kieu(nqt_row.g6_gia_tri, nqt_row.g6_kieu_du_lieu)
        cls._nqt_bo_nho_cache[nqt_khoa] = nqt_gia_tri
        return nqt_gia_tri

    @classmethod
    def g6_cap_nhat(cls, nqt_khoa: str, nqt_gia_tri, nqt_nhom: str = 'website'):
        from backend.app.models.g6_cau_hinh import G6CauHinh
        nqt_row = G6CauHinh.query.filter_by(g6_khoa=nqt_khoa).first()
        if nqt_row:
            nqt_row.g6_gia_tri = str(nqt_gia_tri)
            nqt_row.g6_nhom = nqt_nhom
        else:
            nqt_row = G6CauHinh(
                g6_khoa=nqt_khoa,
                g6_gia_tri=str(nqt_gia_tri),
                g6_nhom=nqt_nhom,
                g6_kieu_du_lieu='string',
            )
            db.session.add(nqt_row)
        db.session.commit()
        cls._nqt_bo_nho_cache.pop(nqt_khoa, None)

    @classmethod
    def g6_xoa_cache(cls):
        cls._nqt_bo_nho_cache.clear()

    @staticmethod
    def _nqt_ep_kieu(nqt_gia_tri: str, nqt_kieu: str):
        if nqt_gia_tri is None:
            return None
        if nqt_kieu == 'int':
            return int(nqt_gia_tri)
        if nqt_kieu == 'bool':
            return nqt_gia_tri in ('1', 'true', 'True')
        if nqt_kieu == 'json':
            import json
            return json.loads(nqt_gia_tri)
        return nqt_gia_tri
