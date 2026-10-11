from functools import partial
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
from requests import RequestException, Timeout

class GraphState(TypedDict):
    process_data: dict


def input_node(state: GraphState) -> dict:
    print(f"input_node 收到的初始值:{state}")
    return {"process_data": {"input": "input_value"}}


# 节点可带额外参数，用 partial 绑定后传给 add_node
def process_node(state: dict, param1: int, param2: str) -> dict:
    print(state, param1, param2)
    print("process_with_params 的固定参数", param1,param2)
    return {"process_data": {"process": "process_value"}}

# 重试策略：仅对 RequestException、Timeout 重试，最多 3 次
retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=1,
    jitter=True,
    backoff_factor=2,
    retry_on=[RequestException, Timeout],
)

stateGraph = StateGraph(GraphState)
stateGraph.add_node("input", input_node)
process_with_params = partial(process_node, param1=100, param2="test")
stateGraph.add_node("process", process_with_params, retry_policy=retry_policy)
stateGraph.add_edge(START, "input")
stateGraph.add_edge("input", "process")
stateGraph.add_edge("process", END)

graph = stateGraph.compile()

print(stateGraph.edges)
print(stateGraph.nodes)
print(graph.get_graph().print_ascii())
print()

# ... existing code ...
initial_state = {"process_data": {"input": 23}}
result = graph.invoke(initial_state)
print(f"最后的结果是:{result}")