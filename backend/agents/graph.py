from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes import planner_node, programmer_node, tester_node, reviewer_node

def should_continue(state: AgentState):
    if state.get("error_info"):
        return END
    if state.get("needs_clarification"):
        return "clarification_pause"
    return "continue"

def build_orchestrator_graph(checkpointer=None):
    workflow = StateGraph(AgentState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("programmer", programmer_node)
    workflow.add_node("tester", tester_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.set_entry_point("planner")
    workflow.add_conditional_edges(
        "planner", should_continue,
        {"clarification_pause": END, "continue": "programmer", END: END}
    )
    workflow.add_edge("programmer", "tester")
    workflow.add_edge("tester", "reviewer")
    workflow.add_edge("reviewer", END)
    return workflow.compile(checkpointer=checkpointer)
