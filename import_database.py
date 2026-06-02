import os
import re
import pyodbc
import sys
from dotenv import load_dotenv

load_dotenv()

# Reconfigure stdout to use UTF-8 to prevent console printing UnicodeEncodeErrors on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def import_database():
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
    
    # Check command line args
    clear_data = True
    if "--no-clear" in sys.argv:
        clear_data = False
        
    dump_file = "nqt_database_data_dump.sql"
    if not os.path.exists(dump_file):
        print(f"Error: Dump file '{dump_file}' not found in current directory!")
        return

    print(f"Connecting to SQL Server: {server} | Database: {db_name}...")
    try:
        conn = pyodbc.connect(conn_str)
        conn.autocommit = True  # Enable autocommit to run separate SQL statements smoothly
        cursor = conn.cursor()
        
        # Set SQL Server session options to prevent errors with indexed views / computed columns / dates
        cursor.execute("SET QUOTED_IDENTIFIER ON")
        cursor.execute("SET ANSI_NULLS ON")
        cursor.execute("SET ANSI_WARNINGS ON")
        cursor.execute("SET DATEFORMAT ymd")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    if clear_data:
        print("\nClearing all existing data in database tables...")
        try:
            # Set QUOTED_IDENTIFIER ON inside the dynamic SQL scope of sp_MSforeachtable to avoid computed column index failures
            cursor.execute("EXEC sp_MSforeachtable 'SET QUOTED_IDENTIFIER ON; ALTER TABLE ? NOCHECK CONSTRAINT all'")
            cursor.execute("EXEC sp_MSforeachtable 'SET QUOTED_IDENTIFIER ON; DELETE FROM ?'")
            print("Existing data cleared successfully.")
        except Exception as e:
            print(f"Warning/Error during database clearing: {e}")
            print("Proceeding with import anyway...")

    print(f"\nReading dump file: {dump_file}...")
    try:
        with open(dump_file, "r", encoding="utf-8-sig") as f:
            sql_content = f.read()
    except Exception as e:
        print(f"Error reading dump file: {e}")
        return

    # Clean microsecond timestamps (6 digits) to millisecond precision (3 digits)
    # This prevents the 'Conversion failed when converting date and/or time from character string' error in SQL Server
    print("Normalizing date/time timestamps in the SQL dump...")
    sql_content = re.sub(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.(\d{6})",
        lambda m: f"{m.group(1)}.{m.group(2)[:3]}",
        sql_content
    )

    # Split script into batches using 'GO' separator on new line
    batches = re.split(r'(?i)(?m)^\s*GO\s*$', sql_content)
    total_batches = len(batches)
    print(f"Parsed {total_batches} query batches from dump file.")

    executed_count = 0
    error_count = 0

    print("\nStarting execution of SQL batches...")
    for i, batch in enumerate(batches):
        clean_batch = batch.strip()
        if not clean_batch:
            continue
            
        # Print progress summary
        if (i + 1) % 10 == 0 or i == 0 or i == total_batches - 1:
            print(f"  -> Executing batch {i + 1}/{total_batches}...")

        try:
            cursor.execute(clean_batch)
            executed_count += 1
        except Exception as e:
            error_count += 1
            print(f"\n[Error in batch {i + 1}]: {e}")
            
            # Safe print preview with fallback to ascii if needed
            preview = clean_batch[:150].replace('\n', ' ')
            try:
                print(f"Batch preview: {preview}...\n")
            except Exception:
                # If printing raw characters fails due to standard output limitation on Windows console
                safe_preview = preview.encode('ascii', errors='replace').decode('ascii')
                print(f"Batch preview (safe encoding): {safe_preview}...\n")

    print("\n============================================================")
    print("Import Completed Summary:")
    print(f"  - Total batches processed: {executed_count + error_count}")
    print(f"  - Successfully executed: {executed_count}")
    print(f"  - Errors encountered: {error_count}")
    print("============================================================")

    # Re-enable constraints
    try:
        cursor.execute("EXEC sp_MSforeachtable 'SET QUOTED_IDENTIFIER ON; ALTER TABLE ? WITH CHECK CHECK CONSTRAINT all'")
        print("Foreign key constraints re-enabled successfully.")
    except Exception as e:
        print(f"Error re-enabling constraints: {e}")

if __name__ == "__main__":
    import_database()
