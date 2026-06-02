import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import nqt_tao_app, db
from sqlalchemy import text

app = nqt_tao_app()
with app.app_context():
    try:
        # Check database engine dialect
        dialect_name = db.engine.dialect.name
        print(f"Database dialect: {dialect_name}")
        
        # SQL statement to alter table
        if dialect_name == 'mssql':
            sql = text("ALTER TABLE G6NguoiDung ADD g6_totp_secret NVARCHAR(32) NULL;")
        else:
            sql = text("ALTER TABLE G6NguoiDung ADD g6_totp_secret VARCHAR(32) NULL;")
            
        db.session.execute(sql)
        db.session.commit()
        print("Successfully added g6_totp_secret column to G6NguoiDung table!")
    except Exception as e:
        db.session.rollback()
        # If the column already exists, it is expected
        if "already" in str(e).lower() or "duplicate" in str(e).lower() or "42S21" in str(e) or "Column names in each table must be unique" in str(e):
            print("g6_totp_secret column already exists in G6NguoiDung table.")
        else:
            print(f"Error updating database: {e}")
