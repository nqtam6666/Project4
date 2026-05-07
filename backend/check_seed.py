import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import nqt_tao_app, db
from backend.app.models.g6_nguoi_dung import G6QuyenHan

app = nqt_tao_app()

with app.app_context():
    quyen_list = G6QuyenHan.query.all()
    print("SỐ LƯỢNG QUYỀN TRONG DB:", len(quyen_list))
    for q in quyen_list:
        print(q.g6_to_dict())
