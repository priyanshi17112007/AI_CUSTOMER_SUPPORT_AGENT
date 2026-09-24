"""
data/mock_data.py
=================
In-memory mock database for ResolveAI Customer Support Resolution System.
Contains realistic, clearly fictional sample data for orders, payments,
customer accounts, and dynamic support tickets.
"""

import copy
from datetime import datetime
from typing import Dict, Any, List, Optional


# Fictional Orders Database
INITIAL_ORDERS: Dict[str, Dict[str, Any]] = {
    "ORD1001": {
        "order_id": "ORD1001",
        "customer_id": "CUST-101",
        "customer_name": "Alice Smith",
        "item_name": "Sony WH-1000XM5 Wireless Noise-Canceling Headphones",
        "category": "Electronics",
        "quantity": 1,
        "amount": 399.99,
        "currency": "USD",
        "order_date": "2026-09-18",
        "status": "Shipped",
        "delivery_status": "Delayed",
        "carrier": "FedEx Priority",
        "tracking_number": "FDX-982341123",
        "original_eta": "2026-09-22",
        "revised_eta": "2026-09-26",
        "delay_reason": "Severe weather disruption at regional sorting hub (Memphis, TN)",
        "delivery_address": "742 Evergreen Terrace, Springfield, OR",
        "delivered_date": None,
        "is_returnable": False,
    },
    "ORD1002": {
        "order_id": "ORD1002",
        "customer_id": "CUST-102",
        "customer_name": "Bob Johnson",
        "item_name": "Dell UltraSharp 27-inch 4K USB-C Hub Monitor",
        "category": "Computer Accessories",
        "quantity": 1,
        "amount": 589.50,
        "currency": "USD",
        "order_date": "2026-09-23",
        "status": "Payment Failed",
        "delivery_status": "On Hold - Awaiting Payment",
        "carrier": "Unassigned",
        "tracking_number": None,
        "original_eta": None,
        "revised_eta": None,
        "delay_reason": None,
        "delivery_address": "1204 Market Street, San Francisco, CA",
        "delivered_date": None,
        "is_returnable": False,
    },
    "ORD1003": {
        "order_id": "ORD1003",
        "customer_id": "CUST-101",
        "customer_name": "Alice Smith",
        "item_name": "Ergonomic Mechanical Keyboard (RGB Blue Switches)",
        "category": "Computer Accessories",
        "quantity": 1,
        "amount": 149.00,
        "currency": "USD",
        "order_date": "2026-09-15",
        "status": "Delivered",
        "delivery_status": "Delivered",
        "carrier": "UPS Ground",
        "tracking_number": "UPS-1Z9999999999",
        "original_eta": "2026-09-21",
        "revised_eta": "2026-09-21",
        "delay_reason": None,
        "delivery_address": "742 Evergreen Terrace, Springfield, OR",
        "delivered_date": "2026-09-21",
        "is_returnable": True,
        "return_window_days": 15,
        "return_deadline": "2026-10-06",
    },
    "ORD1004": {
        "order_id": "ORD1004",
        "customer_id": "CUST-103",
        "customer_name": "Carol Davis",
        "item_name": "Apple Watch Series 9 GPS 45mm",
        "category": "Wearables",
        "quantity": 1,
        "amount": 429.00,
        "currency": "USD",
        "order_date": "2026-07-10",
        "status": "Delivered",
        "delivery_status": "Delivered",
        "carrier": "FedEx Standard",
        "tracking_number": "FDX-774411990",
        "original_eta": "2026-07-15",
        "revised_eta": "2026-07-15",
        "delay_reason": None,
        "delivery_address": "550 Elm Street, Austin, TX",
        "delivered_date": "2026-07-15",
        "is_returnable": False,
        "return_window_days": 15,
        "return_deadline": "2026-07-30",
        "ineligibility_reason": "Return policy window expired (Delivered on 2026-07-15, deadline was 2026-07-30).",
    },
    "ORD1005": {
        "order_id": "ORD1005",
        "customer_id": "CUST-102",
        "customer_name": "Bob Johnson",
        "item_name": "Logitech MX Master 3S Wireless Mouse",
        "category": "Computer Accessories",
        "quantity": 1,
        "amount": 99.99,
        "currency": "USD",
        "order_date": "2026-09-22",
        "status": "Out for Delivery",
        "delivery_status": "Out for Delivery (Expected by 7:00 PM today)",
        "carrier": "DHL Express",
        "tracking_number": "DHL-55881234",
        "original_eta": "2026-09-24",
        "revised_eta": "2026-09-24",
        "delay_reason": None,
        "delivery_address": "1204 Market Street, San Francisco, CA",
        "delivered_date": None,
        "is_returnable": False,
    }
}

