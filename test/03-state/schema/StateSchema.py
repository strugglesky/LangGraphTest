from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


# 仅包含「输入」字段的 Schema：限制调用方进图时能传什么
class InputState(TypedDict):
    question: str


# 仅包含「输出」字段的 Schema：限制图最终对外返回什么
class OutputState(TypedDict):
    answer: str


# 图内部使用的完整 State Schema（输入 + 输出）
class OverallState(InputState, OutputState):
    pass

def answer_node(state: InputState):
    """处理节点：根据 question 生成 answer。"""
    print(f"执行 answer_node 节点:")
    print(f"  输入: {state}")
    answer = "再见" if "bye" in state["question"].lower() else "你好"
    result = {"answer": answer, "question": state["question"]}
    print(f"  输出: {result}")
    return result

def demo_input_output_schema():
    """演示：调用时只传 question，返回时只得到 answer。"""
    print("=== 演示输入输出模式 ===")

    # 指定 input_schema / output_schema，约束图的对外接口
    builder = StateGraph(
        OverallState, input_schema=InputState, output_schema=OutputState
    )
    builder.add_edge(START, "answer_node")
    builder.add_node("answer_node", answer_node)
    builder.add_edge("answer_node", END)
    graph = builder.compile()

    # invoke 只传 InputState 的字段；返回结果仅包含 OutputState 的字段
    result = graph.invoke({"question": "你好 Bye"})
    print(f"图调用结果: {result}")
    print(graph.get_graph().print_ascii())
    print()

def main():
    print("=== LangGraph 图输入输出模式===\n")
    demo_input_output_schema()
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()