import uuid

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, NotRequired


class StoryState(TypedDict):
    """故事状态：字段均可逐步写入。"""

    character: NotRequired[str]
    setting: NotRequired[str]
    plot: NotRequired[str]
    ending: NotRequired[str]


def create_character(state: StoryState):
    """创建故事角色（模拟 LLM 节点）。"""
    print("执行节点: create_character")

    mock_character = "一只会说话的猫"
    print(f"创建的角色: {mock_character}")
    return {"character": mock_character}


def set_setting(state: StoryState):
    """设置故事背景。"""
    print("执行节点: set_setting")

    mock_setting = "在一个神秘的图书馆里"
    print(f"设置的背景: {mock_setting}")
    return {"setting": mock_setting}


def develop_plot(state: StoryState):
    """发展故事情节。"""
    print("执行节点: develop_plot")

    character = state.get("character", "未知角色")
    setting = state.get("setting", "未知背景")
    mock_plot = f"{character}在{setting}发现了一本会发光的书"
    print(f"发展的剧情: {mock_plot}")
    return {"plot": mock_plot}


def write_ending(state: StoryState):
    """编写故事结局。"""
    print("执行节点: write_ending")

    plot = state.get("plot", "未知剧情")
    mock_ending = f"当{plot}时，整个图书馆都被魔法光芒照亮了"
    print(f"编写的结局: {mock_ending}")
    return {"ending": mock_ending}

def main():
    print("=== LangGraph 高级时间旅行演示 ===\n")

    workflow = StateGraph(StoryState)

    workflow.add_node("create_character", create_character)
    workflow.add_node("set_setting", set_setting)
    workflow.add_node("develop_plot", develop_plot)
    workflow.add_node("write_ending", write_ending)

    workflow.add_edge(START, "create_character")
    workflow.add_edge("create_character", "set_setting")
    workflow.add_edge("set_setting", "develop_plot")
    workflow.add_edge("develop_plot", "write_ending")
    workflow.add_edge("write_ending", END)

    graph = workflow.compile(checkpointer=InMemorySaver())
    print(graph.get_graph().print_ascii())

    print("1. 生成第一个故事...")
    config1 = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
        }
    }
    story1 = graph.invoke({}, config1)

    print("2. 查看第一个故事的历史状态...")
    state_history = list(graph.get_state_history(config1))
    for state in state_history:
        if state.config and 'configurable' in state.config:
            print(state.config['configurable']['checkpoint_id'], " ", state.next," ",state)
        else:
            print(state.next," ",state)
    print(len(state_history))
    print(type(state_history[0]))
    print(dir(state_history[0]))

    print("3. 从中间状态恢复执行，创建第二个故事...")
    # state_history
    character_state = state_history[2]
    print(f"选中的状态: {character_state.next}")
    print(f"选中的状态值: {character_state.values}")
    new_config = character_state.config
    print(f"新配置: {new_config}")

    runable_config = graph.update_state(
        new_config,
        values={"character": "一只会打篮球的鸡"}
    )
    print(f'runable_config: {runable_config}')
    story2 = graph.invoke(None, runable_config)

    history_cfg = {"configurable": {"thread_id": config1["configurable"]["thread_id"]}}
    state_history2 = list(graph.get_state_history(history_cfg))
    for state in state_history2:
        if state.config and 'configurable' in state.config:
            print(state.config['configurable']['checkpoint_id'], " ",
                  state.metadata.get("source"), " ",
                  state.next, " ", state)
        else:
            print(state.next, " ", state)
    print(story2)


if __name__ == '__main__':
    main()