from datetime import datetime

from backend.database import get_connection


def create_campaign(
    campaign_type,
    name,
    product_a=None,
    product_b=None,
    offer=None,
    target_customers=0,
    expected_revenue=0,
    status="DRAFT"
):
    connection = get_connection()
    cursor = connection.cursor()

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
            campaign_type,
            name,
            product_a,
            product_b,
            offer,
            target_customers,
            status,
            expected_revenue,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    campaign_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return campaign_id


def get_campaigns():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM campaigns
        ORDER BY id DESC
    """)

    campaigns = cursor.fetchall()
    connection.close()

    return [dict(campaign) for campaign in campaigns]


if __name__ == "__main__":
    campaigns = get_campaigns()

    print("\n📢 GrowthPilot AI — Campaigns\n")

    if not campaigns:
        print("No campaigns created yet.")

    for campaign in campaigns:
        print("=" * 70)
        print(f"Campaign ID: {campaign['id']}")
        print(f"Type: {campaign['campaign_type']}")
        print(f"Name: {campaign['name']}")
        print(f"Products: {campaign['product_a']} → {campaign['product_b']}")
        print(f"Offer: {campaign['offer']}")
        print(f"Target customers: {campaign['target_customers']}")
        print(f"Expected revenue: ₹{campaign['expected_revenue']:,.2f}")
        print(f"Status: {campaign['status']}")