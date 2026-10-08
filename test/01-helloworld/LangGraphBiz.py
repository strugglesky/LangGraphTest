from langgraph.constants import START,END
from langgraph.graph import StateGraph

def addition(state) -> dict:
    """加法节点：将 state 中的 x 加 1。"""
    print(f"加法节点收到的初始值:{state}")
    return {"x": state["x"] + 1}

def subtraction(state) -> dict:
    """减法节点：将 state 中的 x 减 5。"""
    print(f"减法节点收到的初始值:{state}")
    return {"x": state["x"] - 5}


graph = StateGraph(dict)
graph.add_node("add",addition)
graph.add_node("subtract",subtraction)
graph.add_edge(START,"add")
graph.add_edge("add","subtract")
graph.add_edge("subtract",END)

app = graph.compile()
result = app.invoke({"x": 10})
print(result)
print(result["x"])
