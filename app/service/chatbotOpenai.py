from typing import Annotated
import os
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)
llm = ChatOpenAI(model="gpt-4")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compila el gráfico sin checkpointer para evitar guardar en memoria
graph = graph_builder.compile()

config = {"configurable": {"thread_id": "1"}}

def get_chatbot_response(description: str) -> str:
    prompt = "Give me a recommendation if my BMI is "+description+",the text no is too long it's just like 100 characters"
    response_text = ""
    for event in graph.stream({"messages": [("user", prompt)]}, config, stream_mode="values"):
        # Captura el último mensaje en la lista de mensajes del evento
        response_text = event["messages"][-1].content
    return response_text
