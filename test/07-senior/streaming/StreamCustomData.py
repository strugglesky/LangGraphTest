from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    query: str
    answer: str
    progress: list


def node_with_custom_streaming(state: State) -> State:
    """带自定义流式传输的节点：边写自定义流边更新状态。"""
    writer = get_stream_writer()

    writer({"custom_key": "开始处理查询"})
    writer({"progress": "步骤1: 分析查询内容", "status": "running"})

    query = state["query"]

    writer({"progress": "步骤2: 生成结果", "status": "running"})
    writer({"progress": "步骤3: 完成处理", "status": "completed"})
    writer({"custom_key": "查询处理完成"})

    result = f"处理结果: {query.upper()}"
    return {
        "answer": result,
        "progress": state.get("progress", []) + ["处理完成"],
    }

def main():
    print("=== LangGraph 自定义数据流式传输演示 ===\n")

    graph = (
        StateGraph(State)
        .add_node("node_with_custom_streaming", node_with_custom_streaming)
        .add_edge(START, "node_with_custom_streaming")
        .add_edge("node_with_custom_streaming", END)
        .compile()
    )

    inputs = {"query": "hello world", "answer": "", "progress": []}

    for chunk in graph.stream(inputs, stream_mode="custom"):
        print(chunk, end="")

if __name__ == '__main__':
    main()