from backend.app import nqt_tao_app, db
from backend.app.seeds.nqt_seed import nqt_chay_seed

app = nqt_tao_app()
with app.app_context():
    nqt_chay_seed()
    print("Seed completed successfully!")
