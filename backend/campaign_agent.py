from datetime import datetime

from backend.database import get_connection
from backend.recommendation_agent import generate_recommendation


def create_campaign():

    recommendation = generate_recommendation()

    if recommendation["status"] != "RECOMMENDATION_CREATED":
        return {
            "status": "CAMPAIGN_NOT_CREATED",
            "reason": "No recommendation available."
        }

    connection = get_connection()
    cursor = connection.cursor()

    target_product = recommendation["target_product"]
    recommended_product = recommendation["recommended_product"]
    discount_percent = recommendation["discount_percent"]
    customer_segment_size = recommendation["customer_segment_size"]

    campaign_name = (
        f"{recommended_product} Cross-Sell Campaign"
    )

    offer = (
        f"{discount_percent}% OFF {recommended_product}"
    )

    expected_revenue = (
        customer_segment_size
        * recommendation["recommended_price"]
        * 0.20
    )

    cursor.execute(
        """
        INSERT INTO campaigns
        (
            campaign_type,
            name,
            product_a,
            product_b,
            offer,
            target_customers,
            status,
            expected_revenue,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "CROSS_SELL",
            campaign_name,
            target_product,
            recommended_product,
            offer,
            customer_segment_size,
            "PENDING_APPROVAL",
            expected_revenue,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    campaign_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "status": "CAMPAIGN_CREATED",
        "campaign_id": campaign_id,
        "campaign_name": campaign_name,
        "campaign_type": "CROSS_SELL",
        "target_product": target_product,
        "recommended_product": recommended_product,
        "target_customers": customer_segment_size,
        "offer": offer,
        "offer_price": recommendation["recommended_price"],
        "expected_revenue": round(expected_revenue, 2),
        "campaign_status": "PENDING_APPROVAL"
    }


if __name__ == "__main__":

    print("\n🚀 GrowthPilot AI — Campaign Agent\n")

    result = create_campaign()

    print("=" * 70)

    print(f"Status: {result['status']}")

    if result["status"] == "CAMPAIGN_CREATED":

        print(
            f"\n🆔 Campaign ID:"
            f"\n{result['campaign_id']}"
        )

        print(
            f"\n📢 Campaign:"
            f"\n{result['campaign_name']}"
        )

        print(
            f"\n🎯 Target:"
            f"\nCustomers who purchased {result['target_product']}"
        )

        print(
            f"\n🛍️ Recommended product:"
            f"\n{result['recommended_product']}"
        )

        print(
            f"\n👥 Target customers:"
            f"\n{result['target_customers']}"
        )

        print(
            f"\n🏷️ Offer:"
            f"\n{result['offer']}"
        )

        print(
            f"\n💵 Offer price:"
            f"\n₹{result['offer_price']:,.2f}"
        )

        print(
            f"\n📈 Expected revenue:"
            f"\n₹{result['expected_revenue']:,.2f}"
        )

        print(
            f"\n⏳ Status:"
            f"\n{result['campaign_status']}"
        )

    print("=" * 70)