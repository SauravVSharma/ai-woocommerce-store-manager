from typing import TypedDict, Optional, Dict, Any, List
from langgraph.graph import StateGraph, START, END

from woocommerce_tools import (
    get_products,
    get_orders_today,
    get_pending_orders,
    get_low_stock_products
)

from ollama_client import ask_ollama
from memory import add_memory, format_memory


class AgentState(TypedDict):
    question: str
    user_email: str
    memory: Optional[str]
    selected_tools: List[str]
    tool_results: Dict[str, Any]
    answer: Optional[str]


def choose_tools(state: AgentState) -> AgentState:
    question = state["question"].lower()

    selected_tools = []

    if (
        "orders today" in question
        or "today order" in question
        or "revenue today" in question
        or "sales today" in question
    ):
        selected_tools.append("get_orders_today")

    if (
        "pending orders" in question
        or "pending order" in question
        or "processing orders" in question
        or "on hold orders" in question
    ):
        selected_tools.append("get_pending_orders")

    if (
        "low stock" in question
        or "stock low" in question
        or "out of stock soon" in question
        or "less stock" in question
    ):
        selected_tools.append("get_low_stock_products")

    if (
        "products" in question
        or "product list" in question
        or "show product" in question
        or "list product" in question
    ):
        selected_tools.append("get_products")

    return {
        **state,
        "selected_tools": selected_tools
    }


def run_tools(state: AgentState) -> AgentState:
    selected_tools = state.get("selected_tools", [])
    tool_results = {}

    for tool in selected_tools:

        if tool == "get_orders_today":
            tool_results[tool] = get_orders_today()

        elif tool == "get_pending_orders":
            tool_results[tool] = get_pending_orders()

        elif tool == "get_low_stock_products":
            tool_results[tool] = get_low_stock_products()

        elif tool == "get_products":
            tool_results[tool] = get_products()

    return {
        **state,
        "tool_results": tool_results
    }


def generate_answer(state: AgentState) -> AgentState:
    question = state["question"]
    selected_tools = state.get("selected_tools", [])
    tool_results = state.get("tool_results", {})
    conversation_history = state.get("memory")

    if not selected_tools:
        prompt = f"""
You are an AI WooCommerce Store Manager.

Previous Conversation:
{conversation_history}

User Question:
{question}

Answer clearly and briefly.
If the user refers to previous context, use the previous conversation.
Do not invent WooCommerce store data.
"""

        answer = ask_ollama(prompt)

        return {
            **state,
            "answer": answer
        }

    prompt = f"""
You are an AI WooCommerce Store Manager.

Previous Conversation:
{conversation_history}

User Question:
{question}

Tools Used:
{selected_tools}

Live WooCommerce Tool Results:
{tool_results}

Create a clear, short, business-friendly answer.
If multiple tools were used, combine the results into one useful summary.
Do not invent data.
Only use the provided tool results and previous conversation.
"""

    answer = ask_ollama(prompt)

    return {
        **state,
        "answer": answer
    }


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("choose_tools", choose_tools)
    graph.add_node("run_tools", run_tools)
    graph.add_node("generate_answer", generate_answer)

    graph.add_edge(START, "choose_tools")
    graph.add_edge("choose_tools", "run_tools")
    graph.add_edge("run_tools", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()


app_graph = build_graph()


def run_langgraph_agent(question: str, user_email: str = "guest"):
    memory_text = format_memory(user_email)

    result = app_graph.invoke({
        "question": question,
        "user_email": user_email,
        "memory": memory_text,
        "selected_tools": [],
        "tool_results": {},
        "answer": None
    })

    add_memory(user_email, "user", question)
    add_memory(user_email, "assistant", result["answer"])

    return result["answer"]
