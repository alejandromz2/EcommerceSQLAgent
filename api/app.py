import pandas as pd
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from sqlalchemy import create_engine
from flask import Flask, request, jsonify
import os
import requests
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
# Asegura que "src" esté en sys.path
import src.config as config
from src.connection_llm import iniciar_conexion_llm, preguntar_sql_en_espanol


# Iniciando Flask App
app = Flask(__name__)

# Función para enviar mensajes de Telegram
def enviar_mensaje_telegram(chat_id, text, TELEGRAM_API_URL):
    url = f'{TELEGRAM_API_URL}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response.json()

# Token del bot de Telegram
TELEGRAM_API_URL = f'https://api.telegram.org/bot{config.TELEGRAM_TOKEN}'


agent_executor_sql, agent_executor_translator = iniciar_conexion_llm()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        # Pasar la pregunta al LLM
        response = preguntar_sql_en_espanol(user_message, agent_executor_sql, agent_executor_translator)

        # Enviar la respuesta al usuario
        enviar_mensaje_telegram(chat_id, response, TELEGRAM_API_URL)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5600)