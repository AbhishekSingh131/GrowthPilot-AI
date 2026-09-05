import os

import razorpay
from dotenv import load_dotenv


load_dotenv()


RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise RuntimeError(
        "Razorpay test API credentials are missing from .env"
    )


client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_KEY_SECRET
    )
)


def create_razorpay_order(amount, receipt, notes=None):

    order_data = {
        "amount": int(amount * 100),
        "currency": "INR",
        "receipt": receipt
    }

    if notes:
        order_data["notes"] = notes

    order = client.order.create(
        data=order_data
    )

    return order