import operator
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class ListAddState(TypedDict):
    data: Annotated[List[int], operator.add]

def producer_1(state: ListAddState) -> dict:
    return {"data": [1, 2]}


def producer_2(state: ListAddState) -> dict:
    return {"data": [3, 4]}

def run_demo():
    print("3.1 列表追加 Reducer 演示:")
    builder = StateGraph(ListAddState)
    builder.add_node("producer1", producer_1)
    builder.add_node("producer2", producer_2)
    builder.add_edge(START, "producer1")
    builder.add_edge("producer1", "producer2")
    builder.add_edge("producer2", END)
    graph = builder.compile()
    print(graph.get_graph().print_ascii())
    result = graph.invoke({"data": [0]})
    print(f"初始状态: {{'data': [0]}}")
    print(f"执行结果: {result}\n")

if __name__ == '__main__':
    run_demo()