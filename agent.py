import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()

def create_agent(db_path="data/database.db"):
    """
    Creates a LangChain SQL Agent connected to
    our SQLite database using Groq LLM.
    """

    # Connect LangChain to SQLite
    db_uri = f"sqlite:///{db_path}"
    db = SQLDatabase.from_uri(db_uri)

    # Initialize Groq LLM
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

    # Create SQL Agent (new style - no AgentType needed)
    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="openai-tools",
        verbose=True,
        handle_parsing_errors=True
    )

    return agent


def run_query(question, db_path="data/database.db"):
    """
    Takes a natural language question,
    runs it through the SQL agent,
    and returns the answer.
    """
    agent = create_agent(db_path)
    result = agent.invoke({"input": question})

    return {
        "question": question,
        "answer": result.get("output", "No answer found")
    }