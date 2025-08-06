from langchain_core.messages import AIMessage
from langchain_core.messages import BaseMessage

class AssistantNode:
    def __init__(self,llm):
        self.llm=llm
        
    def trim_messages(self,messages: list[BaseMessage]) -> list[BaseMessage]:
        """
        Keeps the initial system message and the last N exchanges (Human + AI).
        """
        max_pairs = 5  # adjust this based on expected message length

        # Always keep the first message (usually SystemMessage)
        initial = messages[0:1]

        # Extract recent Human-AI message pairs
        recent = messages[-(max_pairs * 2):]  # each pair is 2 messages

        return initial + recent

        
    def assistant_node(self):
        def _node(state):
            trimmed = self.trim_messages(state["messages"])  # custom truncate

            response = self.llm.invoke(trimmed)
            return {
                "messages": [AIMessage(content=response.content)],
                "response": response.content
            }

        return _node

