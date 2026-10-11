from typing import TypedDict, Annotated

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages


# 1. 定义 State
class State(TypedDict):
    messages: Annotated[list[str], add_messages]

# 2. 定义节点 (Actor)
def node_a(state: State):
    print(f'Node A: {state["messages"]}')
    return {"messages": ["My..."]}

# 3. 构建图
builder = StateGraph(State)
builder.add_node("a", node_a)
builder.add_edge(START,"a")
builder.add_edge("a", END)

# 4. 实例化 Checkpointer (这里用内存版做演示)
memory = InMemorySaver()

# 5. 编译时绑定 Checkpointer
graph = builder.compile(checkpointer=memory)
print(graph.get_graph().print_ascii())
config = {"configurable": {"thread_id": "user_123"}}

# 第一次调用
res1 = graph.invoke({"messages": ["Hello"]}, config)
print(res1)
# Checkpointer 自动保存了状态

# 第二次调用（同一个 thread_id）
res2 = graph.invoke({"messages": ["World"]}, config)
print(res2)
# Checkpointer 自动加载了上一次的 "Hello"，并合并了 "World"