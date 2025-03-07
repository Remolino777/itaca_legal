from dotenv import load_dotenv
load_dotenv()

from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.schema.runnable import RunnableConfig
from nodes import execute_tools, run_agent_reasonig_engine
from state import AgentState
from react import run_agent
import streamlit as st

import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())






AGENT_REASON = 'agent_reason'
ACT = 'act'

def should_continue(state: AgentState) -> str:
    if isinstance(state['agent_outcome'], AgentFinish):
        return END
    else:
        return ACT

###### Langgraph ######    
flow = StateGraph(AgentState)
flow.add_node(AGENT_REASON, run_agent_reasonig_engine)
flow.add_node(ACT, execute_tools) 
flow.set_entry_point(AGENT_REASON)
flow.add_conditional_edges(AGENT_REASON, should_continue)
flow.add_edge(ACT, AGENT_REASON)
app = flow.compile() 

## Streamlit configuración  ###################
def set_background_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #336ca4;
            color: white; /* Color por defecto del texto en la app */
        }
        .chat-response {
            color: white; /* Color blanco para las respuestas del chatbot */
        }
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #d3d3d3; /* Fondo gris para el botón */
            color: grey; /* Texto del botón en gris */
            border: none; /* Opcional: elimina bordes por defecto */
            padding: 5px 15px; /* Ajusta el padding del botón */
            border-radius: 5px; /* Bordes redondeados */
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #b0b0b0; /* Gris más oscuro al pasar el mouse */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
set_background_color()

# Título y logo
st.image(r"https://github.com/user-attachments/assets/c026e391-fa23-4457-b575-5bd933ad6e36", width=300)

# Formulario para la entrada del usuario
with st.form(key="question_form"):
    user_input = st.text_input("Ingresa tu pregunta")
    submit_button = st.form_submit_button(label="Enviar Pregunta")  # No necesita 'color' aquí

# 🔄 Quitar almacenamiento de mensajes en el estado de la sesión
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# Mostrar solo el mensaje actual (sin historial)
if submit_button and user_input:
    # Mostrar la pregunta del usuario (sin guardarla)
    with st.chat_message("user"):
        st.write(user_input)

    # Configurar el contenedor de respuesta y el callback
    with st.chat_message("assistant", avatar="🤖"):        
        st_callback = StreamlitCallbackHandler(st.container())
        cfg = RunnableConfig(callbacks=[st_callback])

        try:
            # Invocar el agente con un estado limpio
            with st.spinner("Procesando tu pregunta..."):
                res = app.invoke(input={'input': user_input}, config=cfg)
                answer = res['agent_outcome'].return_values['output']
            # Mostrar solo la respuesta actual (sin guardarla)
            st.markdown(f'<p class="chat-response">{answer}</p>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Ocurrió un error: {str(e)}")
