from typing import Annotated, TypedDict

from langchain_core import messages
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langgraph.graph.state import Checkpoint
from pydantic import BaseModel
from langchain_core.tools import Tool
from wa_api import waAPiClient
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools import StructuredTool
import uuid
from inputModels import CreateContactInput, RegisterForEventInput

load_dotenv(override=True)

# define state
class State(BaseModel):
    messages: Annotated[list, add_messages]


#define graph builder 
graph_builder = StateGraph(State)
client = waAPiClient()

listContacts = Tool(
        name="list_contacts",
        func=client.listContacts,
        description="Call this tool to fetch list available contacts in wildapricot."
)

findContactViaEmail = Tool(
        name="findContactViaEmail",
        func=client.findContactViaEmail,
        description="Call this tool to find a contact by email. To check of a contact exist with an email."
)


listEvent = Tool(
        name="list_events",
        func=client.listEvents,
        description="Call this tool to fetch list available events in wildapricot. Only fetch active events."
)

createContact = StructuredTool(
        name="create_contact",
        func=client.create_contact,
        description="""
            Call this tool to add a new contact.

            Required args:
            - email: the person's email
            - first_name: ONLY the given name (e.g. 'John' from 'John Wick')
            - last_name: ONLY the family name (e.g. 'Wick' from 'John Wick')

            If the user provides a full name (e.g. 'Terry Halson'), you MUST split it
            into first_name='Terry' and last_name='Halson' before calling this tool.
            Do not pass the full name as first_name.
            """,
        args_schema=CreateContactInput)
 
getEventRegistrations = Tool(
        name="get_event_registrations",
        func=client.get_event_registrations,
        description="""Call this tool to get current registrations for an event, 
                        fetch event detail from list_events, ask user the name of the event."""
)

registerForEvent = StructuredTool(
        name="register_for_event",
        func=client.register_for_event,
        description="""Call this tool to register a contact for an event. User must provide details about the active event 
                        and if contact is missing add a new contact first and then create a new registration.
                        If email provided then search contact by tool 'findContactViaEmail' and the extract the id as contactId
                        if regType is not provided then you must ask the user for that, don't pass the default value""",
        args_schema=RegisterForEventInput
)

tools = [listEvent, createContact, getEventRegistrations, registerForEvent, listContacts, findContactViaEmail]

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

#define node
def chatBot(state: State) -> State:
    return {"messages": [llm_with_tools.invoke(state.messages)]}

#add node
graph_builder.add_node("chatBot", chatBot)
graph_builder.add_node("tool", ToolNode(tools=tools))

#define edges
graph_builder.add_edge(START, "chatBot")
graph_builder.add_conditional_edges("chatBot", tools_condition, {
    "tools": "tool",
    "__end__": END
})
graph_builder.add_edge("tool", "chatBot")

memory = MemorySaver()
#compine graph
graph = graph_builder.compile(checkpointer=memory)

def make_thread_id() -> str:
    return str(uuid.uuid4())

config = {"configurable": {"thread_id": make_thread_id()}, "recursion_limit": 10}

async def userInnput(msg: str, history):
    messages = [{"role": "user", "content": msg}];
    state = State(messages=messages)
    result = await graph.ainvoke(state, config=config)
    print(result)
    return result["messages"][-1].content

gr.ChatInterface(userInnput, type="messages").launch()