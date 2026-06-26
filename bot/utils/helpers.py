from datetime import datetime


def format_price(amount: int) -> str:
    return f"{amount:,}".replace(",", " ")


def format_date(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return dt_str


ORDER_STATUS_MAP = {
    "pending":    ("order_status_pending",    "🕐"),
    "paid":       ("order_status_paid",       "✅"),
    "processing": ("order_status_processing", "⚙️"),
    "completed":  ("order_status_completed",  "📦"),
    "cancelled":  ("order_status_cancelled",  "❌"),
}

PAYMENT_DETAILS = {
    "click":  "9860 0601 2345 6789 (Click)",
    "payme":  "9860 0501 9876 5432 (Payme)",
    "uzcard": "8600 1234 5678 9012 (Uzcard — Alisher K.)",
    "humo":   "9860 2200 1111 2222 (Humo — Alisher K.)",
    "crypto": "TRC20: TXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
}
