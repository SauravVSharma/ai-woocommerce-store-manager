from langgraph_agent import run_langgraph_agent

questions = [
    "show products",
    "show low stock products",
    "show orders today",
    "show pending orders",
    "what is WooCommerce?"
]

for q in questions:
    print("\nQUESTION:", q)
    print("ANSWER:")
    print(run_langgraph_agent(q))
    print("-" * 60)
