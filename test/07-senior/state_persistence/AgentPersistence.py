import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

def main():
    llm = init_chat_model(
        model=os.getenv("Qwen_DefaultModel"),
        model_provider="openai",
        api_key=os.getenv("aliQwen-api"),
        temperature=0.0,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    checkpointer = InMemorySaver()
    agent = create_agent(model=llm, checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "user-001"}}

    msg1 = agent.invoke(
        {"messages": [("user", "你好，我叫张三，喜欢足球，60字内简洁回复")]},
        config,
    )
    msg1["messages"][-1].pretty_print()

    msg2 = agent.invoke(
        {"messages": [("user", "我叫什么？我喜欢做什么？")]},
        config,
    )
    msg2["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()