# Fictional Payments Ledger
INITIAL_PAYMENTS: Dict[str, Dict[str, Any]] = {
    "ORD1001": {
        "payment_id": "PAY-9011",
        "order_id": "ORD1001",
        "amount": 399.99,
        "currency": "USD",
        "status": "COMPLETED",
        "payment_method": "Visa credit card (ending in 4242)",
        "transaction_time": "2026-09-18 14:22:00",
        "gateway_reference": "txn_stripe_9011_live",
        "refund_status": "NONE",
        "failure_reason": None,
        "resolution_action": "Payment captured successfully. Order processed for dispatch."
    },
    "ORD1002": {
        "payment_id": "PAY-9012",
        "order_id": "ORD1002",
        "amount": 589.50,
        "currency": "USD",
        "status": "FAILED",
        "payment_method": "Mastercard debit card (ending in 8819)",
        "transaction_time": "2026-09-23 09:15:00",
        "gateway_reference": "txn_stripe_9012_err",
        "refund_status": "NOT_APPLICABLE",
        "failure_reason": "Declined by issuing bank: Insufficient funds (ERR_51_INSUFFICIENT_FUNDS)",
        "resolution_action": "Customer can retry payment with an alternate card or updated billing information via the checkout link."
    },
    "ORD1003": {
        "payment_id": "PAY-9013",
        "order_id": "ORD1003",
        "amount": 149.00,
        "currency": "USD",
        "status": "COMPLETED",
        "payment_method": "PayPal Account (alice.smith@example.com)",
        "transaction_time": "2026-09-15 11:05:00",
        "gateway_reference": "txn_pp_9013_live",
        "refund_status": "ELIGIBLE_PENDING_RETURN",
        "failure_reason": None,
        "resolution_action": "Full refund of $149.00 will be credited to original PayPal source within 3-5 business days upon item return receipt."
    },
    "ORD1004": {
        "payment_id": "PAY-9014",
        "order_id": "ORD1004",
        "amount": 429.00,
        "currency": "USD",
        "status": "COMPLETED",
        "payment_method": "Apple Pay (Mastercard ending in 1904)",
        "transaction_time": "2026-07-10 16:45:00",
        "gateway_reference": "txn_apple_9014_settled",
        "refund_status": "EXPIRED",
        "failure_reason": None,
        "resolution_action": "Standard refund window closed on 2026-07-30."
    },
    "ORD1005": {
        "payment_id": "PAY-9015",
        "order_id": "ORD1005",
        "amount": 99.99,
        "currency": "USD",
        "status": "COMPLETED",
        "payment_method": "Visa credit card (ending in 1122)",
        "transaction_time": "2026-09-22 18:30:00",
        "gateway_reference": "txn_stripe_9015_live",
        "refund_status": "NONE",
        "failure_reason": None,
        "resolution_action": "Payment captured successfully."
    }
}

# Fictional Customer Directory & Interaction History
INITIAL_CUSTOMERS: Dict[str, Dict[str, Any]] = {
    "CUST-101": {
        "customer_id": "CUST-101",
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "phone": "+1 (555) 234-5678",
        "tier": "VIP Gold Member",
        "member_since": "2024-03-15",
        "total_orders": 14,
        "associated_orders": ["ORD1001", "ORD1003"],
        "interaction_history": [
            {
                "interaction_id": "INT-8801",
                "date": "2026-08-10 10:30",
                "channel": "Live Chat",
                "agent": "ResolveAI Assistant",
                "summary": "Customer requested delivery address verification. Address confirmed as 742 Evergreen Terrace, Springfield, OR.",
                "status": "Resolved"
            },
            {
                "interaction_id": "INT-8942",
                "date": "2026-09-02 14:15",
                "channel": "Support Ticket",
                "ticket_id": "TCK-8012",
                "agent": "Hardware Support Desk",
                "summary": "Inquired regarding extended warranty documentation for prior electronics purchase. PDF certificate sent via email.",
                "status": "Closed"
            }
        ]
    },
    "CUST-102": {
        "customer_id": "CUST-102",
        "name": "Bob Johnson",
        "email": "bob.johnson@example.com",
        "phone": "+1 (555) 876-5432",
        "tier": "Standard Member",
        "member_since": "2025-01-20",
        "total_orders": 3,
        "associated_orders": ["ORD1002", "ORD1005"],
        "interaction_history": [
            {
                "interaction_id": "INT-7102",
                "date": "2026-09-10 16:45",
                "channel": "Live Chat",
                "agent": "ResolveAI Assistant",
                "summary": "Customer asked about promotional coupon code validity on electronics category. Verified coupon expired on Sept 1st.",
                "status": "Resolved"
            }
        ]
    },
    "CUST-103": {
        "customer_id": "CUST-103",
        "name": "Carol Davis",
        "email": "carol.davis@example.com",
        "phone": "+1 (555) 345-6789",
        "tier": "Silver Member",
        "member_since": "2024-11-05",
        "total_orders": 6,
        "associated_orders": ["ORD1004"],
        "interaction_history": [
            {
                "interaction_id": "INT-6029",
                "date": "2026-07-20 09:10",
                "channel": "Support Ticket",
                "ticket_id": "TCK-7721",
                "agent": "Logistics Dispatch",
                "summary": "Proof of delivery request for ORD1004. FedEx carrier signature proof provided to customer.",
                "status": "Closed"
            }
        ]
    }
}

