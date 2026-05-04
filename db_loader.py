import pandas as pd
import sqlite3
import os
import re
import tempfile

# ✅ Global DB path using temp directory
DB_PATH = os.path.join(tempfile.gettempdir(), "database.db")

def load_csv_to_sqlite(csv_file, db_path=None):
    if db_path is None:
        db_path = DB_PATH

    df = pd.read_csv(csv_file)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    file_name = getattr(csv_file, "name", "uploaded_file")
    table_name = os.path.splitext(os.path.basename(file_name))[0]
    table_name = re.sub(r"[^a-zA-Z0-9_]", "_", table_name)
    table_name = table_name.strip("_").lower()

    if not table_name:
        table_name = "uploaded_file"

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

    return {
        "table_name": table_name,
        "columns": list(df.columns),
        "row_count": len(df),
        "db_path": db_path,
        "dataframe": df
    }


def get_table_info(db_path=None):
    if db_path is None:
        db_path = DB_PATH

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    info = {}
    for (table,) in tables:
        cursor.execute(f'PRAGMA table_info("{table}");')
        columns = cursor.fetchall()
        info[table] = [col[1] for col in columns]

    conn.close()
    return info