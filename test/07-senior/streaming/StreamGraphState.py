from typing import TypedDict

from langgraph.graph import StateGraph, START, END, add_messages
from langsmith.env import get_runtime_and_metrics


class DiliState(TypedDict):
    topic: str
    joke: str


def refine_topic(state: DiliState):
    return {"topic": state["topic"] + " and cats"}


def generate_joke(state: DiliState):
    return {"joke": f"This is a joke about {state['topic']}"}

def main():
    graph = (
    StateGraph(DiliState)
    .add_node("refine_topic", refine_topic)
    .add_node("generate_joke", generate_joke)
    .add_node("add_messages", add_messages)
    .add_edge(START, "refine_topic")
    .add_edge("refine_topic", "generate_joke")
    .add_edge("generate_joke", "add_messages")
    .add_edge("add_messages", END)
    .compile()
    )

    print(graph.get)

    for chunk in graph.stream({"topic": "ice cream"}, stream_mode="values"):
        print(chunk)

    for chunk in graph.stream({"topic": "ice cream"}, stream_mode="updates"):
        print(chunk)
