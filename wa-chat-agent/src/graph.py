from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_openai import ChatOpenAI
from wa_tools  import wa_tools
from state import State
import uuid

class GraphBuilder():

    def __init__(self) -> None:
        self.tools = wa_tools().getAll()
        self.graph_builder = StateGraph(State)
        self.llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(self.tools)
        self.defineNodes()
        self.defineEdges()

    def defineNodes(self):
        self.graph_builder.add_node("chat", self.chat)
        self.graph_builder.add_node("tool", ToolNode(tools=self.tools))

    def defineEdges(self):
        self.graph_builder.add_edge(START, "chat")
        self.graph_builder.add_conditional_edges("chat", tools_condition, {
            "tools": "tool",
            "__end__": END
        })
        self.graph_builder.add_edge("tool", "chat")

    def chat(selft, state: State) -> State:
        return {"messages": [selft.llm.invoke(state.messages)]}
    
    def build(self, memory):
        self.thread_id = self.make_thread_id()
        self.graph =  self.graph_builder.compile(checkpointer=memory)

    async def invoke(self, state: State):
        return await self.graph.ainvoke(state, config=self.getConfig())
    
    async def streaResponse(self, state: State):
        #return await self.graph.ainvoke(state, config=self.getConfig())
        return await self.graph.astream_events(state, config=self.getConfig(), version="v1")

    def make_thread_id(self) -> str:
        return str(uuid.uuid4())
    
    def getConfig(self):
        return  {"configurable": {"thread_id": self.thread_id}, "recursion_limit": 10}

 