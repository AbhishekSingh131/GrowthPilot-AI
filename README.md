🚀 GrowthPilot AI — AI Revenue Copilot for Merchant Growth

GrowthPilot AI is an AI-powered merchant growth and revenue optimization system that helps merchants identify revenue opportunities, create targeted campaigns, execute approved actions, and measure business impact.

“I didn't build a chatbot. I built an AI growth system that can measurably increase merchant revenue.”
🎯 What It Does

GrowthPilot AI follows an agentic growth loop:

AI Observes → Decides → Acts → Measures

The system analyzes merchant transaction and customer data to identify opportunities such as:

Cross-selling and upselling
Product recommendations
Customer segmentation
Targeted growth campaigns
Campaign performance optimization
Incremental revenue measurement
ROI-based campaign decisions
🧠 AI Agents
Growth Analyst Agent

Identifies high-value growth opportunities from merchant data.

Recommendation Agent

Generates personalized product recommendations and offers.

Campaign Agent

Creates targeted campaigns based on identified opportunities.

Action & Approval Layer

Ensures merchant approval before executing growth actions.

Execution Agent

Executes approved campaigns and records campaign outcomes.

Measurement Agent

Measures conversions, incremental revenue, campaign cost, ROI, and provides an optimization decision.

🏗️ Architecture
Merchant Data
     ↓
Data & Analytics Layer
     ↓
AI Growth Orchestrator
     ↓
Growth Analyst
     ↓
Recommendation Agent
     ↓
Campaign Agent
     ↓
Merchant Approval
     ↓
Execution Agent
     ↓
Payment / Commerce Layer
     ↓
Measurement Agent
     ↓
Revenue & ROI Decision
💳 Razorpay Test Mode

The project includes Razorpay Test Mode integration for demonstrating payment/order workflows safely without processing real money.

Razorpay credentials are stored locally using environment variables and are not included in the repository.

📊 Demo

The project uses synthetic/demo merchant data to demonstrate the complete AI growth workflow.

Example workflow:

Running Shoes → Sports Socks

The system identifies customers with a strong product relationship, recommends a cross-sell campaign, requests approval, executes the campaign, and measures incremental revenue and ROI.

🛠️ Technology Stack
Python
FastAPI
SQLite
JavaScript
HTML
CSS
Razorpay Test Mode API
REST APIs
AI-driven decision logic
🚀 Running the Project
1. Create and activate the virtual environment
python -m venv venv
2. Install dependencies
pip install -r requirements.txt
3. Configure environment variables

Create a .env file in the project root:

RAZORPAY_KEY_ID=your_test_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret

Never commit .env or API secrets to GitHub.

4. Seed the demo database
python -m backend.seed_data
5. Start the application
python -m uvicorn backend.main:app --reload

Open:

http://127.0.0.1:8000
📈 Key Metrics

GrowthPilot AI measures:

Incremental Revenue
Conversion Rate
Incremental Conversions
Campaign Cost
ROI
Campaign Performance
AI Optimization Decisions
🔐 Safety & Data

This project is designed as a demonstration system.

All merchant/customer information used in the demo is synthetic. No real merchant financial data is included in the repository.

API credentials and secrets should always be stored in environment variables and excluded from source control.

🏆 Project Vision

GrowthPilot AI aims to move merchant growth from manual analysis and guesswork toward an autonomous, measurable AI growth system.

Instead of simply telling a merchant what they could do, the system creates a workflow where AI can:

Observe → Decide → Get Approval → Act → Measure → Optimize

GrowthPilot AI • Agentic Commerce Growth System
