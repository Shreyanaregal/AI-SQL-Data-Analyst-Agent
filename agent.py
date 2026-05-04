import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()

DB_PATH = os.path.join(tempfile.gettempdir(), "database.db")

def create_agent(db_path=None):
    if db_path is None:
        db_path = DB_PATH

    db_uri = f"sqlite:///{db_path}"
    db = SQLDatabase.from_uri(db_uri)

    api_key = None
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = os.getenv("GROQ_API_KEY")

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
