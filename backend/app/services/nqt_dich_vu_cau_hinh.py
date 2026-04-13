from backend.app import db


class NqtDichVuCauHinh:
    _nqt_bo_nho_cache = {}

    @classmethod
    def nqt_lay(cls, nqt_khoa: str, nqt_mac_dinh=None):
        from backend.app.models.nqt_cau_hinh import NqtCauHinh
        if nqt_khoa in cls._nqt_bo_nho_cache:
            return cls._nqt_bo_nho_cache[nqt_khoa]
        nqt_row = NqtCauHinh.query.filter_by(nqt_khoa=nqt_khoa).first()
        if not nqt_row:
            return nqt_mac_dinh
        nqt_gia_tri = cls._nqt_ep_kieu(nqt_row.nqt_gia_tri, nqt_row.nqt_kieu_du_lieu)
        cls._nqt_bo_nho_cache[nqt_khoa] = nqt_gia_tri
        return nqt_gia_tri

    @classmethod
    def nqt_cap_nhat(cls, nqt_khoa: str, nqt_gia_tri):
        from backend.app.models.nqt_cau_hinh import NqtCauHinh
        nqt_row = NqtCauHinh.query.filter_by(nqt_khoa=nqt_khoa).first()
        if nqt_row:
            nqt_row.nqt_gia_tri = str(nqt_gia_tri)
            db.session.commit()
            cls._nqt_bo_nho_cache.pop(nqt_khoa, None)

    @classmethod
    def nqt_xoa_cache(cls):
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
