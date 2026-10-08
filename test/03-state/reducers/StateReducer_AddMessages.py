from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class AddMessagesState(TypedDict):
    messages: Annotated[List,add_messages]

def chat_node_1(state: AddMessagesState) -> dict:
    print(f'执行第{len(state["messages"])}个节点')
    return {"messages": [("assistant", "Hello from node 1")]}


def chat_node_2(state: AddMessagesState) -> dict:
    print(f'执行第{len(state["messages"])}个节点')
    return {"messages": [("assistant", "Hello from node 2")]}

def run_demo():
    print("2. add_messages Reducer（消息列表专用）演示:")
    builder = StateGraph(AddMessagesState)
    builder.add_node("chat1", chat_node_1)
    builder.add_node("chat2", chat_node_2)
    builder.add_edge(START, "chat1")
    builder.add_edge(START, "chat2")  # 两节点并行，各自追加消息
    builder.add_edge("chat1", END)
    builder.add_edge("chat2", END)
    app = builder.compile()
    # 打印图形结构
    print(app.get_graph().print_ascii())

    result = app.invoke({"messages": [("human","hi there"),("user","I want to chat")]})
    print(f'app调用结果: {result}')

if __name__ == '__main__':
    run_demo()
