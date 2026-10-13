from typing import Annotated

import operator
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class PersistenceDemoState(TypedDict):
    # operator.add：列表/数值等按「相加」语义合并（列表相当于拼接）
    messages: Annotated[list, operator.add]
    step_count: Annotated[int, operator.add]

def step_one(state: PersistenceDemoState) -> dict:
    print("执行步骤 1")
    return {
        "messages": ["执行了步骤 1"],
        "step_count": 1,
    }

def step_two(state: PersistenceDemoState) -> dict:
    print("执行步骤 2")
    return {
        "messages": ["执行了步骤 2"],
        "step_count": 1,
    }


def step_three(state: PersistenceDemoState) -> dict:
    print("执行步骤 3")
    return {
        "messages": ["执行了步骤 3"],
        "step_count": 1,
    }

def create_graph():
    builder = StateGraph(PersistenceDemoState)

    builder.add_node("step_one", step_one)
    builder.add_node("step_two", step_two)
    builder.add_node("step_three", step_three)

    builder.add_edge(START, "step_one")
    builder.add_edge("step_one", "step_two")
    builder.add_edge("step_two", "step_three")
    builder.add_edge("step_three", END)

    return builder

def main():
    print("=== LangGraph 1.0 内存持久化存储演示 ===\n")

    graph = create_graph()
    app = graph.compile(checkpointer=InMemorySaver())

    config = {"configurable": {"thread_id": "user_13811112222"}}

    print("1. 首次执行工作流:")
    result = app.invoke(
        {
            "messages": ["开始执行"],
            "step_count": 0,
        },
        config,
    )
    print(result)

    state = app.get_state(config)
    print(type(state))
    print(state)

    history = app.get_state_history(config)
    for checkpoint in history:
        print("=" * 50)
        print(f"当前状态: {checkpoint.values}")

    print("=" * 80)
    print("3. 恢复执行工作流:")
    # 工作流若已结束，再次 invoke(None, config) 通常直接返回已落盘的结果
    result2 = app.invoke(None, config)
    print(f"恢复执行结果: {result2}\n")

    print("=== 演示结束 ===")


if __name__ == '__main__':
    main()