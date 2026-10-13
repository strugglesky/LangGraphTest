from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class DiliState(TypedDict):
    question: str
    answer: str
    confidence: float  # 置信度分数
    steps: list

def think(state: DiliState) -> DiliState:
    """思考节点：模拟多步推理，写入 steps。"""
    question = state["question"]
    steps = [f"分析问题: {question}", "检索相关知识", "形成初步答案"]
    return {"steps": steps}


def respond(state: DiliState) -> DiliState:
    """回应节点：根据关键词生成答案与置信度。"""
    question = state["question"]
    if "天气" in question:
        answer = "今天天气晴朗"
        confidence = 0.9
    elif "时间" in question:
        answer = "现在是上午10点"
        confidence = 0.8
    else:
        answer = "这是一个很好的问题"
        confidence = 0.7

    return {
        "answer": answer,
        "confidence": confidence,
    }

def reflect(state: DiliState) -> DiliState:
    """反思节点：在 steps 上追加校验与结论。"""
    answer = state["answer"]
    confidence = state["confidence"]
    steps = state.get("steps", [])

    steps.append(f"验证答案: {answer}")
    steps.append(f"置信度评估: {confidence}")

    if confidence > 0.8:
        conclusion = "高置信度答案"
    elif confidence > 0.5:
        conclusion = "中等置信度答案"
    else:
        conclusion = "低置信度答案"

    steps.append(f"结论: {conclusion}")

    return {"steps": steps}

def main():
    graph:StateGraph = (
        StateGraph(DiliState)
        .add_node("think", think)
        .add_node("respond", respond)
        .add_node("reflect", reflect)
        .add_edge(START, "think")
        .add_edge("think", "respond")
        .add_edge("respond", "reflect")
        .add_edge("reflect", END)
        .compile()
    )
    print(graph.get_graph().print_ascii())

    print("=== LangGraph 多模式流式传输演示 ===\n")

    input_state = {
        "question": "今天天气怎么样?",
        "answer": "",
        "confidence": 0.0,
        "steps": [],
    }

    print("--- 1. 同时使用 stream_mode=[values, updates] 多种流模式 ---")

    for mode, chunk in graph.stream(input_state, stream_mode=["values","updates"]):
        print(f"  [{mode}]: {chunk}")

    print("="*20)

    print("--- 2. 使用 debug 模式 ---")

    for chunk in graph.stream(input_state, stream_mode=["debug"]):
        print(f"  {chunk}")

if __name__ == '__main__':
    main()