"""
app.py
======
Streamlit Web Dashboard for ResolveAI - Agentic Customer Support Resolution System.
Provides a visually interactive, professional agent interface showcasing autonomous
multi-step tool reasoning, execution traces, live database states, and ticket escalation.
"""

import os
import json
import time
import pandas as pd
import streamlit as st

import config
from agents.customer_support_agent import CustomerSupportAgent
from data.mock_data import (
    get_all_orders,
    get_all_payments,
    get_all_customers,
    get_all_tickets,
    reset_mock_data,
    get_customer_by_id
)

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="ResolveAI - Agentic Support System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS STYLING (Modern Glassmorphic Dark / Tech Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    /* Header Styling */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.98rem;
        margin-bottom: 14px;
    }

    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Architecture Workflow Banner */
    .workflow-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
    }

    .workflow-step {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #cbd5e1;
        background: rgba(30, 41, 59, 0.8);
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .workflow-arrow {
        color: #64748b;
        font-weight: 800;
    }

    /* Badges */
    .category-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 5px 14px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.3px;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.3);
    }

    .tool-tag {
        display: inline-block;
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.35);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    /* Response Container */
    .response-card {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 14px;
        padding: 24px;
        margin-top: 16px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    /* Ticket Card */
    .ticket-alert-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(185, 28, 28, 0.2) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 5px solid #ef4444;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 14px;
        margin-bottom: 18px;
    }

    /* Step Trace Cards */
    .trace-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid #818cf8;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    
    .trace-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
    }

    /* Quick Preset Buttons */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# INITIALIZE SESSION STATE
# ---------------------------------------------------------
if "agent_result" not in st.session_state:
    st.session_state.agent_result = None

if "query_input" not in st.session_state:
    st.session_state.query_input = "Where is my order ORD1001?"

if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = "CUST-101"

if "total_resolutions" not in st.session_state:
    st.session_state.total_resolutions = 0


# ---------------------------------------------------------
# SIDEBAR: CONFIGURATION & LIVE DATABASE INSPECTOR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    
    # Model Mode
    model_provider = st.selectbox(
        "Agent Reasoning Engine",
        [
            "Autonomous Deterministic ReAct (Fast & Reliable)",
            "Google Gemini (API Key required)",
            "OpenAI GPT-4o (API Key required)",
            "Groq Llama 3 (API Key required)"
        ],
        index=0,
        help="Select the inference orchestrator. Autonomous mode provides instant zero-latency deterministic reasoning."
    )
    
    if "Gemini" in model_provider:
        api_key_input = st.text_input("Gemini API Key", value=config.GEMINI_API_KEY or "", type="password")
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
            config.GEMINI_API_KEY = api_key_input
    elif "OpenAI" in model_provider:
        api_key_input = st.text_input("OpenAI API Key", value=config.OPENAI_API_KEY or "", type="password")
        if api_key_input:
            os.environ["OPENAI_API_KEY"] = api_key_input
            config.OPENAI_API_KEY = api_key_input
    elif "Groq" in model_provider:
        api_key_input = st.text_input("Groq API Key", value=config.GROQ_API_KEY or "", type="password")
        if api_key_input:
            os.environ["GROQ_API_KEY"] = api_key_input
            config.GROQ_API_KEY = api_key_input

    st.markdown("---")
    
    # Mock Database Live Inspector
    st.markdown("### 📊 In-Memory DB Inspector")
    st.caption("Live state of orders, payments, tickets, and customer records.")

    all_orders = get_all_orders()
    all_tickets = get_all_tickets()
    all_payments = get_all_payments()
    all_customers = get_all_customers()

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Total Orders", len(all_orders))
    metric_col2.metric("Open Tickets", len(all_tickets))

    with st.expander("📦 Orders Database", expanded=False):
        orders_df = pd.DataFrame([
            {
                "Order ID": o["order_id"],
                "Customer": o["customer_id"],
                "Item": o["item_name"][:20] + "...",
                "Status": o["status"],
                "Delivery": o["delivery_status"][:15] + ("..." if len(o["delivery_status"]) > 15 else "")
            }
            for o in all_orders.values()
        ])
        st.dataframe(orders_df, use_container_width=True, hide_index=True)

    with st.expander("💳 Payments Ledger", expanded=False):
        payments_df = pd.DataFrame([
            {
                "Order ID": p["order_id"],
                "Amount": f"${p['amount']}",
                "Status": p["status"],
                "Method": p["payment_method"][:18] + "..."
            }
            for p in all_payments.values()
        ])
        st.dataframe(payments_df, use_container_width=True, hide_index=True)

    with st.expander("🎫 Active Support Tickets", expanded=True):
        if all_tickets:
            tickets_df = pd.DataFrame([
                {
                    "Ticket ID": t["ticket_id"],
                    "Cust ID": t["customer_id"],
                    "Order": t.get("order_id") or "N/A",
                    "Priority": t["priority"],
                    "Status": t["status"]
                }
                for t in all_tickets
            ])
            st.dataframe(tickets_df, use_container_width=True, hide_index=True)
        else:
            st.info("No tickets created yet.")

    st.markdown("---")
    if st.button("🔄 Reset Database to Pristine State", use_container_width=True):
        reset_mock_data()
        st.session_state.agent_result = None
        st.toast("In-memory database successfully reset!", icon="✅")
        st.rerun()


