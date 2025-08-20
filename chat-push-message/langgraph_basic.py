from typing import Annotated

from langchain_core import messages
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import random

load_dotenv(override=True)
nouns = ["Cabbages", "Unicorns", "Toasters", "Penguins", "Bananas", "Zombies", "Rainbows", "Eels", "Pickles", "Muffins"]
adjectives = ["outrageous", "smelly", "pedantic", "existential", "moody", "sparkly", "untrustworthy", "sarcastic", "squishy", "haunted"]

# define state
class State(BaseModel):
    messages: Annotated[list, add_messages]

#define graph builder 
graph_builder = StateGraph(State)

#define node
def firstNode(old_state: State) -> State:
    reply = f"{random.choice(nouns)} are {random.choice(adjectives)}"
    messages = [{"role": "assistant", "content": reply}]
    new_state = State(messages=messages)

    return new_state

#add node
graph_builder.add_node("fn",firstNode)

#define edges
graph_builder.add_edge(START, "fn")
graph_builder.add_edge("fn", END)

#compine graph
graph = graph_builder.compile()

def userInnput(msg: str, history):
    messages = [{"role": "user", "content": msg}];
    state = State(messages=messages)
    result = graph.invoke(state)
    print(result)
    return result["messages"][-1].content

gr.ChatInterface(userInnput, type="messages").launch()