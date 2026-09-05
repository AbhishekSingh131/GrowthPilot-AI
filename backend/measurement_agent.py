from backend.database import get_connection


def analyze_campaign(campaign_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM campaign_results
        WHERE campaign_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (campaign_id,)
    )

    result = cursor.fetchone()
    connection.close()

    if not result:
        return {
            "error": f"No result found for campaign #{campaign_id}"
        }

    result = dict(result)

    roi = result["roi"]
    conversions = result["conversions"]
    incremental_revenue = result["incremental_revenue"]
    campaign_cost = result["campaign_cost"]

    # Decision logic
    if roi > 100:
        decision = "SCALE"
        emoji = "🟢"
        recommendation = (
            "Scale this campaign to a larger customer segment "
            "while continuing to monitor conversion rate and ROI."
        )

    elif roi >= 0:
        decision = "OPTIMIZE"
        emoji = "🟡"
        recommendation = (
            "Optimize the campaign targeting, offer or message "
            "before increasing the campaign budget."
        )

    else:
        decision = "STOP"
        emoji = "🔴"
        recommendation = (
            "Stop this campaign and investigate the targeting, "
            "offer and customer response before spending more."
        )

    reason = (
        f"The campaign generated ₹{incremental_revenue:,.2f} "
        f"in incremental revenue against a campaign cost of "
        f"₹{campaign_cost:,.2f}, resulting in an ROI of {roi:.2f}%."
    )

    return {
        "campaign_id": campaign_id,
        "roi": roi,
        "conversions": conversions,
        "incremental_revenue": incremental_revenue,
        "campaign_cost": campaign_cost,
        "decision": decision,
        "emoji": emoji,
        "reason": reason,
        "recommendation": recommendation
    }


if __name__ == "__main__":

    campaign_id = 1

    analysis = analyze_campaign(campaign_id)

    print("\n🤖 GrowthPilot AI — Measurement Agent\n")

    if "error" in analysis:
        print(f"❌ {analysis['error']}")

    else:
        print("=" * 70)

        print(
            f"Campaign #{analysis['campaign_id']}"
        )

        print(
            f"ROI: {analysis['roi']:.2f}%"
        )

        print(
            f"Incremental revenue: "
            f"₹{analysis['incremental_revenue']:,.2f}"
        )

        print(
            f"Campaign cost: "
            f"₹{analysis['campaign_cost']:,.2f}"
        )

        print(
            f"\nDecision: "
            f"{analysis['emoji']} {analysis['decision']}"
        )

        print(
            f"\nReason:\n"
            f"{analysis['reason']}"
        )

        print(
            f"\nRecommendation:\n"
            f"{analysis['recommendation']}"
        )

        print("=" * 70)