from backend.database import get_connection


def analyze_product_opportunities():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        p1.name AS product_a,
        p2.name AS product_b,
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
    LIMIT 10
    """

    rows = cursor.execute(query).fetchall()

    connection.close()

    opportunities = []

    for row in rows:

        customers = row["customers"]

        if customers >= 40:
            priority = "HIGH"

        elif customers >= 20:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        opportunities.append({
            "product_a": row["product_a"],
            "product_b": row["product_b"],
            "customers": customers,
            "priority": priority
        })

    return opportunities


def generate_growth_recommendation():

    opportunities = analyze_product_opportunities()

    if not opportunities:
        return {
            "status": "NO_OPPORTUNITY",
            "message": "No strong product relationships discovered."
        }

    top = opportunities[0]

    product_a = top["product_a"]
    product_b = top["product_b"]
    customers = top["customers"]

    recommendation = (
        f"Create a cross-sell campaign for customers who purchase "
        f"{product_a}. Recommend {product_b} as the next-best product."
    )

    reason = (
        f"{customers} customers purchased both {product_a} "
        f"and {product_b}, making this the strongest observed "
        f"product relationship in the merchant's paid order data."
    )

    return {
        "status": "OPPORTUNITY_FOUND",
        "opportunity": top,
        "recommendation": recommendation,
        "reason": reason,
        "next_action": "CREATE_CAMPAIGN"
    }


if __name__ == "__main__":

    print("\n🤖 GrowthPilot AI — Growth Analyst Agent\n")

    result = generate_growth_recommendation()

    print("=" * 70)

    print(f"Status: {result['status']}")

    if result["status"] == "OPPORTUNITY_FOUND":

        opportunity = result["opportunity"]

        print(
            f"\n🔥 Top Opportunity:"
        )

        print(
            f"{opportunity['product_a']} → "
            f"{opportunity['product_b']}"
        )

        print(
            f"Customers: "
            f"{opportunity['customers']}"
        )

        print(
            f"Priority: "
            f"{opportunity['priority']}"
        )

        print(
            f"\n💡 Recommendation:"
        )

        print(
            result["recommendation"]
        )

        print(
            f"\n🧠 Reason:"
        )

        print(
            result["reason"]
        )

        print(
            f"\n⚡ Next Action:"
        )

        print(
            result["next_action"]
        )

    else:

        print(
            result["message"]
        )

    print("=" * 70)