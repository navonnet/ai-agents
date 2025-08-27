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
        use the appropriate tools to fetch real-time information from WildApricot.
        at start welcoming the user also tell what things you can help with.
        reply with well formated list if actions you can do no in a line.
        don't use word meeting instead use event
        """

    system_message = {"role": "system", "content": system_content}
    userMessage = {"role": "user", "content": msg}

    state = State(messages=[userMessage,system_message])
    assistant_reply = ""  # buffer for streaming text
    async for event in graph.graph.astream_events(state, config=graph.getConfig(), version="v1"):
        if event["event"] == "on_chat_model_stream":
            token = event["data"]["chunk"].content
            if token:
                assistant_reply += token
                # yield a full assistant message each step
                yield {"role": "assistant", "content": assistant_reply}

    #return result["messages"][-1].content
    # Stream output tokens instead of waiting for full response
    

app = gr.ChatInterface(userInput, type="messages")
port = int(os.environ.get("PORT", 7860))
app.launch(server_name="0.0.0.0", server_port=port)
#app.launch(server_name=os.getenv("SERVER"))