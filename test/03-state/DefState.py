from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class BasicState(TypedDict):
    """本图的 State Schema：字段名 + 类型共同定义这张图允许流转的状态结构。"""

    user_input: str
    response: str
    count: int
    process_data: dict

# 创建状态图：BasicState 是本图的 state_schema；本例不写 Annotated，因此各字段都走默认覆盖规则
basicState = StateGraph(BasicState)
# 无中间节点：直接从 START 到 END，状态会原样透传
basicState.add_edge(START, END)
app = basicState.compile()

# invoke 只接收一个核心参数（状态字典）；process_data 为 dict，需传入嵌套字典
initial_state = {
    "user_input": "a",
    "response": "resp",
    "count": 25,
    "process_data": {"k1": "v1"},
}

result = app.invoke(initial_state)
print(result)


