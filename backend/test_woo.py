from woocommerce_tools import get_products, get_orders_today, get_pending_orders, get_low_stock_products

print("PRODUCTS:")
print(get_products())

print("\nORDERS TODAY:")
print(get_orders_today())

print("\nPENDING ORDERS:")
print(get_pending_orders())

print("\nLOW STOCK:")
print(get_low_stock_products())
