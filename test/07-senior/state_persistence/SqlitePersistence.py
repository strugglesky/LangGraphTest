import sqlite3
import operator
from pathlib import Path
from typing import Annotated, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END


class MyState(TypedDict):
    messages: Annotated[list, operator.add]


def node_1(state: MyState):
    return {"messages": ["abc", "def"]}

def main():
    # 默认写在项目旁，避免硬编码 Windows 盘符
    db_dir = Path(__file__).resolve().parent / "sqlite_checkpoints"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "sqlite_data.db"

    conn = sqlite3.connect(database=str(db_path), check_same_thread=False)
    sqlite_db = SqliteSaver(conn=conn)

    builder = StateGraph(MyState)
    builder.add_node("node_1", node_1)

    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", END)

    graph = builder.compile(checkpointer=sqlite_db)

    # 同一 thread_id 表示同一会话；多次执行会累积检查点，调试时可删 .db 或换 thread_id
    config = {"configurable": {"thread_id": "user-001"}}

    initial_state = graph.get_state(config)
    print(f"Initial state: {initial_state}")

    result = graph.invoke({"messages": []}, config)
    print(f"Result: {result}")

    print()
    print("====================查看执行后的状态====================")
    final_state = graph.get_state(config)
    print()
    print(f"Final state: {final_state}")

    conn.close()


if __name__ == "__main__":
    main()

