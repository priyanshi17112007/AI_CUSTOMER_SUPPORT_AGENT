# 🤖 ResolveAI — Agentic Customer Support Resolution System

<div align="center">

### 🚀 Domain Verse 1.0 | Agentic AI Hackathon Project

An autonomous AI customer support system that understands customer issues, selects the appropriate tools, performs multi-step reasoning, and resolves service requests intelligently using **CrewAI** and **Streamlit**.

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/CrewAI-Agentic%20AI-7C3AED?style=for-the-badge" />
<img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-16A34A?style=for-the-badge" />

</div>

---

## ✨ Project Overview

**ResolveAI** is a **Single-Agent Agentic AI** application built to automate customer support workflows.

Unlike traditional chatbots, ResolveAI reasons before responding. It autonomously identifies customer intent, selects the appropriate tool, evaluates results, and decides whether additional actions are required before delivering a final resolution.

### 🎯 Core Capabilities

- 🧠 Understand customer intent
- 🏷️ Classify issue category
- ⚙️ Dynamic tool selection
- 📦 Order & delivery verification
- 💳 Payment status checking
- 🔄 Return eligibility validation
- 🎫 Automatic support ticket creation
- 📜 Previous interaction history
- 📊 Explainable execution trace

---

## 🏗️ Agentic Workflow

```text
Customer Request
        │
        ▼
 Understand Intent
        │
        ▼
 Issue Classification
        │
        ▼
 Dynamic Tool Selection
        │
        ▼
   Tool Execution
        │
        ▼
 Observation / Result
        │
        ▼
 Need Another Action?
   ├── Yes → Execute Next Tool
   └── No
        │
        ▼
 Final Resolution / Ticket
```

---

## 🚀 Key Features

- **Autonomous Customer Support Agent** using CrewAI
- **Multi-step reasoning** instead of fixed chatbot responses
- **Dynamic enterprise tool calling**
- **Interactive Streamlit dashboard**
- **Visible AI execution timeline**
- **Prompt Injection & Jailbreak Guardrails**
- **Mock CRM, Orders, Payments & Returns System**
- **Secure API key management with `.env`**

---

## 🛠️ Tech Stack

<div align="center">

### Languages & Frameworks

<img src="https://skillicons.dev/icons?i=python,streamlit,git,github,vscode" />

### AI Stack

<img src="https://img.shields.io/badge/CrewAI-Agentic%20Framework-7C3AED?style=for-the-badge" />
<img src="https://img.shields.io/badge/Groq-LLM-0F172A?style=for-the-badge" />
<img src="https://img.shields.io/badge/Python%20Dotenv-Environment-16A34A?style=for-the-badge" />
<img src="https://img.shields.io/badge/Pandas-Mock%20Data-150458?style=for-the-badge&logo=pandas&logoColor=white" />

</div>

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Backend Development |
| CrewAI | Agent Orchestration |
| Streamlit | Interactive Dashboard |
| Groq LLM | Language Model |
| Pandas | Mock Data |
| Python Dotenv | Secure Environment Variables |

---

## 📁 Project Structure

```text
AI_CUSTOMER_SUPPORT_AGENT/
│
├── agents/
│   └── customer_support_agent.py
│
├── data/
│   └── mock_data.py
│
├── tools/
│   ├── order_tool.py
│   ├── payment_tool.py
│   ├── return_tool.py
│   ├── ticket_tool.py
│   ├── history_tool.py
│   └── trace.py
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 💡 Demo Queries

| Customer Query | Expected Action |
|---------------|----------------|
| Where is my order **ORD1001**? | Order Lookup |
| My payment for **ORD1002** failed. | Payment Verification |
| I received the wrong product for **ORD1003**. | Return Eligibility |
| Please create a support ticket. | Ticket Creation |
| Show my previous support interactions. | History Retrieval |

---

## 📦 Mock Dataset

| Order ID | Scenario |
|----------|----------|
| ORD1001 | 🚚 Delivery Delayed |
| ORD1002 | 💳 Payment Failed |
| ORD1003 | 🔄 Return Eligible |
| ORD1004 | ⏳ Return Window Expired |

> **Note:** All customer records and orders are fictional and used only for demonstration purposes.

---

## 🔒 Security Features

- ✅ Environment variables using `.env`
- 🔐 No hardcoded API keys
- 🛡️ Prompt Injection Protection
- 🚫 Jailbreak Detection
- ⚙️ Tool Permission Control
- 📋 Structured Error Handling
- 🧾 Execution Logging
- 🔍 Explainable AI Decisions

---

## ▶️ Installation

```bash
# Clone Repository
git clone https://github.com/priyanshi17112007/AI_CUSTOMER_SUPPORT_AGENT.git

# Enter Project
cd AI_CUSTOMER_SUPPORT_AGENT

# Create Virtual Environment
py -3.11 -m venv .venv

# Activate Environment
.\.venv\Scripts\Activate

# Install Dependencies
pip install -r requirements.txt

# Run Application
streamlit run app.py
```

---

## 🎯 Innovation

ResolveAI is **not a simple chatbot**.

Its core innovation is an **Agentic Decision Engine** that autonomously:

- Understands customer objectives
- Selects only the required tools
- Performs multi-step reasoning
- Makes explainable decisions
- Escalates unresolved issues intelligently

This transforms customer support from conversational AI into **autonomous problem resolution**.

---

## 🌱 Future Scope

- 🌍 Multilingual Support
- 🎙️ Voice Customer Assistant
- 💬 WhatsApp & Email Integration
- 🏢 CRM / ERP Connectivity
- 📊 Analytics Dashboard
- 😊 Customer Sentiment Analysis

---

## 📜 License

This project is developed for **educational and hackathon purposes** under **Domain Verse 1.0**.

---

<div align="center">

## 👩‍💻 Author

### **Priyanshi Sharma**

**🤖 Agentic AI Intern | 🐍 Python Developer**

Passionate about **Artificial Intelligence, Agentic AI & Intelligent Automation**

⭐ **If you like this project, don't forget to Star the repository!**

</div>
