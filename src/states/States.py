from langgraph.graph import MessagesState

class AssistantRequest(MessagesState):
    response: str  
