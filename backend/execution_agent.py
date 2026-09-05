import random
from datetime import datetime

from backend.database import get_connection
from backend.measurement import record_campaign_result


def execute_campaign(campaign_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM campaigns
        WHERE id = ?
        """,
        (campaign_id,)
    )

    campaign = cursor.fetchone()

    connection.close()

    if not campaign:
        return {
            "status": "ERROR",
            "message": f"Campaign #{campaign_id} not found."
        }

    campaign = dict(campaign)

    if campaign["status"] != "APPROVED":
        return {
            "status": "ERROR",
            "message": (
                f"Campaign #{campaign_id} cannot be executed. "
                f"Current status: {campaign['status']}"
            )
        }

    targeted_customers = campaign["target_customers"]

    # Synthetic campaign simulation
    exposed_customers = targeted_customers

    # Simulate campaign performance
    conversion_rate = random.uniform(0.20, 0.35)

    conversions = max(
        1,
        round(exposed_customers * conversion_rate)
    )

    # Recommended product price from the campaign
    product_price = 359.10

    campaign_revenue = (
        conversions * product_price
    )

    # Synthetic baseline for comparison
    baseline_conversion_rate = 10.0

    # Demo campaign cost
    campaign_cost = 2000.0

    # Record campaign measurement
    result = record_campaign_result(
        campaign_id=campaign_id,
        targeted_customers=targeted_customers,
        exposed_customers=exposed_customers,
        conversions=conversions,
        campaign_revenue=campaign_revenue,
        baseline_conversion_rate=baseline_conversion_rate,
        campaign_cost=campaign_cost,
        status="COMPLETED_SYNTHETIC"
    )

    # Update campaign status
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE campaigns
        SET status = ?
        WHERE id = ?
        """,
        ("EXECUTED", campaign_id)
    )

    connection.commit()
    connection.close()

    return {
        "status": "CAMPAIGN_EXECUTED",
        "campaign_id": campaign_id,
        "targeted_customers": targeted_customers,
        "exposed_customers": exposed_customers,
        "conversions": conversions,
        "campaign_revenue": round(campaign_revenue, 2),
        "campaign_cost": campaign_cost,
        "measurement_status": result["status"],
        "incremental_revenue": round(
            result["incremental_revenue"],
            2
        ),
        "roi": round(
            result["roi"],
            2
        ),
        "executed_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


if __name__ == "__main__":

    campaign_id = 3

    print("\n⚡ GrowthPilot AI — Campaign Execution Agent\n")

    result = execute_campaign(campaign_id)

    print("=" * 70)

    if result["status"] == "CAMPAIGN_EXECUTED":

        print(
            f"✅ Campaign #{result['campaign_id']} executed."
        )

        print(
            f"\n👥 Customers targeted:"
            f"\n{result['targeted_customers']}"
        )

        print(
            f"\n👀 Customers exposed:"
            f"\n{result['exposed_customers']}"
        )

        print(
            f"\n🛒 Conversions:"
            f"\n{result['conversions']}"
        )

        print(
            f"\n💰 Campaign revenue:"
            f"\n₹{result['campaign_revenue']:,.2f}"
        )

        print(
            f"\n💸 Campaign cost:"
            f"\n₹{result['campaign_cost']:,.2f}"
        )

        print(
            f"\n📈 Incremental revenue:"
            f"\n₹{result['incremental_revenue']:,.2f}"
        )

        print(
            f"\n📊 ROI:"
            f"\n{result['roi']:.2f}%"
        )

        print(
            f"\n🧪 Measurement:"
            f"\n{result['measurement_status']}"
        )

        print(
            "\n⚠️ These campaign results are synthetic "
            "demo data, not real merchant performance."
        )

    else:

        print(
            f"❌ {result['message']}"
        )

    print("=" * 70)