"""
tools package initialization
============================
Re-exports all tools for ResolveAI Customer Support Agent.
Provides direct callable functions and optional CrewAI / LangChain wrappers.
"""

from typing import Dict, Any, Optional
from tools.order_tool import lookup_order
from tools.payment_tool import lookup_payment
from tools.return_tool import check_return_eligibility
from tools.ticket_tool import create_support_ticket
from tools.history_tool import get_customer_history

# Registry dictionary for programmatic tool dispatch
TOOL_REGISTRY = {
    "lookup_order": lookup_order,
    "lookup_payment": lookup_payment,
    "check_return_eligibility": check_return_eligibility,
    "create_support_ticket": create_support_ticket,
    "get_customer_history": get_customer_history,
}

__all__ = [
    "lookup_order",
    "lookup_payment",
    "check_return_eligibility",
    "create_support_ticket",
    "get_customer_history",
    "TOOL_REGISTRY",
]
