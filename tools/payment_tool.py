"""
tools/payment_tool.py
=====================
Tool 2: lookup_payment(order_id)
Retrieves transaction records, payment gateway status, payment methods,
failure reasons, and refund eligibility from the billing ledger.
"""

from typing import Dict, Any
from data.mock_data import get_payment_by_order_id, get_order_by_id


def lookup_payment(order_id: str) -> Dict[str, Any]:
    """
    Look up payment status, payment method, gateway transaction reference,
    failure reasons, and refund status for a specific order.
    
    Args:
        order_id: The order ID associated with the payment (e.g. 'ORD1001', 'ORD1002').
        
    Returns:
        A dictionary with detailed transaction status and resolution guidance.
    """
    if not order_id or not isinstance(order_id, str):
        return {
            "success": False,
            "error": "INVALID_INPUT",
            "message": "Order ID must be provided as a non-empty string."
        }
        
    clean_id = order_id.strip().upper()
    payment = get_payment_by_order_id(clean_id)
    
    if not payment:
        # Check if the order itself exists
        order = get_order_by_id(clean_id)
        if not order:
            return {
                "success": False,
                "error": "ORDER_NOT_FOUND",
                "order_id": clean_id,
                "message": f"Cannot find payment record because order '{clean_id}' does not exist."
            }
        return {
            "success": False,
            "error": "PAYMENT_NOT_FOUND",
            "order_id": clean_id,
            "message": f"No payment record initiated for order '{clean_id}'."
        }
        
    return {
        "success": True,
        "payment_id": payment["payment_id"],
        "order_id": payment["order_id"],
        "amount": payment["amount"],
        "currency": payment["currency"],
        "status": payment["status"],
        "payment_method": payment["payment_method"],
        "transaction_time": payment["transaction_time"],
        "gateway_reference": payment["gateway_reference"],
        "refund_status": payment.get("refund_status", "NONE"),
        "failure_reason": payment.get("failure_reason"),
        "resolution_action": payment.get("resolution_action"),
        "retry_allowed": payment.get("retry_allowed", False)
    }
