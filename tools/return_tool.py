"""
tools/return_tool.py
====================
Tool 3: check_return_eligibility(order_id)
Evaluates store return policies, delivery dates, and return windows
to verify whether an order qualifies for a return/refund.
"""

from typing import Dict, Any
from datetime import datetime
from data.mock_data import get_order_by_id, get_payment_by_order_id


def check_return_eligibility(order_id: str) -> Dict[str, Any]:
    """
    Check if an order is eligible for a return and refund based on delivery date,
    current order status, and category return policies.
    
    Args:
        order_id: The unique identifier of the order (e.g. 'ORD1003', 'ORD1004').
        
    Returns:
        A dictionary indicating eligibility, remaining window days, return instructions, or ineligibility rationale.
    """
    if not order_id or not isinstance(order_id, str):
        return {
            "success": False,
            "error": "INVALID_INPUT",
            "eligible": False,
            "message": "Order ID must be a valid string to check return eligibility."
        }
        
    clean_id = order_id.strip().upper()
    order = get_order_by_id(clean_id)
    
    if not order:
        return {
            "success": False,
            "error": "ORDER_NOT_FOUND",
            "order_id": clean_id,
            "eligible": False,
            "message": f"Order '{clean_id}' was not found in the database. Cannot evaluate return eligibility."
        }
        
    status = order.get("status", "")
    delivery_status = order.get("delivery_status", "")
    
    # Check if order is delivered
    if status != "Delivered" and delivery_status != "Delivered":
        return {
            "success": True,
            "order_id": clean_id,
            "eligible": False,
            "reason": f"Order status is currently '{status}' ({delivery_status}). Returns can only be initiated after delivery.",
            "action_required": "Please wait until the package is delivered before initiating a return request."
        }
        
    # Check return window
    delivered_date_str = order.get("delivered_date")
    is_returnable = order.get("is_returnable", False)
    return_deadline = order.get("return_deadline")
    
    payment = get_payment_by_order_id(clean_id)
    refund_amount = order.get("amount", 0.0)
    currency = order.get("currency", "USD")
    
    if is_returnable:
        return {
            "success": True,
            "order_id": clean_id,
            "item_name": order.get("item_name"),
            "eligible": True,
            "delivered_date": delivered_date_str,
            "return_deadline": return_deadline,
            "refund_amount": f"{currency} {refund_amount:.2f}",
            "payment_method": payment.get("payment_method") if payment else "Original Payment Method",
            "return_instructions": (
                "1. A prepaid return shipping label will be generated for your order. "
                "2. Repack the item in original packaging with all included accessories. "
                "3. Drop off at any authorized UPS/FedEx drop point. "
                f"4. Full refund of {currency} {refund_amount:.2f} will be released within 3-5 business days of receipt."
            ),
            "next_steps": "Customer may proceed with returning the item using the prepaid return label."
        }
    else:
        ineligibility_reason = order.get(
            "ineligibility_reason",
            "The 15-day return window for this order has expired."
        )
        return {
            "success": True,
            "order_id": clean_id,
            "item_name": order.get("item_name"),
            "eligible": False,
            "delivered_date": delivered_date_str,
            "return_deadline": return_deadline,
            "reason": ineligibility_reason,
            "next_steps": "If this was due to a damaged shipment or special warranty condition, support ticket escalation is required."
        }
