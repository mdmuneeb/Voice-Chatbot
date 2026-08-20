from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from backend.app.graph.state import ChatState

from backend.app.graph.nodes import (
    chat_node,
    piper_node,
    save_assistant_node
)


builder = StateGraph(
    ChatState
)


builder.add_node(
    "chat",
    chat_node
)


builder.add_node(
    "piper",
    piper_node
)

builder.add_node(
    "save_assistant",
    save_assistant_node
)


builder.add_edge(
    START,
    "chat"
)


builder.add_edge(
    "chat",
    "piper"
)


builder.add_edge(
    "piper",
    "save_assistant"
)

builder.add_edge(
    "save_assistant",
    END
)


graph = builder.compile()