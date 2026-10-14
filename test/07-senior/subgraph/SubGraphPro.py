from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# 定义不同结构的父子图状态
# 父图状态：仅包含用户查询和最终答案（与子图状态完全不同）
class ParentState(TypedDict):
    user_query: str
    final_answer: str | None


# 子图状态：专注于分析逻辑（与父图状态无重叠字段）
class SubgraphState(TypedDict):
    analysis_input: str
    analysis_result: str
    intermediate_steps: list


# 定义子图核心逻辑
def subgraph_analysis_node(state: SubgraphState) -> SubgraphState:
    """子图核心节点：模拟分析流水线。"""
    query = state["analysis_input"]
    state["intermediate_steps"] = [f"解析查询：{query}", "执行分析逻辑", "生成结果"]
    state["analysis_result"] = f"针对「{query}」的分析结果：这是子图处理后的内容"
    return state


def build_subgraph() -> StateGraph:
    sub_builder = StateGraph(SubgraphState)
    sub_builder.add_node("subgraph_analysis_node", subgraph_analysis_node)
    sub_builder.add_edge(START, "subgraph_analysis_node")
    sub_builder.add_edge("subgraph_analysis_node", END)
    return sub_builder.compile()

compiled_subgraph = build_subgraph()

# 定义父图代理节点（核心：状态转换+调用子图）从节点调用图
def call_subgraph_proxy(state: ParentState) -> ParentState:
    """
    父图代理节点：
    1) 父 -> 子：拼子图输入；
    2) 调用子图 invoke；
    3) 子 -> 父：把 analysis_result 写入 final_answer。
    """
    subgraph_input = {
        "analysis_input": state["user_query"],
        "intermediate_steps": [],
        "analysis_result": "",
    }

    subgraph_response = compiled_subgraph.invoke(subgraph_input)

    return {
        "user_query": state["user_query"],
        "final_answer": subgraph_response["analysis_result"],
    }

def build_parent_graph():
    parent_builder = StateGraph(ParentState)
    # 添加代理节点（核心：手动处理状态转换+调用子图）
    parent_builder.add_node("subgraph_proxy", call_subgraph_proxy)
    # 父图执行链路：START → 代理节点 → END
    parent_builder.add_edge(START, "subgraph_proxy")
    parent_builder.add_edge("subgraph_proxy", END)
    return parent_builder.compile()

def main():
    # 1. 构建父图
    parent_graph = build_parent_graph()
    parent_graph.get_graph().print_ascii()

    # 2. 定义父图初始状态（仅包含user_query，符合父图状态结构）
    initial_state = {
        "user_query": "请分析Python中StateGraph的使用场景",
        "final_answer": None,
    }
    print("父图初始状态：", initial_state)

    # 3. 执行父图，实际而言父图调用了call_subgraph_proxy
    final_state = parent_graph.invoke(initial_state)

    # 4. 输出结果
    print("\n父图最终状态：", final_state)
    print("\n子图处理后的最终答案：", final_state["final_answer"])


if __name__ == "__main__":
    main()
