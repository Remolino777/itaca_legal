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
#import streamlit as st
load_dotenv()
react_prompt = PromptTemplate(
    template='''
    Find the subcategory that better fits the following input as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the subcategory chosen that is most related to the input

Begin!

Question: {input}
Thought:{agent_scratchpad}
'''
)

#GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]


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
