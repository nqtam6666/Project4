from backend.app import db, nqt_tao_app
from sqlalchemy import text

app = nqt_tao_app()
with app.app_context():
    try:
        # Drop the problematic constraint
        # The name is from your error message
        db.session.execute(text("ALTER TABLE G6NguoiDung DROP CONSTRAINT UQ__G6NguoiD__E570C8131408FECC"))
        
        # Create the filtered unique index (SQL Server only syntax)
        db.session.execute(text("CREATE UNIQUE INDEX ix_g6_nguoi_dung_ten_dang_nhap ON G6NguoiDung(g6_ten_dang_nhap) WHERE g6_ten_dang_nhap IS NOT NULL"))
        
        db.session.commit()
        print("Successfully fixed G6NguoiDung unique constraint!")
    except Exception as e:
        print(f"Error fixing constraint: {e}")
        db.session.rollback()
