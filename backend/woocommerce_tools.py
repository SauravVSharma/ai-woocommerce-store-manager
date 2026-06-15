import mysql.connector
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "hr_bot"
}

TABLE_PREFIX = "wp_"


def db_conn():
    return mysql.connector.connect(**DB_CONFIG)


def get_products(limit=10):
    conn = db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
        SELECT 
            p.ID as id,
            p.post_title as name,
            price.meta_value as price,
            stock.meta_value as stock_quantity,
            stock_status.meta_value as stock_status
        FROM {TABLE_PREFIX}posts p
        LEFT JOIN {TABLE_PREFIX}postmeta price 
            ON p.ID = price.post_id AND price.meta_key = '_price'
        LEFT JOIN {TABLE_PREFIX}postmeta stock 
            ON p.ID = stock.post_id AND stock.meta_key = '_stock'
        LEFT JOIN {TABLE_PREFIX}postmeta stock_status 
            ON p.ID = stock_status.post_id AND stock_status.meta_key = '_stock_status'
        WHERE p.post_type = 'product'
        AND p.post_status = 'publish'
        ORDER BY p.ID DESC
        LIMIT %s
    """, (limit,))

    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        "total": len(products),
        "products": products
    }


def get_orders_today():
    conn = db_conn()
    cursor = conn.cursor(dictionary=True)

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(f"""
        SELECT 
            p.ID as id,
            p.post_status as status,
            p.post_date as created_at,
            total.meta_value as total
        FROM {TABLE_PREFIX}posts p
        LEFT JOIN {TABLE_PREFIX}postmeta total
            ON p.ID = total.post_id AND total.meta_key = '_order_total'
        WHERE p.post_type = 'shop_order'
        AND DATE(p.post_date) = %s
        ORDER BY p.ID DESC
    """, (today,))

    orders = cursor.fetchall()

    total_revenue = 0
    for order in orders:
        try:
            total_revenue += float(order.get("total") or 0)
        except:
            pass

    cursor.close()
    conn.close()

    return {
        "total_orders": len(orders),
        "total_revenue": total_revenue,
        "orders": orders
    }


def get_pending_orders():
    conn = db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
        SELECT 
            p.ID as id,
            p.post_status as status,
            p.post_date as created_at,
            total.meta_value as total
        FROM {TABLE_PREFIX}posts p
        LEFT JOIN {TABLE_PREFIX}postmeta total
            ON p.ID = total.post_id AND total.meta_key = '_order_total'
        WHERE p.post_type = 'shop_order'
        AND p.post_status IN ('wc-pending', 'wc-processing', 'wc-on-hold')
        ORDER BY p.ID DESC
        LIMIT 20
    """)

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_pending": len(orders),
        "orders": orders
    }


def get_low_stock_products(threshold=5):
    conn = db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
        SELECT 
            p.ID as id,
            p.post_title as name,
            stock.meta_value as stock_quantity,
            price.meta_value as price
        FROM {TABLE_PREFIX}posts p
        LEFT JOIN {TABLE_PREFIX}postmeta stock 
            ON p.ID = stock.post_id AND stock.meta_key = '_stock'
        LEFT JOIN {TABLE_PREFIX}postmeta price 
            ON p.ID = price.post_id AND price.meta_key = '_price'
        WHERE p.post_type = 'product'
        AND p.post_status = 'publish'
        AND stock.meta_value IS NOT NULL
        AND CAST(stock.meta_value AS UNSIGNED) <= %s
        ORDER BY CAST(stock.meta_value AS UNSIGNED) ASC
    """, (threshold,))

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "threshold": threshold,
        "total_low_stock": len(products),
        "products": products
    }
