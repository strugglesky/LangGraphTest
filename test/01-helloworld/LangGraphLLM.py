import json
import os
from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage, message_to_dict
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

class DiliState(TypedDict):
    messages: Annotated[List, add_messages]

llm = init_chat_model(
    model="qwen3.7-flash",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    extra_body={"enable_thinking": False},
    temperature=0
)

# 3. 定义节点 Nodes：将当前消息列表交给模型，返回新消息字典（add_messages 会追加到 state）
def model_node(state: DiliState):
    reply = llm.invoke(state["messages"])
    print(f'messages的长度： {len(state["messages"])}')
    return {"messages": [reply]}

def check_node(state: DiliState):
    print(f'DiliState中的messages信息：',end="")
    print(state["messages"])
    print(f'messages的长度： {len(state["messages"])}')
    return state

graph = StateGraph(DiliState)
graph.add_node("model", model_node)
graph.add_node("check", check_node)

graph.add_edge(START, "model")
graph.add_edge("model", "check")
graph.add_edge("check", END)
app = graph.compile()

result = app.invoke({"messages": [HumanMessage(content="请用一句话解释什么是 LangGraph。")]})

print("模型回答：", result["messages"])

print("\n--- result 格式化输出 ---")
print(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
        default=lambda o: message_to_dict(o) if isinstance(o, BaseMessage) else str(o),
    )
)

# 可视化
print(app.get_graph().print_ascii())
print("=" * 50)
print(app.get_graph().draw_mermaid())
print("=" * 50)