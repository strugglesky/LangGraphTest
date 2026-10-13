import os
from typing import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START,END

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

class State(TypedDict):
    query: str
    answer: str


def node(state: State):
    print("开始调用 node 节点")

    model = init_chat_model(
        model=os.getenv("Qwen_DefaultModel"),
        model_provider="openai",
        api_key=os.getenv("aliQwen-api"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    llm_result = model.invoke([("user", state["query"])])
    print("llm invoke 结束", end="\n\n")

    return {"answer": llm_result}

def main():
    graph = (
        StateGraph(state_schema=State)
        .add_node(node)
        .add_edge(START, "node")
        .add_edge("node", END)
        .compile()
    )
    print(graph.get_graph().print_ascii())

    inputs = {"query": "帮我生成一个200字的小学生作文，主题为我的一天"}
    for chunk, _metadata in graph.stream(inputs, stream_mode="messages"):
        print(chunk.content, _metadata, end="")

if __name__ == "__main__":
    main()