# ---------------------------------------------------------
# HERO BANNER & ARCHITECTURE WORKFLOW
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
        <div>
            <div class="hero-title">ResolveAI</div>
            <div class="hero-subtitle">Autonomous Agentic Customer Support Resolution System (PS-08)</div>
        </div>
        <div>
            <span class="status-chip">● Agent Online & Ready</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Visual Workflow Diagram (Hackathon demonstration visual)
st.markdown("""
<div class="workflow-container">
    <div class="workflow-step">👤 Customer Query</div>
    <div class="workflow-arrow">➔</div>
    <div class="workflow-step">🧠 Intent & Category</div>
    <div class="workflow-arrow">➔</div>
    <div class="workflow-step">🛠️ Autonomous Tool Call</div>
    <div class="workflow-arrow">➔</div>
    <div class="workflow-step">🔍 Observation Check</div>
    <div class="workflow-arrow">➔</div>
    <div class="workflow-step">🔄 Next Action / Loop</div>
    <div class="workflow-arrow">➔</div>
    <div class="workflow-step">✨ Final Resolution / Ticket</div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# QUICK PRESET DEMO BUTTONS
# ---------------------------------------------------------
st.markdown("##### ⚡ Quick Hackathon Demo Queries")

preset_col1, preset_col2, preset_col3, preset_col4, preset_col5 = st.columns(5)

def set_query(q_text: str, cust_id: str):
    st.session_state.query_input = q_text
    st.session_state.selected_customer = cust_id

with preset_col1:
    if st.button("1. 📦 Where is ORD1001?", use_container_width=True, help="Test delivery delay tracking"):
        set_query("Where is my order ORD1001?", "CUST-101")
        st.rerun()

with preset_col2:
    if st.button("2. 💳 Payment Failed (ORD1002)", use_container_width=True, help="Test payment diagnosis"):
        set_query("My payment for ORD1002 failed.", "CUST-102")
        st.rerun()

with preset_col3:
    if st.button("3. 🔄 Return ORD1003", use_container_width=True, help="Test return eligibility & refund"):
        set_query("I received the wrong product for ORD1003. Can I return it?", "CUST-101")
        st.rerun()

with preset_col4:
    if st.button("4. 🎫 Escalate Ticket", use_container_width=True, help="Test support ticket creation"):
        set_query("My issue cannot be resolved. Please create a support ticket.", "CUST-102")
        st.rerun()

with preset_col5:
    if st.button("5. 📜 Past History", use_container_width=True, help="Test customer history retrieval"):
        set_query("Show me my previous support interactions.", "CUST-101")
        st.rerun()


# ---------------------------------------------------------
# QUERY INPUT FORM
# ---------------------------------------------------------
st.markdown("---")

with st.form(key="agent_query_form"):
    input_col1, input_col2 = st.columns([1, 3])
    
    with input_col1:
        customer_options = {
            "CUST-101": "CUST-101 (Alice Smith - VIP Gold)",
            "CUST-102": "CUST-102 (Bob Johnson - Standard)",
            "CUST-103": "CUST-103 (Carol Davis - Silver)"
        }
        selected_cust_key = st.selectbox(
            "Customer Identity",
            options=list(customer_options.keys()),
            format_func=lambda x: customer_options[x],
            index=list(customer_options.keys()).index(st.session_state.selected_customer) if st.session_state.selected_customer in customer_options else 0
        )
        
    with input_col2:
        user_query = st.text_input(
            "Customer Service Request",
            value=st.session_state.query_input,
            placeholder="e.g., Where is my order ORD1001? or Can I return ORD1003?"
        )
        
    submit_btn = st.form_submit_button("🚀 Run ResolveAI Agent", use_container_width=True, type="primary")

# Execute Agent
if submit_btn:
    if not user_query.strip():
        st.warning("Please enter a customer query to resolve.")
    else:
        st.session_state.selected_customer = selected_cust_key
        st.session_state.query_input = user_query
        
        with st.spinner("🤖 ResolveAI Agent is analyzing intent, querying tools, and orchestrating resolution..."):
            time.sleep(0.3)  # Smooth transition feel
            agent = CustomerSupportAgent()
            result = agent.run(query=user_query, customer_id=selected_cust_key)
            st.session_state.agent_result = result
            st.session_state.total_resolutions += 1


# ---------------------------------------------------------
# RESULTS DISPLAY: RESOLUTION + TRACE + METRICS
# ---------------------------------------------------------
res = st.session_state.agent_result

if res:
    st.markdown("### 🎯 Resolution Results")

    # Header Meta Pills
    meta_col1, meta_col2, meta_col3 = st.columns([2, 3, 2])
    
    with meta_col1:
        st.markdown(f"**Detected Category:**<br><span class='category-badge'>🏷️ {res['detected_category']}</span>", unsafe_allow_html=True)
        
    with meta_col2:
        tools_html = "".join([f"<span class='tool-tag'>⚙️ {t}()</span>" for t in res['tools_used']])
        st.markdown(f"**Tools Autonomous Invocation:**<br>{tools_html}", unsafe_allow_html=True)

    with meta_col3:
        st.markdown(f"**Execution Performance:**<br>⚡ `{res['execution_time_seconds']}s` across `{len(res['execution_trace'])}` reasoning steps", unsafe_allow_html=True)

    # Escalation Ticket Notice (If created)
    if res.get("ticket_created"):
        tck = res["ticket_created"]
        st.markdown(f"""
        <div class="ticket-alert-card">
            <div style="font-weight: 700; font-size: 1.05rem; color: #f87171; margin-bottom: 4px;">
                🚨 Support Ticket Created: {tck['ticket_id']}
            </div>
            <div style="font-size: 0.9rem; color: #cbd5e1;">
                <strong>Priority:</strong> {tck['priority']} &nbsp;|&nbsp; 
                <strong>Category:</strong> {tck['category']} &nbsp;|&nbsp; 
                <strong>Assigned Queue:</strong> {tck['assigned_team']} &nbsp;|&nbsp; 
                <strong>SLA:</strong> {tck['sla']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # AI Final Response Box
    st.markdown(f"""
    <div class="response-card">
        <div style="font-size: 0.85rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">
            🤖 Agent Final Resolution Response
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(res["final_response"])

    # ---------------------------------------------------------
    # AGENT REASONING & EXECUTION TRACE ACCORDION
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🔍 Live Agentic Reasoning & Execution Trace")
    st.caption("Inspect the multi-step ReAct (Thought ➔ Action ➔ Observation ➔ Decision) execution chain.")

    trace_steps = res.get("execution_trace", [])
    
    for idx, step in enumerate(trace_steps, 1):
        step_phase = step.get("phase", f"Step {idx}")
        status_icon = "✅" if step.get("status") == "SUCCESS" else "⏳"
        
        with st.expander(f"{status_icon} Step {idx}: {step_phase} — {step.get('action')}", expanded=True):
            st.markdown(f"**🧠 Agent Thought:**")
            st.info(step.get("thought"))
            
            trace_col1, trace_col2 = st.columns(2)
            with trace_col1:
                st.markdown(f"**🛠️ Action / Tool Selected:** `{step.get('action')}`")
                if step.get("tool_input"):
                    st.json(step.get("tool_input"))
            with trace_col2:
                st.markdown(f"**📋 Tool Observation / State Result:**")
                if isinstance(step.get("observation"), (dict, list)):
                    st.json(step.get("observation"))
                else:
                    st.code(str(step.get("observation") or "Pending..."), language="text")

# ---------------------------------------------------------
# FOOTER & DEMO HELPER
# ---------------------------------------------------------
st.markdown("---")
footer_col1, footer_col2 = st.columns([3, 1])
with footer_col1:
    st.caption("ResolveAI • Agentic Customer Support Resolution System • Problem Statement PS-08")
with footer_col2:
    st.caption("Built for Hackathon Demonstration")
