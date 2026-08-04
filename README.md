# CARE Analytics Engine

> **AI-Powered Customer Support Quality Evaluation & Conversation Intelligence Platform**

CARE (Conversation Analysis & Review Engine) is an end-to-end analytical web application built to evaluate customer service interactions, extract structured sentiment insights, track resolution friction, and continuously improve AI agent dialogue models.

Inspired by enterprise AI customer experience infrastructure, CARE processes customer support transcripts using **OpenAI's GPT-4o** to score sentiment, identify root causes of friction, propose optimal agent responses, and generate structured training datasets.

---

## ✨ Features & Modules

### 🔍 1. Single Conversation Analyzer
- **Automated Quality Scoring**: Instantly evaluates transcripts to output Sentiment Score (1–10), Resolution Quality (1–10), and Escalation Risk (Low / Medium / High).
- **Issue Classification & Summary**: Automatically categorizes customer intent (Delivery, Financing, Vehicle Quality, Trade-in, Documentation) with concise issue summaries.
- **Agent Performance & Friction Identification**: Pinpoints exact dialogue friction points and highlights key breakdown areas.
- **"What the AI Agent Should Have Said"**: Generates specific, empathetic, and policy-compliant dialogue recommendations to coach AI models and human Customer Advocates.
- **GPT-4o Deep Dive Narrative**: Generates narrative diagnostic summaries covering customer behavior trends and suggested model fine-tuning targets.

### 📊 2. Batch Analytics Dashboard
- **Batch CSV Processing**: Processes bulk conversation datasets with rate-limit throttling and real-time progress monitoring.
- **Executive Strategy Summary**: Generates plain English executive digests covering batch health, top friction categories, and operational recommendations.
- **Aggregate KPI Metrics**: Displays average sentiment, resolution rates, percentage of high-escalation risk conversations, and average quality scores.
- **Interactive Visualizations**: Plotly bar charts (category distribution), pie charts (resolution breakdown), and line charts with threshold markers (conversations with sentiment < 5).
- **Export Capabilities**: Allows single-click CSV exports of enriched evaluation data.

### 🧪 3. AI Agent Improvement Lab
- **Response Improver**: Side-by-side prompt coaching comparing current AI responses against improved GPT-4o versions across purchase stages, complete with actionable CX coaching notes.
- **Training FAQ Generator**: Extracts top FAQ clusters from multi-transcript inputs and formats structured CSV training datasets (Question, Ideal Answer, Category, Priority).

---

## 🧰 Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/) (Custom Glassmorphism Theme)
- **LLM Layer**: [OpenAI API](https://platform.openai.com/) (`gpt-4o`)
- **Data & Visualizations**: Pandas, Plotly Express
- **Runtime**: Python 3.11+

---

## ⚙️ Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rahul0443/care-analytics-demo.git
cd care-analytics-demo
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Credentials
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```
Or set up `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

### 4. Launch the Application
```bash
streamlit run app.py
```
The app will open automatically at `http://localhost:8501`.

---

## ☁️ Deployment

This project is pre-configured for 1-click deployment on **Streamlit Community Cloud**:
1. Connect your repository at [share.streamlit.io](https://share.streamlit.io/).
2. Set the main file path to `app.py`.
3. Add `OPENAI_API_KEY` under **Advanced Settings -> Secrets**.
4. Click **Deploy!**

---

## 📝 License

Distributed under the MIT License.
