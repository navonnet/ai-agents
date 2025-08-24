from dotenv import load_dotenv
import gradio as gr
from state import State
from graph import GraphBuilder
from langgraph.checkpoint.memory import MemorySaver
import os
load_dotenv(override=True)

memory = MemorySaver()
graph = GraphBuilder()
graph.build(memory)
      
async def userInput(msg: str, history):
    system_content = """You are a WildApricot meeting manager assistant. Your responsibilities include:
        - Managing events and registrations
        - Creating and updating contacts
        - Handling event registration requests
        - Providing information about available events
        - Assisting with contact searches
        - Deletion is not allowed, for that user has to contact Administrator
        Always be professional, clear, and helpful. When users ask about events or contacts, 
        use the appropriate tools to fetch real-time information from WildApricot."""

    system_message = {"role": "system", "content": system_content}
    userMessage = {"role": "user", "content": msg}

    state = State(messages=[userMessage,system_message])
    result = await graph.invoke(state)
    return result["messages"][-1].content

app = gr.ChatInterface(userInput, type="messages")

app.launch(server_name=os.getenv("SERVER"))