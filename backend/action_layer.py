from datetime import datetime

from backend.database import get_connection


def get_campaign(campaign_id):

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
        return None

    return dict(campaign)


def approve_campaign(campaign_id):

    campaign = get_campaign(campaign_id)

    if not campaign:
        return {
            "status": "ERROR",
            "message": f"Campaign #{campaign_id} not found."
        }

    if campaign["status"] != "PENDING_APPROVAL":
        return {
            "status": "ERROR",
            "message": (
                f"Campaign #{campaign_id} cannot be approved. "
                f"Current status: {campaign['status']}"
            )
        }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE campaigns
        SET status = ?
        WHERE id = ?
        """,
        ("APPROVED", campaign_id)
    )

    connection.commit()
    connection.close()

    return {
        "status": "APPROVED",
        "campaign_id": campaign_id,
        "message": (
            f"Campaign #{campaign_id} has been approved "
            f"by the merchant."
        ),
        "next_action": "READY_FOR_EXECUTION",
        "approved_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


def reject_campaign(campaign_id):

    campaign = get_campaign(campaign_id)

    if not campaign:
        return {
            "status": "ERROR",
            "message": f"Campaign #{campaign_id} not found."
        }

    if campaign["status"] != "PENDING_APPROVAL":
        return {
            "status": "ERROR",
            "message": (
                f"Campaign #{campaign_id} cannot be rejected. "
                f"Current status: {campaign['status']}"
            )
        }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE campaigns
        SET status = ?
        WHERE id = ?
        """,
        ("REJECTED", campaign_id)
    )

    connection.commit()
    connection.close()

    return {
        "status": "REJECTED",
        "campaign_id": campaign_id,
        "message": (
            f"Campaign #{campaign_id} has been rejected "
            f"by the merchant."
        )
    }


if __name__ == "__main__":

    campaign_id = 3

    print("\n🛡️ GrowthPilot AI — Merchant Action Layer\n")

    campaign = get_campaign(campaign_id)

    if not campaign:
        print(f"❌ Campaign #{campaign_id} not found.")

    else:

        print("=" * 70)

        print(
            f"Campaign #{campaign['id']}"
        )

        print(
            f"Name: {campaign['name']}"
        )

        print(
            f"Offer: {campaign['offer']}"
        )

        print(
            f"Target customers: "
            f"{campaign['target_customers']}"
        )

        print(
            f"Current status: "
            f"{campaign['status']}"
        )

        print("=" * 70)

        if campaign["status"] == "PENDING_APPROVAL":

            print("\n👤 Merchant approval required.")

            result = approve_campaign(campaign_id)

            print(
                f"\n✅ {result['message']}"
            )

            print(
                f"Next action: "
                f"{result['next_action']}"
            )

        else:

            print(
                "\n⚠️ Campaign is not waiting for approval."
            )