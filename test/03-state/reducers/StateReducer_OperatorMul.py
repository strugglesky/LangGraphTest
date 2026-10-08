import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class MultiplyState(TypedDict):
    factor: Annotated[float, operator.mul]


def multiplier(state: MultiplyState) -> dict:
    return {"factor": 2.0}

def run_demo():
    print("4. operator.mul Reducer（数值相乘）演示:")
    builder = StateGraph(MultiplyState)
    builder.add_node("multiplier", multiplier)
    builder.add_edge(START, "multiplier")
    builder.add_edge("multiplier", END)
    graph = builder.compile()

    print(graph.get_graph().print_ascii())

    result = graph.invoke({"factor": 5.0})
    print(f"初始状态: {{'factor': 5.0}}")
    print(f"执行结果: {result}")
    print(
        "说明: 因 float 默认 0.0 先参与规约，0.0 * 5.0 = 0.0，后续乘 2.0 仍为 0.0；乘法场景请用自定义 Reducer。\n"
    )


if __name__ == "__main__":
    run_demo()