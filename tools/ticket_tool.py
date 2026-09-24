"""
tools/ticket_tool.py
====================
Tool 4: create_support_ticket(customer_issue, customer_id, priority, order_id)
Creates a formal support ticket when an issue cannot be resolved automatically,
or when human intervention / specialized escalation is required.
"""

from typing import Dict, Any, Optional
from data.mock_data import create_ticket_record, get_customer_by_id


def create_support_ticket(
    customer_issue: str,
    customer_id: str = "CUST-101",
    priority: str = "Medium",
    order_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new customer support ticket in the support queue.
    
    Args:
        customer_issue: Detailed summary of the customer's problem or request.
        customer_id: The ID of the customer (e.g. 'CUST-101', 'CUST-102').
        priority: Priority level ('Low', 'Medium', 'High', 'Urgent').
        order_id: Associated Order ID if applicable (e.g. 'ORD1001').
        
    Returns:
        A dictionary confirming ticket creation with tracking ID and SLA.
    """
    if not customer_issue or not isinstance(customer_issue, str) or not customer_issue.strip():
        return {
            "success": False,
            "error": "INVALID_INPUT",
            "message": "Customer issue description is required to open a support ticket."
        }
        
    clean_cust_id = (customer_id or "CUST-GUEST").strip().upper()
    clean_order_id = (order_id.strip().upper() if order_id and isinstance(order_id, str) and order_id.strip() != "" else None)
    
    # Classify category
    issue_lower = customer_issue.lower()
    if "payment" in issue_lower or "charge" in issue_lower or "card" in issue_lower:
        category = "Billing & Payments"
    elif "return" in issue_lower or "refund" in issue_lower or "damaged" in issue_lower or "wrong product" in issue_lower:
        category = "Returns & Exchanges"
    elif "delivery" in issue_lower or "shipping" in issue_lower or "delayed" in issue_lower or "lost" in issue_lower:
        category = "Logistics & Delivery"
    else:
        category = "Customer Care Escalation"
        
    # Auto-adjust priority if urgent terms present
    clean_priority = priority.title() if priority else "Medium"
    if any(k in issue_lower for k in ["urgent", "emergency", "stolen", "fraud", "unauthorized"]):
        clean_priority = "Urgent"
    elif any(k in issue_lower for k in ["damaged", "wrong product", "severe"]):
        if clean_priority == "Low":
            clean_priority = "Medium"
            
    ticket = create_ticket_record(
        customer_id=clean_cust_id,
        customer_issue=customer_issue,
        priority=clean_priority,
        order_id=clean_order_id,
        category=category
    )
    
    customer = get_customer_by_id(clean_cust_id)
    cust_name = customer["name"] if customer else "Valued Customer"
    
    return {
        "success": True,
        "ticket_id": ticket["ticket_id"],
        "customer_id": ticket["customer_id"],
        "customer_name": cust_name,
        "order_id": ticket["order_id"],
        "category": ticket["category"],
        "priority": ticket["priority"],
        "status": ticket["status"],
        "created_at": ticket["created_at"],
        "assigned_team": ticket["assigned_team"],
        "sla": "2-4 hours for initial agent response",
        "message": f"Support Ticket {ticket['ticket_id']} has been successfully created and escalated to {ticket['assigned_team']}."
    }
