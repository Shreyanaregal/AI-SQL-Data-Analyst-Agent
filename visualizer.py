import pandas as pd
import plotly.express as px
import sqlite3
import os
import tempfile

DB_PATH = os.path.join(tempfile.gettempdir(), "database.db")

def fetch_data(query, db_path=None):
    if db_path is None:
        db_path = DB_PATH
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def generate_chart(df, chart_type="bar", x_col=None, y_col=None, title="Chart"):
    if df is None or df.empty:
        return None
    if x_col is None:
        x_col = df.columns[0]
    if y_col is None:
        numeric_cols = df.select_dtypes(include="number").columns
        y_col = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[1]
    if chart_type == "bar":
        fig = px.bar(df, x=x_col, y=y_col, title=title, color=x_col)
    elif chart_type == "line":
        fig = px.line(df, x=x_col, y=y_col, title=title, markers=True)
    elif chart_type == "pie":
        fig = px.pie(df, names=x_col, values=y_col, title=title)
    elif chart_type == "scatter":
        fig = px.scatter(df, x=x_col, y=y_col, title=title)
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    return fig

def auto_visualize(df, title="Query Results"):
    if df is None or df.empty:
        return None
    if len(df.columns) < 2:
        return None
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()
    try:
        if len(text_cols) >= 1 and len(numeric_cols) >= 1:
            return generate_chart(df, "bar", text_cols[0], numeric_cols[0], title)
        elif len(numeric_cols) >= 2:
            return generate_chart(df, "scatter", numeric_cols[0], numeric_cols[1], title)
        else:
            return generate_chart(df, "bar", df.columns[0], df.columns[1], title)
    except Exception:
        return None
