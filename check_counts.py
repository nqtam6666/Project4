import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import db, nqt_tao_app
from backend.app.models import G6DichVuPhu, G6LopHoc

app = nqt_tao_app()
with app.app_context():
    services = G6DichVuPhu.query.all()
    classes = G6LopHoc.query.all()
    print(f"Services: {len(services)}")
    for s in services:
        print(f"- {s.g6_ten_dich_vu}")
    print(f"Classes: {len(classes)}")
    for c in classes:
        print(f"- {c.g6_ten_lop}")