# Dynamic In-Memory Support Tickets Store
INITIAL_TICKETS: List[Dict[str, Any]] = [
    {
        "ticket_id": "TCK-2026-001",
        "customer_id": "CUST-103",
        "order_id": "ORD1004",
        "issue_description": "Customer requested special exception for return outside 15-day window.",
        "priority": "Low",
        "status": "RESOLVED",
        "category": "Returns & Exceptions",
        "created_at": "2026-08-01 11:00:00",
        "assigned_team": "Tier 2 Customer Operations",
        "resolution_notes": "Exception denied as order was delivered >30 days ago. Offered $10 loyalty credit."
    }
]

# In-memory working copies
_orders_db = copy.deepcopy(INITIAL_ORDERS)
_payments_db = copy.deepcopy(INITIAL_PAYMENTS)
_customers_db = copy.deepcopy(INITIAL_CUSTOMERS)
_tickets_db = copy.deepcopy(INITIAL_TICKETS)
_ticket_counter = 100


def reset_mock_data():
    """Reset the mock database to its pristine initial state."""
    global _orders_db, _payments_db, _customers_db, _tickets_db, _ticket_counter
    _orders_db = copy.deepcopy(INITIAL_ORDERS)
    _payments_db = copy.deepcopy(INITIAL_PAYMENTS)
    _customers_db = copy.deepcopy(INITIAL_CUSTOMERS)
    _tickets_db = copy.deepcopy(INITIAL_TICKETS)
    _ticket_counter = 100


def get_all_orders() -> Dict[str, Dict[str, Any]]:
    """Retrieve all orders from the active database."""
    return _orders_db


def get_order_by_id(order_id: str) -> Optional[Dict[str, Any]]:
    """Lookup an order by its ID (case-insensitive)."""
    clean_id = (order_id or "").strip().upper()
    return _orders_db.get(clean_id)


def get_all_payments() -> Dict[str, Dict[str, Any]]:
    """Retrieve all payment records."""
    return _payments_db


def get_payment_by_order_id(order_id: str) -> Optional[Dict[str, Any]]:
    """Lookup payment record by order ID (case-insensitive)."""
    clean_id = (order_id or "").strip().upper()
    return _payments_db.get(clean_id)


def get_customer_by_id(customer_id: str) -> Optional[Dict[str, Any]]:
    """Lookup customer profile and interactions by customer ID."""
    clean_id = (customer_id or "").strip().upper()
    return _customers_db.get(clean_id)


def get_all_customers() -> Dict[str, Dict[str, Any]]:
    """Retrieve all customer records."""
    return _customers_db


def get_all_tickets() -> List[Dict[str, Any]]:
    """Retrieve all support tickets created so far."""
    return _tickets_db


def create_ticket_record(
    customer_id: str,
    customer_issue: str,
    priority: str = "Medium",
    order_id: Optional[str] = None,
    category: str = "General Support"
) -> Dict[str, Any]:
    """Create a new support ticket and record it in the dynamic tickets store and customer history."""
    global _ticket_counter
    _ticket_counter += 1
    clean_cust_id = (customer_id or "CUST-GUEST").strip().upper()
    clean_order_id = (order_id or "N/A").strip().upper()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket_id = f"TCK-2026-{_ticket_counter:03d}"
    
    ticket_entry = {
        "ticket_id": ticket_id,
        "customer_id": clean_cust_id,
        "order_id": clean_order_id if clean_order_id != "N/A" else None,
        "issue_description": customer_issue.strip(),
        "priority": priority.title() if priority else "Medium",
        "status": "OPEN",
        "category": category,
        "created_at": timestamp,
        "assigned_team": "Human Support Escalations & Tier 2 Resolution",
        "resolution_notes": "Ticket routed to specialist queue. Response SLA within 2 hours."
    }
    
    _tickets_db.insert(0, ticket_entry)
    
    # Append to customer's interaction history if customer exists
    if clean_cust_id in _customers_db:
        _customers_db[clean_cust_id]["interaction_history"].insert(0, {
            "interaction_id": f"INT-AUTO-{_ticket_counter}",
            "date": timestamp,
            "channel": "Agent Escalation",
            "ticket_id": ticket_id,
            "agent": "ResolveAI Agentic Resolution System",
            "summary": f"Automated ticket created: {customer_issue.strip()[:100]}",
            "status": "Open"
        })
        
    return ticket_entry
