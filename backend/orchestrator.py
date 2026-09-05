from backend.growth_analyst import generate_growth_recommendation
from backend.recommendation_agent import generate_recommendation
from backend.campaign_agent import create_campaign


def run_growth_pipeline():

    print("\n🤖 GrowthPilot AI — Agent Orchestrator\n")
    print("=" * 70)

    # Step 1: Growth Analyst
    print("\n🔎 Step 1 — Growth Analyst Agent")

    growth_result = generate_growth_recommendation()

    if growth_result["status"] != "OPPORTUNITY_FOUND":
        return {
            "status": "PIPELINE_STOPPED",
            "stage": "GROWTH_ANALYST",
            "reason": growth_result.get(
                "message",
                "No growth opportunity found."
            )
        }

    opportunity = growth_result["opportunity"]

    print(
        f"Opportunity: "
        f"{opportunity['product_a']} → "
        f"{opportunity['product_b']}"
    )

    print(
        f"Customers: {opportunity['customers']}"
    )

    print(
        f"Priority: {opportunity['priority']}"
    )

    # Step 2: Recommendation Agent
    print("\n💡 Step 2 — Recommendation Agent")

    recommendation = generate_recommendation()

    if recommendation["status"] != "RECOMMENDATION_CREATED":
        return {
            "status": "PIPELINE_STOPPED",
            "stage": "RECOMMENDATION_AGENT",
            "reason": "No recommendation generated."
        }

    print(
        f"Recommend: "
        f"{recommendation['recommended_product']}"
    )

    print(
        f"Offer: "
        f"{recommendation['discount_percent']}% OFF"
    )

    print(
        f"Offer price: "
        f"₹{recommendation['recommended_price']:,.2f}"
    )

    # Step 3: Campaign Agent
    print("\n🚀 Step 3 — Campaign Agent")

    campaign = create_campaign()

    if campaign["status"] != "CAMPAIGN_CREATED":
        return {
            "status": "PIPELINE_STOPPED",
            "stage": "CAMPAIGN_AGENT",
            "reason": "Campaign could not be created."
        }

    print(
        f"Campaign ID: "
        f"{campaign['campaign_id']}"
    )

    print(
        f"Campaign: "
        f"{campaign['campaign_name']}"
    )

    print(
        f"Target customers: "
        f"{campaign['target_customers']}"
    )

    print(
        f"Expected revenue: "
        f"₹{campaign['expected_revenue']:,.2f}"
    )

    print(
        f"Status: "
        f"{campaign['campaign_status']}"
    )

    print("\n" + "=" * 70)

    print(
        "\n✅ Growth pipeline completed successfully."
    )

    print(
        "⏳ Campaign is waiting for merchant approval."
    )

    print("=" * 70)

    return {
        "status": "PIPELINE_COMPLETED",
        "opportunity": opportunity,
        "recommendation": recommendation,
        "campaign": campaign
    }


if __name__ == "__main__":

    result = run_growth_pipeline()

    if result["status"] == "PIPELINE_STOPPED":

        print("\n❌ Pipeline stopped.")

        print(
            f"Stage: {result['stage']}"
        )

        print(
            f"Reason: {result['reason']}"
        )