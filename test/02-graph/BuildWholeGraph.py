from typing import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

"""图的构建流程：
1、初始化一个StateGraph实例。
2、添加节点。
3、定义边，将所有的节点连接起来。
4、设置特殊节点，入口和出口（可选）。
5、编译图。
6、执行工作流。"""

class GraphState(TypedDict):
    process_data: dict

def input_node(state: GraphState) -> dict:
    """入口节点：写入初始 process_data。"""
    print(f"input_node 节点执行 state.get('process_data'): {state.get('process_data')}")
    return {"process_data": {"input": "input_value"}}

def process_node(state: dict) -> dict:
    """处理节点：更新 process_data。"""
    print(
        f"process_node 节点执行 state.get('process_data'): {state.get('process_data')}"
    )
    return {"process_data": {"process": "process_value9527"}}

def output_node(state: GraphState) -> dict:
    """出口节点：读取并返回当前 process_data。"""
    print(
        f"output_node 节点执行 state.get('process_data'): {state.get('process_data')}"
    )
    return {"process_data": state.get("process_data")}

graph = StateGraph(GraphState)
graph.add_node("input", input_node)
graph.add_node("process", process_node)
graph.add_node("output", output_node)

# 固定边：start → input → process → output → end
graph.add_edge(START, "input")
graph.add_edge("input", "process")
graph.add_edge("process", "output")
graph.add_edge("output", END)

app = graph.compile()
result = app.invoke({"process_data": {"name": "测试数据", "value": 123456}})
print(result)
print("="*20)
print(app.get_graph().print_ascii())
