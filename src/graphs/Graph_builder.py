from langgraph.graph import StateGraph, END
from src.states.States import AssistantRequest
from src.nodes.assistant_node import AssistantNode

class GraphBuilder:
    def __init__(self, llm,memory):
        self.llm = llm
        self.memory = memory

    def build_QA_graph(self):
        graph = StateGraph(AssistantRequest)
        assistant_node_obj = AssistantNode(self.llm)

        # Create node with video context
        node = assistant_node_obj.assistant_node()

        graph.add_node("assistant_node", node)
        graph.set_entry_point("assistant_node")
        graph.add_edge("assistant_node", END)


        return graph.compile(checkpointer=self.memory)
