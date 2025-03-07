from dotenv import load_dotenv
from typing import Union
import re

from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent, AgentOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.exceptions import OutputParserException
from tools import get_unique_categories, get_related_subcategories
from langchain import hub
import streamlit as st
load_dotenv()

# google_api_key = st.secrets["GOOGLE_API_KEY"]
# langsmith_tracing = st.secrets["LANGSMITH_TRACING"]
# langsmith_endpoint = st.secrets["LANGSMITH_ENDPOINT"]
# langsmith_api_key = st.secrets["LANGSMITH_API_KEY"]
# langsmith_project = st.secrets["LANGSMITH_PROJECT"]

#react_prompt = PromptTemplate = hub.pull('hwchase17/react')
react_prompt = PromptTemplate(
    template='''
    Encuentra la subcategoría que mejor se ajuste al siguiente input lo mejor que puedas. Tienes acceso a las siguientes herramientas:
{tools}

Utiliza el siguiente formato:

Pregunta: la pregunta de entrada que debes responder
Pensamiento: siempre debes pensar en qué hacer
Acción: la acción a realizar, debe ser una de [{tool_names}]
Entrada de la Acción: la entrada para la acción
Observación: el resultado de la acción
... (este ciclo de Pensamiento/Acción/Entrada de la Acción/Observación puede repetirse N veces)
Pensamiento: ahora sé la respuesta final
Respuesta Final: la subcategoría elegida que esté más relacionada con el input.

¡Empieza!

Pregunta: {input}
Pensamiento: {agent_scratchpad}
'''
)




tools = [get_unique_categories, get_related_subcategories]

llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash-latest', temperature=0)
    
reac_agent_runnable = create_react_agent(llm, tools, react_prompt)

# Agent executor creation
agent_executor = AgentExecutor(
    agent=reac_agent_runnable,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True    
)
def run_agent(query):
    try:
        # Invocar el agente executor con una consulta
        response = agent_executor.invoke({"input": query})
        return response['output']
    except Exception as e:
        print(f"Error al ejecutar el agente: {e}")
        return None
