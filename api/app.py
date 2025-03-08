import pandas as pd
import sys
from pathlib import Path
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from sqlalchemy import create_engine
import os
sys.path.append(os.path.abspath("."))
from src import config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_CREDENTIALS

# Creating Agent
llm = OpenAI(temperature=0, verbose=True, openai_api_key=config.OPENAI_API_KEY)

# Crear la URI de conexión
BIGQUERY_URI = f"bigquery://{config.PROJECT_ID}/{config.DATASET_ID}"

# Crear el motor SQLAlchemy para BigQuery
engine = create_engine(BIGQUERY_URI)
