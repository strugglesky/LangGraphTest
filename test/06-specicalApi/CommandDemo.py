import operator
from time import struct_time
from typing import Annotated

from numpy.distutils.system_info import fftw_info
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

# 全局常量：统一递归限制，便于维护
RECURSION_LIMIT = 20


# 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]  # 自动合并消息
    current_agent: str
    task_completed: bool
    count: int

def decision_agent(state: AgentState) -> Command[AgentState]:
    print("执行节点: decision_agent")
    if state["task_completed"]:
        print("✅ 检测到任务已完成，直接终止流程")
        return Command(
            update={"messages": [("system", "所有任务处理完成，流程正常结束")]},
            goto=END,
        )
    # 提取消息文本（兼容空消息）
    last_message = state["messages"][-1] if state["messages"] else ("", "")
    last_msg_content = last_message[1]
    print(f"最新消息文本: {last_msg_content}")

    if "计算" in last_msg_content:
        print("✅ 检测到数学任务，路由到数学代理")
        return Command(
            update={
                "messages": [("system", "路由到数学代理")],
                "current_agent": "math_agent",
            },
            goto="math_agent",
        )
    else:
        print("✅ 检测到非数学任务，任务结束")
        return Command(
            update={
                "messages": [("system", "任务已经结束")],
                "current_agent": "END",
                "task_completed": True
            },
            goto="END",
        )

def math_agent(state: AgentState) -> Command[AgentState]:
    print("执行节点: math_agent")
    count_ = state['count'] + 1
    print(f"count结果: {count_}")
    flag: bool = False
    if count_ >= 100:
        flag = True
    return Command(
        update={
            "messages": [("assistant", f"count计算结果: {count_}")],
            "current_agent": "decision_agent",
            "count": count_,
            "task_completed": flag,
        },
        goto="decision_agent",
    )

if __name__ == '__main__':
    builder = StateGraph(AgentState)

    builder.add_node("decision_agent", decision_agent)
    builder.add_node("math_agent", math_agent)
    builder.add_edge(START, "decision_agent")
    builder.add_edge("decision_agent", END)

    graph = builder.compile()
    print(graph.get_graph().print_ascii())
    result = graph.invoke(
        {
            "messages": [("user", "我需要计算数学题")],
            "current_agent": "user",
            "task_completed": False,
            "count": 0,
        },
        {"recursion_limit": RECURSION_LIMIT},  # recursion_limit 必须放在 config 字典里
    )

    print(result)




