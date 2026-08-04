# CARE Analytics Demo — Carvana Customer Care Strategy Analytics

A professional, enterprise-grade Streamlit web application simulating Carvana's **CARE (Conversation Analysis Review Engine)** platform and AI Customer Support Agent **Sebastian**.

Built by **Rahul Muddhapuram** after interviewing with **Trevor Jensen**, Senior Manager of Customer Care Strategy Analytics at Carvana.

---

## 📖 The Story Behind This Project

During my interview with Trevor Jensen, he shared details about Carvana's AI-powered customer experience infrastructure — specifically their AI agent **Sebastian** and their internal **Conversation Analysis Review Engine (CARE)** built on Azure AI Foundry.

I was so energized by our conversation that I went home, deeply researched Carvana's platform and public case studies, and built this application to demonstrate my understanding of the problem space and my ability to immediately contribute to the team.

This is not a generic demo. Every feature is designed around the specific analytical problems Carvana's Customer Care Strategy Analytics team solves every day:
- **Sebastian**: AI Agent handling customer support conversations across financing, delivery, vehicle quality, trade-ins, and documentation. Reduced inbound calls per sale by 45% and reduced YoY customer care costs by 40%+.
- **CARE**: AI Engine evaluating 100% of customer interactions (not just a 1% sample) to surface friction, monitor agent quality, and continuously improve Sebastian and human Advocates.

---

## 🛠️ Application Structure & Features

The app is organized into four main sections:

### 1. 🏠 Home Page
- **The Problem & Solution**: Explains Carvana's scale, the challenge of maintaining quality across millions of interactions, and how CARE solves it.
- **Carvana CX Impact Metrics**: Displays real results (45% call reduction, 100% conversation visibility, 40%+ YoY cost reduction).
- **Direct Navigation**: One-click launcher to enter the analytical suite.

### 2. 🔍 Single Conversation Analyzer
- **Transcript Input**: Interactive text area with 5 pre-built realistic Carvana sample conversations (Delayed Delivery, Financing APR, Happy Trade-in, Vehicle Quality scratch, State Registration tag).
- **Row 1 Metric Cards**: Sentiment Score (1-10 color-coded), Resolution Quality (1-10 color-coded), Escalation Risk (Low/Medium/High).
- **Row 2 Insight Cards**: Issue Category with icon, Issue Summary, Resolution Status badge, Agent Evaluation, and Key Friction Point (highlighted yellow).
- **Row 3 Highlight Box**: "💡 What Sebastian Should Have Said" (suggested optimal agent response).
- **Row 4 Deep Dive**: Expandable GPT-4o narrative analysis outlining customer behavior patterns and training implications.

### 3. 📊 Batch Dashboard
- **Batch CSV Upload**: Upload any CSV containing customer transcripts or click "Download Sample CSV" (pre-loaded with 10 real-world conversations).
- **Progress Tracking**: Real-time progress bar with rate-limit throttling.
- **GPT-4o Executive Summary Box**: High-level plain English summary of batch health, friction clusters, and strategic recommendations.
- **5 Summary KPI Cards**: Average Sentiment, % Resolved, % High Escalation Risk, Top Issue Category, Average Resolution Quality.
- **Interactive Visualizations**:
  - Plotly Bar Chart: Issue Category Distribution in Carvana Green (`#00A67C`).
  - Plotly Pie Chart: Resolution Status breakdown.
  - Plotly Line Chart: Sentiment Score across conversations with a red dotted threshold line at score 5.
- **Data Table & CSV Export**: Filterable table with color-coded risk flags and full dataset CSV export.

### 4. 🧪 Sebastian Improvement Lab
- **Tab A: Response Improver**: Side-by-side comparison of Sebastian's original response vs GPT-4o's improved response across purchase stages (Browsing, Financing, Post-Purchase, Delivery, Trade-in, Documentation), accompanied by 3 senior CX coaching notes.
- **Tab B: Training FAQ Generator**: Multi-transcript pattern analysis generating structured FAQ tables, priority rankings (High/Medium/Low), strategic recommendations, and exportable CSV training data.

---

## 🧰 Tech Stack

- **Frontend / Framework**: Streamlit (`v1.35.0`)
- **AI / LLM Layer**: OpenAI API (`gpt-4o` model via `openai v1.30.0`)
- **Visualizations**: Plotly (`v5.22.0`)
- **Data Processing**: Pandas (`v2.2.2`)
- **Language**: Python 3.11
- **Deployment**: Streamlit Community Cloud

---

## 💻 Local Setup Instructions

1. **Clone or navigate to the repository:**
   ```bash
   cd "Trevor Project"
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API Key:**
   - Option A: Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Option B: Create a `.streamlit/secrets.toml` file:
     ```toml
     OPENAI_API_KEY = "your_openai_api_key_here"
     ```
   *(Note: If no API key is provided, the application automatically uses built-in smart mock CARE analytics so all features remain fully functional for demonstration purposes).*

5. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Deployment on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select your repository, branch (`main`), and main file path (`app.py`).
4. In **Advanced Settings**, add your `OPENAI_API_KEY` under Secrets:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
5. Click **Deploy!**

---

## 👤 About the Builder

**Rahul Muddhapuram**
- Candidate for Customer Care Strategy Analytics at Carvana.
- Passionate about leveraging AI, LLM orchestration, and strategy analytics to build seamless, customer-first experiences.
- Contact: Rahul Muddhapuram
