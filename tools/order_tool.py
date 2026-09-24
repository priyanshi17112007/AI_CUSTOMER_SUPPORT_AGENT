"""
tools/order_tool.py
===================
Tool 1: lookup_order(order_id)
Retrieves real-time order status, shipping carrier, ETA, delivery tracking,
and item details from the orders database.
"""

from typing import Dict, Any, Optional
from data.mock_data import get_order_by_id


def lookup_order(order_id: str) -> Dict[str, Any]:
    """
    Look up order details, status, delivery state, tracking number, and amount.
    
    Args:
        order_id: The unique identifier of the order (e.g., 'ORD1001', 'ORD1002').
        
    Returns:
        A dictionary containing order status, delivery tracking, items, and resolution hints.
    """
    if not order_id or not isinstance(order_id, str):
        return {
            "success": False,
            "error": "INVALID_INPUT",
            "message": "Order ID must be a non-empty string (e.g. 'ORD1001')."
        }
        
    clean_id = order_id.strip().upper()
    order = get_order_by_id(clean_id)
    
    if not order:
        return {
            "success": False,
            "error": "ORDER_NOT_FOUND",
            "order_id": clean_id,
            "message": f"No order found with ID '{clean_id}'. Please verify the order number."
        }
        
    return {
        "success": True,
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "customer_name": order["customer_name"],
        "item_name": order["item_name"],
        "quantity": order["quantity"],
        "amount": order["amount"],
        "currency": order["currency"],
        "order_date": order["order_date"],
        "status": order["status"],
        "delivery_status": order["delivery_status"],
        "carrier": order["carrier"],
        "tracking_number": order["tracking_number"],
        "original_eta": order["original_eta"],
        "revised_eta": order["revised_eta"],
        "delay_reason": order.get("delay_reason"),
        "delivery_address": order["delivery_address"],
        "delivered_date": order.get("delivered_date"),
        "is_returnable": order.get("is_returnable", False),
        "return_deadline": order.get("return_deadline")
    }
