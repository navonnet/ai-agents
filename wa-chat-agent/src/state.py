from pydantic import BaseModel
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict

class State(BaseModel):
    messages: Annotated[list, add_messages]