from typing import TypedDict

from langchain_core.utils import print_text
from langgraph.graph import START,END,StateGraph
import uuid

class HelloState(TypedDict):
    name: str
    greeting: str

def greet(helloState: HelloState) -> dict:
    name = helloState['name']
    print(f'HelloState中的name为：{name}')
    return {"greeting": "how are you" + name}

def add_emoji(helloState: HelloState) -> dict:
    greeting = helloState['greeting']
    greeting += ' 。。。😄'
    return {"greeting": greeting}

graph = StateGraph(HelloState)
graph.add_node("greet", greet)
graph.add_node("add_emoji", add_emoji)
graph.add_edge(START,"greet")
graph.add_edge("greet","add_emoji")
graph.add_edge("add_emoji",END)

app = graph.compile()
result = app.invoke({"name": 'lili'})
print(result)
print(result['greeting'])

print(app.get_graph().print_ascii())
print("="*20)
print(app.get_graph().draw_mermaid())
print("="*20)