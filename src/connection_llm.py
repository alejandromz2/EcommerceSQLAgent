import os
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from sqlalchemy import create_engine
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
# Asegura que "src" esté en sys.path
import src.config as config

def iniciar_conexion_llm():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_CREDENTIALS

    # Creating Agent
    llm = OpenAI(temperature=0, verbose=True, openai_api_key=config.OPENAI_API_KEY)

    # Crear la URI de conexión
    BIGQUERY_URI = f"bigquery://{config.PROJECT_ID}/{config.DATASET_ID}"

    # Crear el motor SQLAlchemy para BigQuery
    engine = create_engine(BIGQUERY_URI)

    # Conectar la base de datos a LangChain
    db = SQLDatabase(engine)

    agent_executor_sql = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    # Crear el prompt para mejorar la respuesta en español
    template = """
    Eres un asistente virtual especializado en eCommerce, diseñado para ayudar a los clientes de manera clara, amigable y útil.

    Tu tarea es transformar la siguiente información técnica obtenida de una consulta SQL en una respuesta atractiva y comprensible para el usuario final. Asegúrate de:

    1️⃣ **Hacer la respuesta fácil de entender** (evita términos técnicos innecesarios).
    2️⃣ **Ser conversacional y cercano** (habla como un asistente amigable, no como un robot).
    3️⃣ **Organizar la información** en una estructura clara (listas, párrafos cortos, etc.).
    4️⃣ **Ofrecer contexto adicional** si es necesario (ejemplo: si el usuario pregunta por un producto, menciona beneficios clave).
    5️⃣ **Finalizar con una llamada a la acción** si aplica (ejemplo: "¿Te gustaría que te ayude a encontrar más productos similares? 😊").

    ### 🔹 **Ejemplo de Transformación**
    ❌ **Entrada SQL sin formato:**
    "El producto más vendido es el 'Smartphone X'. Se han vendido 10,000 unidades en los últimos 30 días."

    ✅ **Salida esperada (más clara y amigable):**
    📢 **¡El Smartphone X es un éxito de ventas!** 🚀  
    En los últimos 30 días, **10,000 personas** lo han comprado, lo que lo convierte en uno de los productos más populares de nuestra tienda.  
    👉 **¿Quieres conocer más sobre sus características o encontrar accesorios compatibles?** 😊

    ---

    ### 🔹 **Aquí está la respuesta del agente SQL, si es un enunciado en ingles lo tienes que traducir y sino responde a la pregunta usando el valor recibido como respuesta**
    {respuesta_sql}

    🔄 **Devuelve la versión mejorada aquí:**
    """

    prompt = PromptTemplate(template=template, input_variables=["respuesta_sql"])

    # 2️⃣ Crear la cadena de traducción y reformateo
    agent_executor_translator = LLMChain(llm=llm, prompt=prompt, verbose=True)

    return agent_executor_sql, agent_executor_translator


# 3️⃣ Función para ejecutar los agentes en secuencia
def preguntar_sql_en_espanol(pregunta, agent_executor_sql, agent_executor_translator):
    print(f"\n🔹 Pregunta original: {pregunta}")

    # 1. Ejecutar consulta SQL con el primer agente
    respuesta_sql = agent_executor_sql.run(pregunta)
    print(f"\n✅ Respuesta SQL: {respuesta_sql}")

    # 2. Traducir y reformatear con el segundo agente
    respuesta_final = agent_executor_translator.run(respuesta_sql)

    return respuesta_final