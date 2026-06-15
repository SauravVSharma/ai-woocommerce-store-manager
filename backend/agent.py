from woocommerce_tools import (
    get_products,
    get_orders_today,
    get_pending_orders,
    get_low_stock_products
)

def run_agent(question):

    q = question.lower()

    if "orders today" in q:
        return get_orders_today()

    if "pending orders" in q:
        return get_pending_orders()

    if "low stock" in q:
        return get_low_stock_products()

    if "products" in q:
        return get_products()

    return None
