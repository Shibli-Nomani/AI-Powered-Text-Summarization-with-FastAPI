# services/graph.py
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated

#from agents.orchestrator_agent import orchestrator_agent, routing_logic
from agents.summary_agent import summary_agent

# Define the state structure for the graph
class State(TypedDict):
    messages: Annotated[list, "add_messages"]
    answer: str
    transcript: str
    question: str
    file_id: str   # ✅ Added so summary_agent can fetch logs

# Function to build and compile the workflow graph  
def build_graph():
    graph = StateGraph(State)
    graph.add_node("summary_agent", summary_agent)
    graph.add_edge(START, "summary_agent")
    graph.add_edge("summary_agent", END)
    return graph.compile()

    # Add nodes
    #graph.add_node("orchestrator_agent", orchestrator_agent)
   

    # Build edges
    #graph.add_edge(START, "orchestrator_agent")
    
#
    #graph.add_conditional_edges(
    #    "orchestrator_agent",
    #    routing_logic,
    #    {
    #        "summary_agent": "summary_agent",
    #        # "qna_agent": "qna_agent",  # can be re-enabled later
    #    }
    #)

    

    # Compile the graph
    
    
