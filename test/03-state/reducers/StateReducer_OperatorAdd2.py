import operator
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class StringConcatState(TypedDict):
    text: Annotated[List[str], operator.add]  # Changed from operator.add to operator.concat


def add_text_1(state: StringConcatState) -> dict:
    return {"text": ["Hello "]}


def add_text_2(state: StringConcatState) -> dict:
    return {"text": ["World!"]}

def run_demo():
    print("3.2 字符串连接 Reducer 演示:")
    builder = StateGraph(StringConcatState)
    builder.add_node("add_text_1", add_text_1)
    builder.add_node("add_text_2", add_text_2)
    builder.add_edge(START, "add_text_1")
    builder.add_edge(START, "add_text_2")
    builder.add_edge("add_text_1", END)
    builder.add_edge("add_text_2", END)
    graph = builder.compile()
    print(graph.get_graph().print_ascii())
    result = graph.invoke({"text": ["Say: "]})
    print(f"初始状态: {{'text': ['Say: ']}}")
    print(f"执行结果: {result}\n")

if __name__ == '__main__':
    run_demo()