from collections import defaultdict
from backend.database import get_connection


def get_product_sales():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            products.id,
            products.name,
            products.category,
            COUNT(orders.id) AS orders_count,
            SUM(orders.quantity) AS units_sold,
            SUM(orders.amount) AS revenue
        FROM orders
        JOIN products ON products.id = orders.product_id
        WHERE orders.status = 'paid'
        GROUP BY products.id
        ORDER BY revenue DESC
    """)

    results = cursor.fetchall()
    connection.close()

    return [dict(row) for row in results]


def find_cross_sell_opportunities():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        WITH customer_products AS (
            SELECT DISTINCT
                customer_id,
                product_id
            FROM orders
            WHERE status = 'paid'
        ),

        product_customers AS (
            SELECT
                product_id,
                COUNT(DISTINCT customer_id) AS customers_count
            FROM customer_products
            GROUP BY product_id
        ),

        product_pairs AS (
            SELECT
                cp1.product_id AS product_a_id,
                cp2.product_id AS product_b_id,
                COUNT(DISTINCT cp1.customer_id) AS customers_both
            FROM customer_products cp1
            JOIN customer_products cp2
                ON cp1.customer_id = cp2.customer_id
                AND cp1.product_id < cp2.product_id
            GROUP BY
                cp1.product_id,
                cp2.product_id
        )

        SELECT
            pp.product_a_id,
            pp.product_b_id,
            p1.name AS product_a,
            p2.name AS product_b,
            pc.customers_count AS customers_a,
            pp.customers_both
        FROM product_pairs pp

        JOIN products p1
            ON p1.id = pp.product_a_id

        JOIN products p2
            ON p2.id = pp.product_b_id

        JOIN product_customers pc
            ON pc.product_id = pp.product_a_id

        WHERE pp.customers_both > 0
    """)

    results = cursor.fetchall()
    connection.close()

    opportunities = []

    for row in results:
        data = dict(row)

        customers_a = data["customers_a"]
        customers_both = data["customers_both"]

        if customers_a == 0:
            continue

        cross_sell_rate = (
            customers_both / customers_a
        ) * 100

        opportunities.append({
            **data,
            "cross_sell_rate": round(
                cross_sell_rate,
                2
            )
        })

    opportunities.sort(
        key=lambda x: (
            x["cross_sell_rate"],
            x["customers_both"]
        ),
        reverse=True
    )

    return opportunities

def generate_opportunities():
    sales = get_product_sales()
    cross_sell = find_cross_sell_opportunities()

    opportunities = []

    # -----------------------------------------
    # 1. Top Revenue Product
    # -----------------------------------------

    if sales:
        top_product = sales[0]

        opportunities.append({
            "type": "revenue_product",
            "title": "Top Revenue Product",
            "product": top_product["name"],
            "revenue": top_product["revenue"],
            "recommendation": (
                f"Increase promotion of {top_product['name']} "
                "because it currently generates the highest revenue."
            )
        })

    # -----------------------------------------
    # 2. Cross-Sell Opportunity
    # -----------------------------------------

    if cross_sell:
        best_pair = cross_sell[0]

        # Estimate revenue opportunity
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT price
            FROM products
            WHERE id = ?
        """, (best_pair["product_b_id"],))

        product = cursor.fetchone()
        connection.close()

        product_price = product["price"]

        estimated_opportunity = (
            best_pair["customers_a"]
            * (best_pair["cross_sell_rate"] / 100)
            * product_price
        )

        # Simple confidence score
        confidence = min(
    95,
    round(
        best_pair["cross_sell_rate"] * 0.8
        + min(best_pair["customers_both"], 20) * 1.0,
        0
        )
    )

        opportunities.append({
            "type": "cross_sell",
            "title": "Revenue Opportunity",
            "product_a": best_pair["product_a"],
            "product_b": best_pair["product_b"],
            "customers_a": best_pair["customers_a"],
            "customers_both": best_pair["customers_both"],
            "cross_sell_rate": best_pair["cross_sell_rate"],
            "estimated_opportunity": round(
                estimated_opportunity,
                2
            ),
            "confidence": confidence,
            "recommendation": (
    f"Test a {best_pair['product_a']} + "
    f"{best_pair['product_b']} bundle with a small customer segment."
    if confidence < 70
    else
    f"Create a {best_pair['product_a']} + "
    f"{best_pair['product_b']} bundle."
)
        })

    return opportunities


if __name__ == "__main__":
    opportunities = generate_opportunities()

    print("\n🚀 GrowthPilot AI — Revenue Intelligence\n")

    for opportunity in opportunities:

        print("=" * 65)

        print(f"Type: {opportunity['type']}")
        print(f"Title: {opportunity['title']}")

        if opportunity["type"] == "revenue_product":

            print(f"Product: {opportunity['product']}")
            print(f"Revenue: ₹{opportunity['revenue']:,.2f}")

        elif opportunity["type"] == "cross_sell":

            print(
                f"{opportunity['product_a']} → "
                f"{opportunity['product_b']}"
            )

            print(
                f"Customers buying "
                f"{opportunity['product_a']}: "
                f"{opportunity['customers_a']}"
            )

            print(
                f"Also bought "
                f"{opportunity['product_b']}: "
                f"{opportunity['customers_both']}"
            )

            print(
                f"Cross-sell rate: "
                f"{opportunity['cross_sell_rate']}%"
            )

            print(
                f"Estimated opportunity: "
                f"₹{opportunity['estimated_opportunity']:,.2f}"
            )

            print(
                f"Confidence: "
                f"{opportunity['confidence']}%"
            )

        print(
            f"Recommended action: "
            f"{opportunity['recommendation']}"
        )