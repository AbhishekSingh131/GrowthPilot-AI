import random
from datetime import datetime, timedelta

from backend.database import get_connection, create_tables


PRODUCTS = [
    ("Running Shoes", "Footwear", 2799, 50),
    ("Sports Socks", "Accessories", 399, 150),
    ("Gym T-Shirt", "Apparel", 799, 100),
    ("Track Pants", "Apparel", 1299, 80),
    ("Water Bottle", "Accessories", 499, 120),
    ("Yoga Mat", "Fitness", 999, 70),
    ("Gym Gloves", "Accessories", 699, 90),
    ("Sports Cap", "Accessories", 599, 100),
]


def create_customers(connection):
    cursor = connection.cursor()

    for i in range(1, 101):
        cursor.execute(
            """
            INSERT INTO customers (name, email)
            VALUES (?, ?)
            """,
            (
                f"Customer {i}",
                f"customer{i}@example.com"
            )
        )

    cursor.execute("""
        SELECT id
        FROM customers
        ORDER BY id
    """)

    rows = cursor.fetchall()

    return [row["id"] for row in rows]


def create_products(connection):
    cursor = connection.cursor()

    for product in PRODUCTS:
        cursor.execute(
            """
            INSERT INTO products
            (name, category, price, stock)
            VALUES (?, ?, ?, ?)
            """,
            product
        )

    cursor.execute("""
        SELECT id, name
        FROM products
        ORDER BY id
    """)

    rows = cursor.fetchall()

    return {
        row["name"]: row["id"]
        for row in rows
    }


def create_orders(connection, customer_ids, product_ids):

    cursor = connection.cursor()

    base_date = datetime.now()

    running_shoes = product_ids["Running Shoes"]
    sports_socks = product_ids["Sports Socks"]
    gym_tshirt = product_ids["Gym T-Shirt"]
    track_pants = product_ids["Track Pants"]
    water_bottle = product_ids["Water Bottle"]
    yoga_mat = product_ids["Yoga Mat"]
    gym_gloves = product_ids["Gym Gloves"]
    sports_cap = product_ids["Sports Cap"]

    for customer_id in customer_ids:

        number_of_purchases = random.randint(3, 8)

        # Customer segments with different buying preferences
        if customer_id % 5 == 1:
            preferred_products = [
                running_shoes,
                sports_socks,
                sports_cap
            ]

        elif customer_id % 5 == 2:
            preferred_products = [
                gym_tshirt,
                track_pants,
                gym_gloves
            ]

        elif customer_id % 5 == 3:
            preferred_products = [
                water_bottle,
                yoga_mat,
                sports_socks
            ]

        elif customer_id % 5 == 4:
            preferred_products = [
                running_shoes,
                sports_socks,
                gym_tshirt,
                water_bottle,
                sports_cap
            ]

        else:
            preferred_products = [
                sports_socks,
                gym_tshirt,
                track_pants,
                water_bottle,
                yoga_mat,
                gym_gloves,
                sports_cap
            ]

        purchased_products = set()

        for _ in range(number_of_purchases):

            # Strong Running Shoes → Sports Socks relationship
            if (
                running_shoes in purchased_products
                and random.random() < 0.70
            ):
                product_id = sports_socks

            # Strong Sports Socks → Running Shoes relationship
            elif (
                sports_socks in purchased_products
                and random.random() < 0.45
            ):
                product_id = running_shoes

            else:
                product_id = random.choice(
                    preferred_products
                )

            purchased_products.add(product_id)

            quantity = 1

            cursor.execute(
                """
                SELECT price
                FROM products
                WHERE id = ?
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:
                raise RuntimeError(
                    f"Product ID {product_id} was not found."
                )

            amount = product["price"] * quantity

            status = random.choices(
                ["paid", "failed"],
                weights=[95, 5]
            )[0]

            order_date = (
                base_date
                - timedelta(
                    days=random.randint(0, 90)
                )
            ).strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                """
                INSERT INTO orders
                (
                    customer_id,
                    product_id,
                    quantity,
                    amount,
                    status,
                    order_date
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    customer_id,
                    product_id,
                    quantity,
                    amount,
                    status,
                    order_date
                )
            )


def seed_database():

    create_tables()

    connection = get_connection()
    cursor = connection.cursor()

    # Clear old demo data
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM products")

    connection.commit()

    # Create fresh customers
    customer_ids = create_customers(connection)

    # Create fresh products and dynamically retrieve their IDs
    product_ids = create_products(connection)

    # Create realistic order history
    create_orders(
        connection,
        customer_ids,
        product_ids
    )

    connection.commit()
    connection.close()

    print("✅ GrowthPilot demo data created successfully!")
    print("📊 100 customers")
    print("🛍️ 8 products")
    print("📦 Realistic customer purchase patterns")
    print("🔗 Cross-sell behavior included")
    print("📅 90 days of order history")


if __name__ == "__main__":
    seed_database()