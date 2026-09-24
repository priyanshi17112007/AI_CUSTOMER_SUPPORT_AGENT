"""
tests/test_agent.py
===================
Automated Test Suite for ResolveAI Customer Support Resolution Agent.
Tests individual tools, error conditions, and end-to-end multi-step agent queries.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools import (
    lookup_order,
    lookup_payment,
    check_return_eligibility,
    create_support_ticket,
    get_customer_history
)
from agents import CustomerSupportAgent
from data.mock_data import reset_mock_data, get_all_tickets


def test_lookup_order():
    print("\n--- Testing lookup_order ---")
    # Valid existing order
    res1 = lookup_order("ORD1001")
    assert res1["success"] is True
    assert res1["delivery_status"] == "Delayed"
    print("  [PASS] Valid order lookup (ORD1001) passed.")

    # Non-existent order
    res2 = lookup_order("ORD9999")
    assert res2["success"] is False
    assert res2["error"] == "ORDER_NOT_FOUND"
    print("  [PASS] Invalid order lookup handling passed.")


def test_lookup_payment():
    print("\n--- Testing lookup_payment ---")
    # Failed payment
    res1 = lookup_payment("ORD1002")
    assert res1["success"] is True
    assert res1["status"] == "FAILED"
    print("  [PASS] Failed payment lookup (ORD1002) passed.")

    # Successful payment
    res2 = lookup_payment("ORD1001")
    assert res2["success"] is True
    assert res2["status"] == "COMPLETED"
    print("  [PASS] Completed payment lookup (ORD1001) passed.")


def test_return_eligibility():
    print("\n--- Testing check_return_eligibility ---")
    # Eligible return
    res1 = check_return_eligibility("ORD1003")
    assert res1["success"] is True
    assert res1["eligible"] is True
    print("  [PASS] Return eligible check (ORD1003) passed.")

    # Expired return window
    res2 = check_return_eligibility("ORD1004")
    assert res2["success"] is True
    assert res2["eligible"] is False
    print("  [PASS] Expired return window check (ORD1004) passed.")


def test_ticket_creation():
    print("\n--- Testing create_support_ticket ---")
    res = create_support_ticket(
        customer_issue="Customer received damaged item",
        customer_id="CUST-101",
        priority="High",
        order_id="ORD1001"
    )
    assert res["success"] is True
    assert "TCK-" in res["ticket_id"]
    assert res["status"] == "OPEN"
    print(f"  [PASS] Ticket creation passed: {res['ticket_id']}")


def test_customer_history():
    print("\n--- Testing get_customer_history ---")
    res = get_customer_history("CUST-101")
    assert res["success"] is True
    assert res["name"] == "Alice Smith"
    assert len(res["interaction_history"]) > 0
    print(f"  [PASS] Customer history passed for {res['name']}.")


def test_end_to_end_agent_queries():
    print("\n==========================================")
    print("TESTING END-TO-END AGENT QUERIES")
    print("==========================================")
    agent = CustomerSupportAgent()

    test_queries = [
        ("Where is my order ORD1001?", "CUST-101", "Delivery & Tracking", ["lookup_order"]),
        ("My payment for ORD1002 failed.", "CUST-102", "Billing & Payments", ["lookup_payment", "lookup_order"]),
        ("I received the wrong product for ORD1003. Can I return it?", "CUST-101", "Returns & Refunds", ["lookup_order", "check_return_eligibility"]),
        ("My issue cannot be resolved. Please create a support ticket.", "CUST-102", "Support Ticket Escalation", ["create_support_ticket"]),
        ("Show me my previous support interactions.", "CUST-101", "Account & Support History", ["get_customer_history"])
    ]

    for idx, (query, cust_id, expected_cat, expected_tools) in enumerate(test_queries, 1):
        print(f"\n[Test Case {idx}] Query: '{query}'")
        result = agent.run(query=query, customer_id=cust_id)
        
        print(f"  Category Detected : {result['detected_category']}")
        print(f"  Tools Invoked     : {result['tools_used']}")
        print(f"  Trace Steps       : {len(result['execution_trace'])} steps")
        print(f"  Execution Time    : {result['execution_time_seconds']}s")
        assert result["detected_category"] == expected_cat
        for tool in expected_tools:
            assert tool in result["tools_used"], f"Expected {tool} in {result['tools_used']}"
        print(f"  [PASS] Test Case {idx} PASSED!")

    print("\n[SUCCESS] ALL 5 END-TO-END AGENT DEMO TESTS PASSED SUCCESSFULLY!\n")


if __name__ == "__main__":
    reset_mock_data()
    test_lookup_order()
    test_lookup_payment()
    test_return_eligibility()
    test_ticket_creation()
    test_customer_history()
    test_end_to_end_agent_queries()
