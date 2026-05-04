import streamlit as st
import sqlite3
import pandas as pd
from db_loader import load_csv_to_sqlite, get_table_info, DB_PATH
from agent import run_query
from visualizer import auto_visualize, fetch_data

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="AI SQL Data Analyst",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI SQL Data Analyst Agent")
st.markdown("Upload a CSV → Ask questions in plain English → Get answers + charts!")

# ─── Session State ─────────────────────────────────────────
if "db_ready" not in st.session_state:
    st.session_state.db_ready = False
if "table_info" not in st.session_state:
    st.session_state.table_info = {}
if "df_preview" not in st.session_state:
    st.session_state.df_preview = None
if "db_path" not in st.session_state:
    st.session_state.db_path = DB_PATH

# ─── Sidebar: CSV Upload ────────────────────────────────────
with st.sidebar:
    st.header("📁 Upload Your CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        with st.spinner("Loading CSV into database..."):
            result = load_csv_to_sqlite(uploaded_file)
            st.session_state.db_ready = True
            st.session_state.db_path = result["db_path"]
            st.session_state.table_info = get_table_info(result["db_path"])
            st.session_state.df_preview = result["dataframe"]

        st.success(f"✅ Table **{result['table_name']}** loaded!")
        st.info(f"📊 {result['row_count']} rows | {len(result['columns'])} columns")

        st.subheader("📋 Columns:")
        for col in result["columns"]:
            st.write(f"• {col}")

# ─── Main Area ──────────────────────────────────────────────
if st.session_state.db_ready:

    # Data Preview
    with st.expander("👀 Preview Data", expanded=False):
        st.dataframe(st.session_state.df_preview, use_container_width=True)

    st.divider()

    # Question Input
    st.subheader("💬 Ask a Question")
    question = st.text_input(
        "Type your question in plain English:",
        placeholder="e.g. What is the average age? Who is the oldest person?"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        ask_btn = st.button("🔍 Ask Agent", use_container_width=True)

    if ask_btn and question:
        with st.spinner("🤖 Agent is thinking..."):
            result = run_query(question, db_path=st.session_state.db_path)

        st.divider()

        # Answer
        st.subheader("✅ Answer")
        st.success(result["answer"])

        # Auto Chart
        st.subheader("📊 Auto Visualization")
        try:
            table_name = list(st.session_state.table_info.keys())[0]
            df = fetch_data(f"SELECT * FROM {table_name}", db_path=st.session_state.db_path)
            fig = auto_visualize(df, title=f"Data Overview: {question}")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Could not generate chart for this query.")
        except Exception as e:
            st.warning(f"Could not generate chart: {e}")

    elif ask_btn and not question:
        st.warning("⚠️ Please type a question first!")

else:
    # Empty state
    st.info("👈 Please upload a CSV file from the sidebar to get started!")
    st.markdown("""
    ### 🚀 How it works:
    1. **Upload** any CSV file
    2. **Ask** a question in plain English
    3. The AI agent **generates SQL**, runs it, and returns the **answer**
    4. A **chart** is auto-generated from your data
    """)