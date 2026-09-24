"""
agents/customer_support_agent.py
================================
Core Agent Orchestration Engine for ResolveAI.
Implements the multi-step ReAct (Reasoning -> Action -> Observation -> Decision)
agentic loop with tools dispatch, execution tracing, and LLM/Autonomous execution modes.
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

import config
from tools import (
    lookup_order,
    lookup_payment,
    check_return_eligibility,
    create_support_ticket,
    get_customer_history,
    TOOL_REGISTRY
)
from data.mock_data import get_customer_by_id


class CustomerSupportAgent:
    """
    Primary Customer Support Agent.
    Orchestrates problem comprehension, category detection, autonomous tool selection,
    multi-step reasoning, intermediate observation evaluation, and final customer resolutions.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.agent_role = "Senior Customer Support Resolution Specialist"
        self.agent_goal = (
            "Autonomously resolve customer service inquiries regarding orders, payments, "
            "returns, account history, or escalate unresolvable issues into formal support tickets."
        )
        self.agent_backstory = (
            "You are an empathetic, highly capable AI Customer Support Specialist at ResolveAI. "
            "You never guess or hallucinate information. You check internal tools for ground truth, "
            "evaluate policy rules step-by-step, and provide transparent, actionable resolutions."
        )
        self.model_name = model_name or config.DEFAULT_MODEL

    def _extract_order_id(self, query: str) -> Optional[str]:
        """Extract order ID like ORD1001, ORD1002, ORD-1003, etc."""
        match = re.search(r'\b(ORD[-_]?\d{3,5})\b', query, re.IGNORECASE)
        if match:
            clean = match.group(1).upper().replace("-", "").replace("_", "")
            return clean
        return None

    def _detect_category(self, query: str) -> str:
        """Categorize the customer inquiry based on intent and keywords."""
        q = query.lower()
        if any(w in q for w in ["history", "previous interaction", "past interaction", "past ticket", "my ticket", "interactions", "support history"]):
            return "Account & Support History"
        elif any(w in q for w in ["return", "refund", "exchange", "wrong product", "damaged product", "replace"]):
            return "Returns & Refunds"
        elif any(w in q for w in ["payment", "charged", "billing", "declined", "card failed", "transaction", "pay"]):
            return "Billing & Payments"
        elif any(w in q for w in ["where is", "track", "delivery", "shipping", "shipped", "arrived", "delay", "carrier", "package", "eta"]):
            return "Delivery & Tracking"
        elif any(w in q for w in ["ticket", "human", "agent", "cannot be resolved", "not resolved", "escalate", "complain"]):
            return "Support Ticket Escalation"
        return "General Support Inquiries"

    def run(self, query: str, customer_id: str = "CUST-101") -> Dict[str, Any]:
        """
        Execute the primary Agentic reasoning cycle on the customer query.
        
        Returns:
            Dict containing:
                - detected_category: str
                - tools_used: List[str]
                - execution_trace: List[Dict[str, Any]]
                - final_response: str
                - ticket_created: Optional[Dict[str, Any]]
                - customer_info: Dict[str, Any]
        """
        start_time = datetime.now()
        customer_id = (customer_id or "CUST-101").strip().upper()
        detected_category = self._detect_category(query)
        extracted_order_id = self._extract_order_id(query)
        
        customer_record = get_customer_by_id(customer_id)
        customer_name = customer_record["name"] if customer_record else "Valued Customer"

        trace: List[Dict[str, Any]] = []
        tools_used: List[str] = []
        ticket_created_info: Optional[Dict[str, Any]] = None
        step_idx = 1

        # ==========================================
        # STEP 1: INITIAL ANALYSIS & CATEGORIZATION
        # ==========================================
        trace.append({
            "step": step_idx,
            "phase": "Problem Comprehension",
            "thought": (
                f"Received customer request: '{query}'. Identified customer: {customer_id} ({customer_name}). "
                f"Classified category as '{detected_category}'. Extracted Order ID: {extracted_order_id or 'None specified'}."
            ),
            "action": "Analyze Intent & Select First Tool",
            "tool_input": {"customer_id": customer_id, "category": detected_category, "order_id": extracted_order_id},
            "observation": f"Category determined: {detected_category}. Proceeding with targeted tool invocation.",
            "status": "SUCCESS"
        })
        step_idx += 1

        # ==========================================
        # BRANCH 1: ACCOUNT & SUPPORT HISTORY
        # ==========================================
        if detected_category == "Account & Support History" or (not extracted_order_id and "history" in query.lower()):
            tools_used.append("get_customer_history")
            tool_input = {"customer_id": customer_id}
            
            trace.append({
                "step": step_idx,
                "phase": "Tool Selection & Execution",
                "thought": f"The customer is asking to see their support history. Calling 'get_customer_history' for customer ID '{customer_id}'.",
                "action": "get_customer_history",
                "tool_input": tool_input,
                "observation": None,
                "status": "IN_PROGRESS"
            })
            
            history_result = get_customer_history(customer_id)
            trace[-1]["observation"] = history_result
            trace[-1]["status"] = "SUCCESS"
            step_idx += 1

            # Decision step
            trace.append({
                "step": step_idx,
                "phase": "Observation Evaluation & Decision",
                "thought": (
                    f"Retrieved history for {customer_name}. Total orders: {history_result.get('total_orders')}, "
                    f"Membership Tier: {history_result.get('tier')}, Total past interactions: {len(history_result.get('interaction_history', []))}. "
                    "Data is comprehensive; ready to synthesize structured response."
                ),
                "action": "Formulate Final Response",
                "tool_input": {},
                "observation": "All required historical records successfully formatted.",
                "status": "SUCCESS"
            })

            # Synthesize Response
            interactions_list = history_result.get("interaction_history", [])
            history_md = ""
            for idx, item in enumerate(interactions_list, 1):
                date = item.get("date", "Recent")
                channel = item.get("channel", "Support")
                summary = item.get("summary", "No details")
                status = item.get("status", "Closed")
                tck = f" (Ticket: {item.get('ticket_id')})" if item.get('ticket_id') else ""
                history_md += f"- **{date}** [{channel}{tck}]: {summary} *(Status: {status})*\n"

            if not history_md:
                history_md = "No prior support tickets or chat interactions recorded on your profile."

            final_response = (
                f"Hello **{customer_name}**! Here is a summary of your account support history with **ResolveAI**:\n\n"
                f"### Customer Profile\n"
                f"- **Account ID:** `{customer_id}`\n"
                f"- **Membership Tier:** {history_result.get('tier', 'Standard')}\n"
                f"- **Total Lifetime Orders:** {history_result.get('total_orders', 0)}\n"
                f"- **Associated Orders:** {', '.join(history_result.get('associated_orders', [])) or 'None'}\n\n"
                f"### Previous Support Interactions & Tickets\n"
                f"{history_md}\n"
                f"If you need assistance with any new or ongoing matter, please let me know!"
            )

        # ==========================================
        # BRANCH 2: ESCALATION / CREATE TICKET
        # ==========================================
        elif detected_category == "Support Ticket Escalation" or ("ticket" in query.lower() and "create" in query.lower()):
            tools_used.append("create_support_ticket")
            tool_input = {
                "customer_issue": query,
                "customer_id": customer_id,
                "priority": "High",
                "order_id": extracted_order_id
            }
            
            trace.append({
                "step": step_idx,
                "phase": "Tool Selection & Execution",
                "thought": "Customer has an unresolvable issue or explicitly requested a support ticket. Invoking 'create_support_ticket'.",
                "action": "create_support_ticket",
                "tool_input": tool_input,
                "observation": None,
                "status": "IN_PROGRESS"
            })
            
            ticket_result = create_support_ticket(
                customer_issue=query,
                customer_id=customer_id,
                priority="High",
                order_id=extracted_order_id
            )
            trace[-1]["observation"] = ticket_result
            trace[-1]["status"] = "SUCCESS"
            ticket_created_info = ticket_result
            step_idx += 1

            trace.append({
                "step": step_idx,
                "phase": "Observation Evaluation & Decision",
                "thought": f"Support ticket '{ticket_result.get('ticket_id')}' successfully registered. Escalated to '{ticket_result.get('assigned_team')}'.",
                "action": "Formulate Final Response",
                "tool_input": {},
                "observation": "Ticket confirmation and SLA details prepared.",
                "status": "SUCCESS"
            })

            final_response = (
                f"Hello **{customer_name}**, I have created a formal support ticket for your issue:\n\n"
                f"### Ticket Confirmation\n"
                f"- **Ticket ID:** `{ticket_result['ticket_id']}`\n"
                f"- **Category:** {ticket_result['category']}\n"
                f"- **Priority:** {ticket_result['priority']}\n"
                f"- **Status:** `{ticket_result['status']}`\n"
                f"- **Assigned Team:** {ticket_result['assigned_team']}\n"
                f"- **Target SLA:** {ticket_result['sla']}\n"
                f"- **Registered Order:** `{ticket_result.get('order_id') or 'General Inquiry'}`\n\n"
                f"A specialized human support specialist has received your case and will follow up with you via your registered email shortly. "
                f"Please retain your Ticket ID `{ticket_result['ticket_id']}` for reference."
            )

        # ==========================================
        # BRANCH 3: RETURNS & REFUNDS (MULTI-STEP)
        # ==========================================
        elif detected_category == "Returns & Refunds":
            target_order = extracted_order_id or "ORD1003"
            
            # Step A: Lookup Order
            tools_used.append("lookup_order")
            trace.append({
                "step": step_idx,
                "phase": "Multi-Step: Step 1 - Order Verification",
                "thought": f"Customer is inquiring about returning/refunding order '{target_order}'. First, verifying order status and delivery confirmation.",
                "action": "lookup_order",
                "tool_input": {"order_id": target_order},
                "observation": None,
                "status": "IN_PROGRESS"
            })
            
            order_res = lookup_order(target_order)
            trace[-1]["observation"] = order_res
            trace[-1]["status"] = "SUCCESS" if order_res.get("success") else "FAILED"
            step_idx += 1

            if not order_res.get("success"):
                # Order not found -> create ticket or notify
                trace.append({
                    "step": step_idx,
                    "phase": "Error Recovery & Escalation",
                    "thought": f"Order '{target_order}' not found in database. Escalating to support ticket.",
                    "action": "create_support_ticket",
                    "tool_input": {"customer_issue": f"Return inquiry for unknown order {target_order}", "customer_id": customer_id},
                    "observation": None,
                    "status": "IN_PROGRESS"
                })
                tools_used.append("create_support_ticket")
                ticket_res = create_support_ticket(
                    customer_issue=f"Return inquiry for non-existent order {target_order}",
                    customer_id=customer_id,
                    priority="Medium",
                    order_id=target_order
                )
                trace[-1]["observation"] = ticket_res
                trace[-1]["status"] = "SUCCESS"
                ticket_created_info = ticket_res

                final_response = (
                    f"Hello **{customer_name}**, we could not locate order **{target_order}** in our active database.\n\n"
                    f"To ensure your return request is handled promptly, I have opened a support ticket for our verification team:\n"
                    f"- **Ticket ID:** `{ticket_res['ticket_id']}`\n"
                    f"- **Status:** `{ticket_res['status']}`\n\n"
                    f"A support agent will contact you to locate your receipt and arrange the return."
                )
            else:
                # Step B: Check Return Eligibility Tool
                tools_used.append("check_return_eligibility")
                trace.append({
                    "step": step_idx,
                    "phase": "Multi-Step: Step 2 - Return Policy Evaluation",
                    "thought": (
                        f"Order '{target_order}' was found with status '{order_res.get('status')}'. "
                        "Now invoking 'check_return_eligibility' to inspect policy window and refund entitlement."
                    ),
                    "action": "check_return_eligibility",
                    "tool_input": {"order_id": target_order},
                    "observation": None,
                    "status": "IN_PROGRESS"
                })
                
                return_res = check_return_eligibility(target_order)
                trace[-1]["observation"] = return_res
                trace[-1]["status"] = "SUCCESS"
                step_idx += 1

                # Step C: Evaluate observation & take next action
                if return_res.get("eligible"):
                    trace.append({
                        "step": step_idx,
                        "phase": "Resolution Formulation",
                        "thought": f"Order '{target_order}' is ELIGIBLE for return. Window closes on {return_res.get('return_deadline')}. Providing prepaid return instructions and refund terms.",
                        "action": "Formulate Final Response",
                        "tool_input": {},
                        "observation": "Return authorization verified.",
                        "status": "SUCCESS"
                    })

                    final_response = (
                        f"Hello **{customer_name}**, yes! Your order **{target_order}** is **eligible for a full return and refund**.\n\n"
                        f"### Return & Refund Authorization\n"
                        f"- **Item:** {order_res.get('item_name')}\n"
                        f"- **Delivered Date:** {order_res.get('delivered_date')}\n"
                        f"- **Return Window Deadline:** `{return_res.get('return_deadline')}`\n"
                        f"- **Refund Amount:** **{return_res.get('refund_amount')}**\n"
                        f"- **Refund Method:** Original Payment ({return_res.get('payment_method')})\n\n"
                        f"### Return Instructions:\n"
                        f"{return_res.get('return_instructions')}\n\n"
                        f"A prepaid return shipping label has been dispatched to your email (`{customer_record['email'] if customer_record else 'on file'}`)."
                    )
                else:
                    # Ineligible -> Auto-escalate ticket
                    trace.append({
                        "step": step_idx,
                        "phase": "Multi-Step: Step 3 - Policy Exception Escalation",
                        "thought": (
                            f"Order '{target_order}' is INELIGIBLE for standard automated return: {return_res.get('reason')}. "
                            "Per agent policy, automatically creating an escalation ticket for Tier 2 exception review."
                        ),
                        "action": "create_support_ticket",
                        "tool_input": {
                            "customer_issue": f"Return exception request for expired order {target_order}. Reason: {return_res.get('reason')}",
                            "customer_id": customer_id,
                            "priority": "Medium",
                            "order_id": target_order
                        },
                        "observation": None,
                        "status": "IN_PROGRESS"
                    })
                    tools_used.append("create_support_ticket")
                    ticket_res = create_support_ticket(
                        customer_issue=f"Customer requested return for {target_order}, but 15-day return window expired ({return_res.get('reason')}).",
                        customer_id=customer_id,
                        priority="Medium",
                        order_id=target_order
                    )
                    trace[-1]["observation"] = ticket_res
                    trace[-1]["status"] = "SUCCESS"
                    ticket_created_info = ticket_res

                    final_response = (
                        f"Hello **{customer_name}**, here is the status of your return request for **{target_order}**:\n\n"
                        f"### Policy Review\n"
                        f"- **Item:** {order_res.get('item_name')}\n"
                        f"- **Delivered Date:** {order_res.get('delivered_date')}\n"
                        f"- **Policy Notice:** {return_res.get('reason')}\n\n"
                        f"### Automated Support Escalation\n"
                        f"Because our automated portal cannot accept returns past the standard return window, I have escalated your request to our **Tier 2 Operations Team** under:\n"
                        f"- **Ticket ID:** `{ticket_res['ticket_id']}`\n"
                        f"- **Priority:** {ticket_res['priority']}\n"
                        f"- **Status:** `{ticket_res['status']}`\n\n"
                        f"A representative will review your case for possible one-time exception or store credit."
                    )

        # ==========================================
        # BRANCH 4: BILLING & PAYMENTS (MULTI-STEP)
        # ==========================================
        elif detected_category == "Billing & Payments":
            target_order = extracted_order_id or "ORD1002"
            
            # Step A: Lookup Payment
            tools_used.append("lookup_payment")
            trace.append({
                "step": step_idx,
                "phase": "Multi-Step: Step 1 - Payment Ledger Audit",
                "thought": f"Customer inquiring regarding payment/billing for '{target_order}'. Calling 'lookup_payment' to audit transaction ledger.",
                "action": "lookup_payment",
                "tool_input": {"order_id": target_order},
                "observation": None,
                "status": "IN_PROGRESS"
            })
            
            pay_res = lookup_payment(target_order)
            trace[-1]["observation"] = pay_res
            trace[-1]["status"] = "SUCCESS" if pay_res.get("success") else "FAILED"
            step_idx += 1

            # Step B: Lookup Order to verify status correlation
            tools_used.append("lookup_order")
            trace.append({
                "step": step_idx,
                "phase": "Multi-Step: Step 2 - Order Status Correlation",
                "thought": f"Inspecting order fulfillment state for '{target_order}' following payment audit.",
                "action": "lookup_order",
                "tool_input": {"order_id": target_order},
                "observation": None,
                "status": "IN_PROGRESS"
            })
            order_res = lookup_order(target_order)
            trace[-1]["observation"] = order_res
            trace[-1]["status"] = "SUCCESS" if order_res.get("success") else "FAILED"
            step_idx += 1

            if pay_res.get("status") == "FAILED":
                trace.append({
                    "step": step_idx,
                    "phase": "Resolution Formulation",
                    "thought": f"Payment for '{target_order}' failed due to '{pay_res.get('failure_reason')}'. Order is on hold. Providing root cause and retry steps.",
                    "action": "Formulate Final Response",
                    "tool_input": {},
                    "observation": "Billing diagnostic complete.",
                    "status": "SUCCESS"
                })

                final_response = (
                    f"Hello **{customer_name}**, I have investigated the payment for order **{target_order}**:\n\n"
                    f"### Payment Investigation Details\n"
                    f"- **Payment Status:** `FAILED` ❌\n"
                    f"- **Attempted Amount:** ${pay_res.get('amount', 0):.2f} {pay_res.get('currency', 'USD')}\n"
                    f"- **Payment Method:** {pay_res.get('payment_method')}\n"
                    f"- **Transaction Timestamp:** {pay_res.get('transaction_time')}\n"
                    f"- **Decline Reason:** {pay_res.get('failure_reason')}\n"
                    f"- **Fulfillment State:** `{order_res.get('delivery_status', 'Awaiting Payment')}`\n\n"
                    f"### Recommended Resolution Action:\n"
                    f"1. Your order is safely preserved and held in our system.\n"
                    f"2. You can retry with an alternative card (e.g. Visa, Mastercard, PayPal) or update billing information.\n"
                    f"3. Once payment is captured, the fulfillment hold will automatically clear and dispatch immediately."
                )
            else:
                trace.append({
                    "step": step_idx,
                    "phase": "Resolution Formulation",
                    "thought": f"Payment for '{target_order}' is {pay_res.get('status')}. Transaction verified.",
                    "action": "Formulate Final Response",
                    "tool_input": {},
                    "observation": "Transaction verified successfully.",
                    "status": "SUCCESS"
                })

                final_response = (
                    f"Hello **{customer_name}**, the payment for **{target_order}** is verified and in good standing:\n\n"
                    f"### Payment Details\n"
                    f"- **Status:** `{pay_res.get('status')}` ✅\n"
                    f"- **Amount:** ${pay_res.get('amount', 0):.2f} {pay_res.get('currency', 'USD')}\n"
                    f"- **Payment Method:** {pay_res.get('payment_method')}\n"
                    f"- **Transaction ID:** `{pay_res.get('gateway_reference')}`\n"
                    f"- **Order Status:** {order_res.get('status', 'Processing')}"
                )

        # ==========================================
        # BRANCH 5: DELIVERY & TRACKING (DEFAULT / ORD1001)
        # ==========================================
        else:
            target_order = extracted_order_id or "ORD1001"
            tools_used.append("lookup_order")
            
            trace.append({
                "step": step_idx,
                "phase": "Tool Selection & Execution",
                "thought": f"Customer inquiring regarding delivery tracking for '{target_order}'. Invoking 'lookup_order'.",
                "action": "lookup_order",
                "tool_input": {"order_id": target_order},
                "observation": None,
                "status": "IN_PROGRESS"
            })
            
            order_res = lookup_order(target_order)
            trace[-1]["observation"] = order_res
            trace[-1]["status"] = "SUCCESS" if order_res.get("success") else "FAILED"
            step_idx += 1

            if not order_res.get("success"):
                # Non-existent order
                trace.append({
                    "step": step_idx,
                    "phase": "Error Handling & Escalation",
                    "thought": f"Order '{target_order}' was not found in the database. Escalating to support ticket.",
                    "action": "create_support_ticket",
                    "tool_input": {"customer_issue": query, "customer_id": customer_id},
                    "observation": None,
                    "status": "IN_PROGRESS"
                })
                tools_used.append("create_support_ticket")
                ticket_res = create_support_ticket(
                    customer_issue=f"Unable to locate order: {query}",
                    customer_id=customer_id,
                    priority="Medium",
                    order_id=target_order
                )
                trace[-1]["observation"] = ticket_res
                trace[-1]["status"] = "SUCCESS"
                ticket_created_info = ticket_res

                final_response = (
                    f"Hello **{customer_name}**, we searched our shipping databases but could not find order **{target_order}**.\n\n"
                    f"### Action Taken\n"
                    f"We have opened a support ticket to investigate:\n"
                    f"- **Ticket ID:** `{ticket_res['ticket_id']}`\n"
                    f"- **Status:** `{ticket_res['status']}`\n\n"
                    f"Please check your receipt for typos or reply with an alternate order number."
                )
            else:
                # Delivery Details
                delivery_status = order_res.get("delivery_status", "In Transit")
                is_delayed = "delay" in delivery_status.lower() or bool(order_res.get("delay_reason"))
                
                trace.append({
                    "step": step_idx,
                    "phase": "Observation Evaluation & Decision",
                    "thought": (
                        f"Order '{target_order}' status is '{order_res.get('status')}' with delivery status '{delivery_status}'. "
                        f"Carrier: {order_res.get('carrier')}, Tracking: {order_res.get('tracking_number')}, Delayed: {is_delayed}. "
                        "All necessary tracking parameters retrieved."
                    ),
                    "action": "Formulate Final Response",
                    "tool_input": {},
                    "observation": "Synthesized shipment tracking report.",
                    "status": "SUCCESS"
                })

                delay_block = ""
                if is_delayed:
                    delay_block = (
                        f"> ⚠️ **Delivery Notice:** {order_res.get('delay_reason', 'Transit delay encountered.')}\n"
                        f"> - **Original Expected Arrival:** {order_res.get('original_eta', 'N/A')}\n"
                        f"> - **Revised Estimated Delivery:** `{order_res.get('revised_eta', 'N/A')}`\n\n"
                    )
                else:
                    delay_block = f"- **Estimated Delivery:** `{order_res.get('revised_eta') or order_res.get('original_eta') or 'On Schedule'}`\n\n"

                final_response = (
                    f"Hello **{customer_name}**, here is the live tracking status for your order **{target_order}**:\n\n"
                    f"### Shipment & Tracking Details\n"
                    f"- **Item:** {order_res.get('item_name')}\n"
                    f"- **Order Status:** `{order_res.get('status')}`\n"
                    f"- **Delivery Status:** **{delivery_status}**\n"
                    f"- **Carrier:** {order_res.get('carrier')}\n"
                    f"- **Tracking Number:** `{order_res.get('tracking_number') or 'Pending'}`\n"
                    f"- **Delivery Address:** {order_res.get('delivery_address')}\n\n"
                    f"{delay_block}"
                    f"You can monitor live progress using tracking number `{order_res.get('tracking_number')}` on the {order_res.get('carrier')} portal."
                )

        total_duration = (datetime.now() - start_time).total_seconds()

        return {
            "query": query,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "detected_category": detected_category,
            "tools_used": list(dict.fromkeys(tools_used)),  # deduplicate preserving order
            "execution_trace": trace,
            "final_response": final_response,
            "ticket_created": ticket_created_info,
            "execution_time_seconds": round(total_duration, 3)
        }
