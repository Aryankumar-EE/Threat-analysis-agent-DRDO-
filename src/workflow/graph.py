from langgraph.graph import StateGraph

from workflow.state import ThreatState

from workflow.nodes import (
    extraction_node,
    recommendation_node,
    retrieval_node,
    verification_node,
    threat_node,
    report_node
)
builder = StateGraph(ThreatState)

builder.add_node("extract", extraction_node)
builder.add_node("retrieve", retrieval_node)
builder.add_node("verify", verification_node)
builder.add_node("threat", threat_node)
builder.add_node("recommend",recommendation_node)
builder.add_node("report", report_node)

builder.set_entry_point("extract")

builder.add_edge("extract", "retrieve")
builder.add_edge("retrieve", "verify")
builder.add_edge("verify", "threat")
builder.add_edge("threat","recommend")
builder.add_edge("recommend","report")


graph = builder.compile()