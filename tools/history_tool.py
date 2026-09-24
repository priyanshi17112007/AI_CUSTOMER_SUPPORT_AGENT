"""
tools/history_tool.py
=====================
Tool 5: get_customer_history(customer_id)
Retrieves previous support interactions, open/closed tickets, customer profile,
and associated orders to maintain continuity across customer touchpoints.
"""

from typing import Dict, Any
from data.mock_data import get_customer_by_id, get_all_tickets


def get_customer_history(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve customer profile, interaction history, previous tickets, and account tier.
    
    Args:
        customer_id: The unique customer identifier (e.g., 'CUST-101', 'CUST-102').
        
    Returns:
        A dictionary containing the customer's full profile and past interaction timeline.
    """
    if not customer_id or not isinstance(customer_id, str):
        return {
            "success": False,
            "error": "INVALID_INPUT",
            "message": "Customer ID must be a non-empty string (e.g. 'CUST-101')."
        }
        
    clean_id = customer_id.strip().upper()
    customer = get_customer_by_id(clean_id)
    
    if not customer:
        return {
            "success": False,
            "error": "CUSTOMER_NOT_FOUND",
            "customer_id": clean_id,
            "message": f"No customer record found for ID '{clean_id}'. Verify customer ID."
        }
        
    # Also fetch all dynamic tickets associated with this customer
    all_tickets = get_all_tickets()
    customer_tickets = [t for t in all_tickets if t.get("customer_id") == clean_id]
    
    return {
        "success": True,
        "customer_id": customer["customer_id"],
        "name": customer["name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "tier": customer["tier"],
        "member_since": customer["member_since"],
        "total_orders": customer["total_orders"],
        "associated_orders": customer["associated_orders"],
        "interaction_history": customer["interaction_history"],
        "active_tickets_count": len([t for t in customer_tickets if t.get("status") == "OPEN"]),
        "total_tickets_count": len(customer_tickets),
        "recent_tickets": customer_tickets[:3]
    }
