import operator
from typing import TypedDict, Annotated

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END


class ParentState(TypedDict):
    count: Annotated[int, operator.add]


class SubgraphState(TypedDict):
    count: Annotated[int, operator.add]

def parent_node(state: ParentState) -> ParentState:
    print('进入父图节点')
    print(state['count'])
    """父图首节点：保证 parent_messages 为列表并追加父侧消息。"""
    return state

def subgraph_node(state: SubgraphState) -> SubgraphState:
    print('进入子图节点')
    print(state['count'])
    return state


def build_subgraph(saver: InMemorySaver):
    """构建并返回编译后的子图。"""
    sub_builder = StateGraph(SubgraphState)
    sub_builder.add_node("sub_node", subgraph_node)
    sub_builder.add_edge(START, "sub_node")
    sub_builder.add_edge("sub_node", END)
    return sub_builder.compile(saver)


def build_parent_graph(compiled_subgraph, saver:InMemorySaver):
    """构建并返回编译后的父图。"""
    builder = StateGraph(ParentState)
    builder.add_node("parent_node", parent_node)
    builder.add_node("subgraph_node", compiled_subgraph)
    builder.add_edge(START, "parent_node")
    builder.add_edge("parent_node", "subgraph_node")
    builder.add_edge("subgraph_node", END)
    return builder.compile(saver)

def main():
    saver = InMemorySaver()
    config = {
        "configurable": {
            "thread_id": "user001"
        }
    }
    # 构建子图
    compiled_subgraph = build_subgraph(saver)
    print('子图')
    print(compiled_subgraph.get_graph().print_ascii())
    # 构建父图
    parent_graph = build_parent_graph(compiled_subgraph,saver)
    print('父图')
    print(parent_graph.get_graph().print_ascii())
    initial_state = {"count": 1}
    print("初始状态：", initial_state)

    # 父图执行时会进入子图；sub_message 不会出现在父图最终 dict（ParentState 无此键）
    final_state = parent_graph.invoke(initial_state, config)
    print("\n执行后最终状态：", final_state)
    for state in list(parent_graph.get_state_history(config)):
        print(state)

if __name__ == "__main__":
    main()
