import time
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy

class State(TypedDict):
    x: int
    result: int

def expensive_node(state: State) -> dict[str, int]:
    """模拟耗时计算（sleep 3 秒），用于观察缓存命中时不再执行。"""
    time.sleep(3)
    return {"result": state["x"] * 2}

builder = StateGraph(State)
builder.add_node("expensive_node", expensive_node, cache_policy=CachePolicy(ttl=8))
builder.set_entry_point("expensive_node")
builder.set_finish_point("expensive_node")

graph = builder.compile(cache=InMemoryCache())
print(graph.get_graph().print_ascii())

# 第一次执行：无缓存，耗时约 3 秒
print("第一次执行（无缓存，耗时 3 秒）：")
print(graph.invoke({"x": 5}))

# 第二次执行：命中缓存，立即返回
print("\n第二次运行利用缓存并快速返回：")
print(graph.invoke({"x": 5}))

# 等待 ttl 过期后再次执行，将重新计算
print("\n等待 8 秒，缓存过期...")
time.sleep(8)
print("8 秒后第三次执行（重新计算，耗时 3 秒）：")
print(graph.invoke({"x": 5}))

