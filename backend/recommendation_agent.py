from backend.database import get_connection


def generate_recommendation():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        p1.name AS product_a,
        p2.name AS product_b,
        p2.price AS recommended_product_price,
        COUNT(DISTINCT o1.customer_id) AS customers
    FROM orders o1
    JOIN orders o2
        ON o1.customer_id = o2.customer_id
        AND o1.product_id < o2.product_id
    JOIN products p1
        ON p1.id = o1.product_id
    JOIN products p2
        ON p2.id = o2.product_id
    WHERE
        o1.status = 'paid'
        AND o2.status = 'paid'
    GROUP BY
        o1.product_id,
        o2.product_id
    ORDER BY
        customers DESC
    LIMIT 1
    """

    opportunity = cursor.execute(query).fetchone()

    connection.close()

    if not opportunity:
        return {
            "status": "NO_RECOMMENDATION"
        }

    product_a = opportunity["product_a"]
    product_b = opportunity["product_b"]
    customers = opportunity["customers"]
    product_price = opportunity["recommended_product_price"]

    # Simple bounded offer for the demo
    discount_percent = 10

    discounted_price = (
        product_price * (1 - discount_percent / 100)
    )

    return {
        "status": "RECOMMENDATION_CREATED",
        "target_product": product_a,
        "recommended_product": product_b,
        "customer_segment_size": customers,
        "original_price": product_price,
        "discount_percent": discount_percent,
        "recommended_price": round(discounted_price, 2),
        "reason": (
            f"{customers} customers purchased both "
            f"{product_a} and {product_b}."
        ),
        "recommendation": (
            f"Recommend {product_b} to customers who "
            f"purchase {product_a}, with a {discount_percent}% "
            f"cross-sell offer."
        ),
        "campaign_goal": "INCREASE_CROSS_SELL_REVENUE"
    }


if __name__ == "__main__":

    print("\n🤖 GrowthPilot AI — Recommendation Agent\n")

    result = generate_recommendation()

    print("=" * 70)

    print(f"Status: {result['status']}")

    if result["status"] == "RECOMMENDATION_CREATED":

        print(
            f"\n🎯 Target product:"
            f"\n{result['target_product']}"
        )

        print(
            f"\n🛍️ Recommended product:"
            f"\n{result['recommended_product']}"
        )

        print(
            f"\n👥 Customer segment:"
            f"\n{result['customer_segment_size']} customers"
        )

        print(
            f"\n💰 Original price:"
            f"\n₹{result['original_price']:,.2f}"
        )

        print(
            f"\n🏷️ Recommended offer:"
            f"\n{result['discount_percent']}% OFF"
        )

        print(
            f"\n💵 Offer price:"
            f"\n₹{result['recommended_price']:,.2f}"
        )

        print(
            f"\n🧠 Reason:"
            f"\n{result['reason']}"
        )

        print(
            f"\n💡 Recommendation:"
            f"\n{result['recommendation']}"
        )

        print(
            f"\n🎯 Campaign goal:"
            f"\n{result['campaign_goal']}"
        )

    print("=" * 70)