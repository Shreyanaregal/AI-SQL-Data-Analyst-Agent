import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()

DB_PATH = os.path.join(tempfile.gettempdir(), "database.db")

def create_agent(db_path):
    # Read from Streamlit secrets first, fallback to env var
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing! Add it to Streamlit secrets.")

    llm = ChatGroq(
        api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0
    
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="openai-tools",
        verbose=True,
        handle_parsing_errors=True
    )
    return agent

def run_query(question, db_path=None):
    if db_path is None:
        db_path = DB_PATH
    agent = create_agent(db_path)
    result = agent.invoke({"input": question})
    return {
        "question": question,
        "answer": result.get("output", "No answer found")
    }
