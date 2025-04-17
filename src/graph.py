from typing import Literal
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langchain_core.messages import (
    HumanMessage,
    RemoveMessage,
    SystemMessage,
)
from tools import get_albums, get_songs, get_lyrics
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import MessagesState
import requests


agent_prompt = """You are an expert specialized in analysis of Taylor Swift songs. Your role is to find any information that could help to answer user's question."""
answer_prompt = """You are an expert specialized in analysis of Taylor Swift songs. Provide a in-depth analysis of the user question."""


tools = [get_albums, get_songs, get_lyrics]
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
summarize_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
answer_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

model = model.bind_tools(tools)
answer_model = answer_model.with_config(tags=["answer"])
tool_node = ToolNode(tools=tools)


def should_continue(
    state: MessagesState,
) -> Literal["tools", "summarize", "answer"]:
    messages = state["messages"]
    print("FLAG", len(messages), messages)
    last_message = messages[-1]
    if (
        len([message for message in messages if isinstance(message, HumanMessage)]) > 6
    ):  # TODO: improve decision of summary call
        return "summarize"
    elif last_message.tool_calls:
        return "tools"
    return "answer"


def call_agent(state: MessagesState):
    messages = state["messages"]
    messages = [SystemMessage(agent_prompt)] + messages
    # print(messages)
    response = model.invoke(messages)
    return {"messages": [response]}


def call_answer(state: MessagesState):
    messages = state["messages"]
    messages = [SystemMessage(answer_prompt)] + messages
    # print(messages)
    response = answer_model.invoke(messages)
    return {"messages": [response]}


def call_summary(state: MessagesState):
    messages = state["messages"]
    summary_prompt = "Create a summary based on the conversation above:"
    messages = state["messages"] + [HumanMessage(content=summary_prompt)]
    response = summarize_model.invoke(messages)
    delete_messages = [
        RemoveMessage(id=m.id) for m in state["messages"][:-2]
    ]  # INFO: RemoveMessage send object that will remove message from state => This is used to remove message that has been summarized
    return {"messages": [response] + delete_messages}


def setup_graph():

    builder = StateGraph(MessagesState)

    builder.add_node("agent", call_agent)
    builder.add_node("tools", tool_node)
    builder.add_node("answer", call_answer)
    builder.add_node("summarize", call_summary)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent",
        should_continue,
        {"summarize": "summarize", "tools": "tools", "answer": "answer"},
    )

    builder.add_edge("tools", "agent")
    builder.add_edge("summarize", "agent")
    builder.add_edge("answer", END)

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph
