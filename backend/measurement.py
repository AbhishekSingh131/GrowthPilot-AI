from datetime import datetime

from backend.database import get_connection


def record_campaign_result(
    campaign_id,
    targeted_customers,
    exposed_customers,
    conversions,
    campaign_revenue,
    baseline_conversion_rate,
    campaign_cost,
    status="COMPLETED"
):
    campaign_conversion_rate = (
        conversions / exposed_customers * 100
        if exposed_customers > 0
        else 0
    )

    baseline_conversions = (
        exposed_customers * baseline_conversion_rate / 100
    )

    incremental_conversions = (
        conversions - baseline_conversions
    )

    average_revenue_per_conversion = (
        campaign_revenue / conversions
        if conversions > 0
        else 0
    )

    incremental_revenue = (
        incremental_conversions
        * average_revenue_per_conversion
    )

    roi = (
        (
            (incremental_revenue - campaign_cost)
            / campaign_cost
        ) * 100
        if campaign_cost > 0
        else 0
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO campaign_results
        (
            campaign_id,
            targeted_customers,
            exposed_customers,
            conversions,
            campaign_revenue,
            baseline_conversion_rate,
            campaign_conversion_rate,
            incremental_conversions,
            incremental_revenue,
            campaign_cost,
            roi,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            campaign_id,
            targeted_customers,
            exposed_customers,
            conversions,
            campaign_revenue,
            baseline_conversion_rate,
            campaign_conversion_rate,
            incremental_conversions,
            incremental_revenue,
            campaign_cost,
            roi,
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    connection.commit()
    connection.close()

    return {
        "campaign_id": campaign_id,
        "targeted_customers": targeted_customers,
        "exposed_customers": exposed_customers,
        "conversions": conversions,
        "campaign_revenue": campaign_revenue,
        "baseline_conversion_rate": baseline_conversion_rate,
        "campaign_conversion_rate": campaign_conversion_rate,
        "incremental_conversions": incremental_conversions,
        "incremental_revenue": incremental_revenue,
        "campaign_cost": campaign_cost,
        "roi": roi,
        "status": status
    }


def get_campaign_results():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM campaign_results
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return [dict(result) for result in results]


if __name__ == "__main__":

    results = get_campaign_results()

    print("\n📊 GrowthPilot AI — Campaign Measurement\n")

    if not results:
        print("No campaign results recorded yet.")

    for result in results:

        print("=" * 70)

        print(
            f"Campaign ID: "
            f"{result['campaign_id']}"
        )

        print(
            f"Targeted customers: "
            f"{result['targeted_customers']}"
        )

        print(
            f"Exposed customers: "
            f"{result['exposed_customers']}"
        )

        print(
            f"Conversions: "
            f"{result['conversions']}"
        )

        print(
            f"Campaign revenue: "
            f"₹{result['campaign_revenue']:,.2f}"
        )

        print(
            f"Baseline conversion: "
            f"{result['baseline_conversion_rate']:.2f}%"
        )

        print(
            f"Campaign conversion: "
            f"{result['campaign_conversion_rate']:.2f}%"
        )

        print(
            f"Incremental conversions: "
            f"{result['incremental_conversions']:.2f}"
        )

        print(
            f"Incremental revenue: "
            f"₹{result['incremental_revenue']:,.2f}"
        )

        print(
            f"Campaign cost: "
            f"₹{result['campaign_cost']:,.2f}"
        )

        print(
            f"ROI: "
            f"{result['roi']:.2f}%"
        )

        print(
            f"Status: "
            f"{result['status']}"
        )