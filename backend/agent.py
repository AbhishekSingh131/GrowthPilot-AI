from datetime import datetime

from backend.analytics import generate_opportunities
from backend.database import get_connection
from backend.campaigns import create_campaign


def save_action(
    action_type,
    product_a=None,
    product_b=None,
    reason="",
    confidence=None,
    estimated_revenue=None,
    status="PROPOSED"
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO agent_actions
        (
            action_type,
            product_a,
            product_b,
            reason,
            confidence,
            estimated_revenue,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            action_type,
            product_a,
            product_b,
            reason,
            confidence,
            estimated_revenue,
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    connection.commit()
    connection.close()


def growth_agent():

    opportunities = generate_opportunities()

    print("\n🤖 GrowthPilot AI — Growth Agent\n")

    if not opportunities:
        print("No growth opportunities detected.")
        return

    for opportunity in opportunities:

        print("=" * 70)

        # Revenue Product Opportunity
        if opportunity["type"] == "revenue_product":

            product = opportunity["product"]
            revenue = opportunity["revenue"]

            action = "INCREASE_PROMOTION"

            reason = (
                f"{product} is currently the highest "
                "revenue-generating product."
            )

            print("🟢 OPPORTUNITY DETECTED")
            print(f"Product: {product}")
            print(f"Revenue: ₹{revenue:,.2f}")

            print("\n🤖 AGENT DECISION")
            print(f"Action: {action}")

            print("\n💡 REASON")
            print(reason)

            print("\n⚡ PROPOSED ACTION")
            print(
                f"Increase promotional visibility for {product}."
            )

            save_action(
                action_type=action,
                product_a=product,
                reason=reason,
                confidence=100,
                estimated_revenue=revenue,
                status="PROPOSED"
            )

        # Cross-Sell Opportunity
        elif opportunity["type"] == "cross_sell":

            product_a = opportunity["product_a"]
            product_b = opportunity["product_b"]

            confidence = opportunity["confidence"]
            estimated_revenue = opportunity[
                "estimated_opportunity"
            ]

            print("🟢 OPPORTUNITY DETECTED")

            print(
                f"Product Pair: "
                f"{product_a} → {product_b}"
            )

            print(
                f"Cross-sell rate: "
                f"{opportunity['cross_sell_rate']}%"
            )

            print(
                f"Estimated opportunity: "
                f"₹{estimated_revenue:,.2f}"
            )

            print(
                f"Confidence: "
                f"{confidence}%"
            )

            # High-confidence opportunity
            if confidence >= 70:

                action = "CREATE_BUNDLE"

                reason = (
                    "Strong purchasing relationship detected "
                    "between the two products."
                )

                proposed_action = (
                    f"Create a bundle containing "
                    f"{product_a} and {product_b}."
                )

                status = "PROPOSED"

                # Create campaign
                campaign_id = create_campaign(
                    campaign_type="CROSS_SELL",
                    name=f"{product_a} + {product_b} Bundle",
                    product_a=product_a,
                    product_b=product_b,
                    offer="10% bundle discount",
                    target_customers=opportunity["customers_a"],
                    expected_revenue=estimated_revenue,
                    status="DRAFT"
                )

                print("\n📢 CAMPAIGN CREATED")
                print(f"Campaign ID: {campaign_id}")
                print(
                    f"Campaign: "
                    f"{product_a} + {product_b} Bundle"
                )
                print("Offer: 10% bundle discount")
                print(
                    f"Target customers: "
                    f"{opportunity['customers_a']}"
                )
                print(
                    f"Expected revenue: "
                    f"₹{estimated_revenue:,.2f}"
                )
                print("Status: DRAFT")

            # Low-confidence opportunity
            else:

                action = "MONITOR"

                reason = (
                    "The purchasing relationship is not strong "
                    "enough for an immediate campaign."
                )

                proposed_action = (
                    "Continue monitoring customer "
                    "purchasing behavior."
                )

                status = "MONITORING"

            print("\n🤖 AGENT DECISION")
            print(f"Action: {action}")

            print("\n💡 REASON")
            print(reason)

            print("\n⚡ PROPOSED ACTION")
            print(proposed_action)

            save_action(
                action_type=action,
                product_a=product_a,
                product_b=product_b,
                reason=reason,
                confidence=confidence,
                estimated_revenue=estimated_revenue,
                status=status
            )


if __name__ == "__main__":
    growth_agent()