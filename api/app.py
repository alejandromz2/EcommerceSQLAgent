import pandas as pd
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from sqlalchemy import create_engine
from flask import Flask, request, jsonify
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
# Asegura que "src" esté en sys.path
import src.config as config
from src.connection_llm import iniciar_conexion_llm, preguntar_sql_en_espanol

app = Flask(__name__)

agent_executor_sql, agent_executor_translator = iniciar_conexion_llm()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    response = preguntar_sql_en_espanol(data["question"], agent_executor_sql, agent_executor_translator)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5600)