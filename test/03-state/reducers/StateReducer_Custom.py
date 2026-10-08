from typing import Annotated

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

def MyOperatorMul(current: float, update: float) -> float:
    """自定义乘法 Reducer：首次合并时把 current 的边界情况单独处理，再继续乘法累计。"""
    # 第一次调用时 current 往往是类型默认值 0.0，若直接 current * update 会得到 0，后续无法恢复
    if current == 0.0:
        print(f"current:{current}")
        print(f"update:{update}")
        # 等价于从 1.0 开始乘：1.0 * update
        return 1.0 * update
    return current * update

class MultiplyState(TypedDict):
    factor: Annotated[float, MyOperatorMul]


def multiplier(state: MultiplyState) -> dict:
    # 节点返回的 update 会与 state["factor"] 经 MyOperatorMul 合并
    return {"factor": 2.0}


def run_demo():
    print("使用自定义reducer解决乘法问题:")
    builder = StateGraph(MultiplyState)
    builder.add_node("multiplier", multiplier)
    builder.add_edge(START, "multiplier")
    builder.add_edge("multiplier", END)
    graph = builder.compile()

    print(graph.get_graph().print_ascii())

    # 初始 factor=5.0 与节点返回 2.0 经 Reducer 合并为 5.0 * 2.0 = 10.0
    result = graph.invoke({"factor": 5.0})
    print(f"初始状态: {{'factor': 5.0}}")
    print(f"执行结果: {result}")
    print(f"解释: 5.0 * 2.0 = 10.0\n")


if __name__ == "__main__":
    run_demo()