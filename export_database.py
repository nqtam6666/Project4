import os
import pyodbc
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def export_database():
    driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server').replace('+', ' ')
    server = os.getenv('DB_SERVER', 'localhost')
    db_name = os.getenv('DB_NAME', 'nqtam_project4')
    trusted = os.getenv('DB_TRUSTED_CONNECTION', 'yes')
    
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={db_name};"
        f"Trusted_Connection={trusted};"
    )
    
    print(f"Connecting to SQL Server: {server} | Database: {db_name}...")
    try:
        conn = pyodbc.connect(conn_str)
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-16-le')
        conn.setencoding(encoding='utf-16-le')
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    # Fetch all user tables
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE' 
          AND TABLE_NAME NOT LIKE 'sys%'
          AND TABLE_NAME NOT LIKE 'MS%'
        ORDER BY TABLE_NAME
    """)
    tables = [row[0] for row in cursor.fetchall()]
    
    output_file = "nqt_database_data_dump.sql"
    print(f"Found {len(tables)} tables. Generating dump file: {output_file}...")
    
    with open(output_file, "w", encoding="utf-8-sig") as f:
        f.write("-- ============================================================\n")
        f.write("-- NQT GYM SYSTEM - COMPLETE DATABASE DATA EXPORT DUMP\n")
        f.write(f"-- Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Database: {db_name}\n")
        f.write("-- Hướng dẫn khôi phục:\n")
        f.write(f"--   1. Chạy các file schema trong thư mục database/ để tạo cấu trúc bảng.\n")
        f.write(f"--   2. Chạy file {output_file} này để khôi phục dữ liệu.\n")
        f.write("-- ============================================================\n\n")
        
        f.write(f"USE [{db_name}];\nGO\n\n")
        
        f.write("-- 1. Vô hiệu hóa tất cả foreign key constraints để tránh lỗi phụ thuộc\n")
        f.write("EXEC sp_MSforeachtable \"ALTER TABLE ? NOCHECK CONSTRAINT all\";\nGO\n\n")
        
        for table in tables:
            print(f"Dumping table: {table}...")
            f.write(f"-- ------------------------------------------------------------\n")
            f.write(f"-- Dữ liệu bảng: [{table}]\n")
            f.write(f"-- ------------------------------------------------------------\n")
            
            # Check if table has identity column
            cursor.execute(f"""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table}' 
                  AND COLUMNPROPERTY(object_id(TABLE_NAME), COLUMN_NAME, 'IsIdentity') = 1
            """)
            has_identity = cursor.fetchone() is not None
            
            # Get columns info
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table}'
                ORDER BY ORDINAL_POSITION
            """)
            cols_info = cursor.fetchall()
            columns = [c[0] for c in cols_info]
            types = {c[0]: c[1] for c in cols_info}
            
            if has_identity:
                f.write(f"SET IDENTITY_INSERT [{table}] ON;\nGO\n\n")
            
            col_list_str = ", ".join([f"[{c}]" for c in columns])
            cursor.execute(f"SELECT {col_list_str} FROM [{table}]")
            rows = cursor.fetchall()
            
            if rows:
                for row in rows:
                    vals = []
                    for col_name, val in zip(columns, row):
                        if val is None:
                            vals.append("NULL")
                        elif types[col_name] in ('int', 'bigint', 'smallint', 'tinyint', 'decimal', 'numeric', 'float', 'real', 'bit'):
                            if isinstance(val, bool):
                                vals.append("1" if val else "0")
                            else:
                                vals.append(str(val))
                        else:
                            # String/DateTime/Time - escape quotes and prefix with N
                            escaped = str(val).replace("'", "''")
                            vals.append(f"N'{escaped}'")
                    
                    vals_str = ", ".join(vals)
                    f.write(f"INSERT INTO [{table}] ({col_list_str}) VALUES ({vals_str});\n")
                
                f.write("GO\n\n")
            else:
                f.write(f"-- (Bảng [{table}] rỗng)\n\n")
                
            if has_identity:
                f.write(f"SET IDENTITY_INSERT [{table}] OFF;\nGO\n\n")
                
        f.write("-- 2. Kích hoạt lại toàn bộ foreign key constraints\n")
        f.write("EXEC sp_MSforeachtable \"ALTER TABLE ? WITH CHECK CHECK CONSTRAINT all\";\nGO\n")
        
    print("\n============================================================")
    print(f"Export Completed Successfully!")
    print(f"Dump File: {output_file}")
    print("============================================================")

if __name__ == "__main__":
    export_database()
