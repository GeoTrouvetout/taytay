from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, Graph, StateGraph, START
from langgraph.graph.message import MessagesState

import chainlit as cl
from langgraph.graph.state import CompiledStateGraph
import requests
import json
import chromadb
from graph import setup_graph

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# client = chromadb.PersistentClient(path="./chroma-data")

# vectorstore = Chroma(
#     collection_name="taylor_swift_wiki",
#     client=client,
#     embedding_function=embedding_model,
# )


@cl.on_chat_start
async def on_chat_start():
    # welcome = cl.Message(
    #     content=(
    #         "Bonjour :)! Je suis une IA spécialisée en analyse littéraire des paroles de Taylor Swift "
    #         "(a.k.a TayTay). Demande-moi ce que tu veux à ce sujet et j'essayerai d'y répondre :)"
    #     )
    # )
    graph = setup_graph()
    cl.user_session.set("graph", graph)


def get_graph() -> CompiledStateGraph:
    graph = cl.user_session.get("graph")
    return graph


@cl.on_message
async def on_message(user_msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = None

    initial_state = {"messages": [HumanMessage(content=user_msg.content)]}

    graph = get_graph()
    for node_msg, metadata in graph.stream(
        initial_state,
        stream_mode="messages",
        config=RunnableConfig(callbacks=[cb], **config),
    ):
        node = metadata.get("langgraph_node")
        if node == "answer":
            if not final_answer:
                final_answer = cl.Message(content="")

            await final_answer.stream_token(node_msg.content)

    if final_answer:
        await final_answer.send()
