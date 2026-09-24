"""
data package initialization
"""
from data.mock_data import (
    get_all_orders,
    get_order_by_id,
    get_all_payments,
    get_payment_by_order_id,
    get_all_customers,
    get_customer_by_id,
    get_all_tickets,
    create_ticket_record,
    reset_mock_data
)

__all__ = [
    "get_all_orders",
    "get_order_by_id",
    "get_all_payments",
    "get_payment_by_order_id",
    "get_all_customers",
    "get_customer_by_id",
    "get_all_tickets",
    "create_ticket_record",
    "reset_mock_data"
]
