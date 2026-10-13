from operator import add
from typing import Annotated, TypedDict

from langgraph.constants import END
from langgraph.graph import StateGraph, START


class DiliState(TypedDict):
    """
    状态：messages 使用 operator.add 合并策略——新返回的列表与原有列表拼接（非覆盖）。
    """

    messages: list[str]

def sub_node(state: DiliState) -> DiliState:
    return {"messages": ["response from subgraph"]}

# --- 子图 ---
subgraph_node = (
    StateGraph(DiliState)
    .add_node("sub_node", sub_node)
    .add_edge(START, "sub_node")
    .add_edge("sub_node", END)
    .compile()
)
print('子图编译完成')
print(subgraph_node.get_graph().print_ascii())

graph = (
    StateGraph(DiliState)
    .add_node("subgraph_node", subgraph_node)
    .add_edge(START, "subgraph_node")
    .add_edge("subgraph_node", END)
    .compile()
)
print('父图编译完成')
print(graph.get_graph().print_ascii())

print(graph.invoke({"messages": ["main-graph"]}))
# 预期形态示例：{'messages': ['main-graph', 'main-graph', 'response from subgraph']}
