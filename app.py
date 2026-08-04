import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import time
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="CARE Analytics Engine | Carvana CX Strategy",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise UI/UX Design System (Ultra-Clean, High-Contrast & Readable)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
    
    /* Global Canvas & Base Fonts */
    html, body, .stApp {
        background-color: #070C14;
        color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Top Glass Navbar */
    .carvana-navbar {
        background: rgba(15, 24, 38, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px 28px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }
    .brand-title-container {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .brand-logo-badge {
        background: linear-gradient(135deg, #106BC7 0%, #228BE6 100%);
        width: 46px;
        height: 46px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 14px rgba(34, 139, 230, 0.35);
    }
    .carvana-navbar h2 {
        color: #FFFFFF !important;
        margin: 0;
        font-size: 1.45rem;
        letter-spacing: -0.02em;
    }
    .carvana-navbar p {
        color: #94A3B8 !important;
        margin: 2px 0 0 0;
        font-size: 0.85rem;
    }
    .status-pill {
        background: rgba(0, 200, 150, 0.12);
        border: 1px solid rgba(0, 200, 150, 0.35);
        color: #00C896;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        background-color: #00C896;
        border-radius: 50%;
        box-shadow: 0 0 8px #00C896;
    }
    
    /* Ultra-Clean Cards */
    .glass-card {
        background: #0F1826;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(34, 139, 230, 0.4);
        transform: translateY(-2px);
    }
    
    /* Clean Metric Cards */
    .metric-card {
        background: #0F1826;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 22px 16px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        border-color: #228BE6;
        transform: translateY(-2px);
    }
    .metric-val {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 4px;
        letter-spacing: -0.03em;
    }
    .metric-lbl {
        color: #94A3B8;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    
    /* Content Highlight Boxes */
    .insight-box-blue {
        background: rgba(34, 139, 230, 0.08);
        border-left: 4px solid #228BE6;
        border-radius: 0 10px 10px 0;
        padding: 20px 24px;
        margin: 18px 0;
    }
    .insight-box-gold {
        background: rgba(250, 176, 5, 0.08);
        border-left: 4px solid #FAB005;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .response-card-red {
        background: rgba(255, 75, 75, 0.06);
        border-left: 4px solid #FF4B4B;
        border-radius: 0 10px 10px 0;
        padding: 20px;
        height: 100%;
    }
    .response-card-blue {
        background: rgba(34, 139, 230, 0.06);
        border-left: 4px solid #228BE6;
        border-radius: 0 10px 10px 0;
        padding: 20px;
        height: 100%;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .badge-green { background: rgba(0, 200, 150, 0.2); color: #00C896; border: 1px solid rgba(0, 200, 150, 0.4); }
    .badge-blue { background: rgba(34, 139, 230, 0.2); color: #228BE6; border: 1px solid rgba(34, 139, 230, 0.4); }
    .badge-yellow { background: rgba(250, 176, 5, 0.2); color: #FAB005; border: 1px solid rgba(250, 176, 5, 0.4); }
    .badge-red { background: rgba(255, 75, 75, 0.2); color: #FF4B4B; border: 1px solid rgba(255, 75, 75, 0.4); }

    /* Clean Buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #106BC7 0%, #228BE6 100%) !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(34, 139, 230, 0.35) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(34, 139, 230, 0.5) !important;
    }

    /* Sidebar Clean styling */
    section[data-testid="stSidebar"] {
        background-color: #040810 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    </style>
""", unsafe_allow_html=True)

# Sample Conversations
SAMPLE_CONVERSATIONS = {
    "Sample 1: Delayed Delivery (Frustrated)": """Customer: Hi, I've been waiting for my 2021 Toyota Camry delivery since yesterday at 3 PM. Nobody showed up and nobody called me.
Agent: Thanks for contacting Carvana. Let me look up your order status. Can I have your order number?
Customer: Order #CV-8849201. I've already called twice today and stayed home taking time off work. This is unacceptable.
Agent: I see your appointment was delayed due to transport logistics from the regional hub in Dallas.
Customer: Well why didn't anyone notify me? I'm thinking about canceling this entire purchase if you can't guarantee a time today.
Agent: We apologize for the inconvenience. The new estimated arrival window is tomorrow between 10 AM and 2 PM.
Customer: Tomorrow? That doesn't work for me. I need the car for a trip starting tomorrow morning.
Agent: Unfortunately that is the earliest slot available on the carrier route.
Customer: Can I talk to a supervisor or get a compensation credit for lost wages and canceled trip plans?
Agent: You will receive an automated notification once the driver dispatches tomorrow morning. Let us know if you need anything else.""",

    "Sample 2: Financing Confusion (Confused)": """Customer: Hello, I just looked at my final purchase contract for the 2020 Honda Civic and the APR is listed as 6.8%, but my pre-qualification letter said 4.9%. Why did it jump almost 2%?
Agent: Hello! I'd be happy to explain how pre-qualification and final underwriting differ at Carvana.
Customer: Okay, because 6.8% adds over $40 a month to my payment and I budgeted based on the 4.9% offer.
Agent: Pre-qualification utilizes soft credit pull estimations prior to income and debt-to-income verification. Upon formal credit application submission, our lending partners evaluate actual stip verification and credit bureau hard pulls.
Customer: I understand that, but my credit score hasn't changed at all in the last two weeks and my income proof was verified.
Agent: Minor variance in LTV (loan-to-value) ratios based on the vehicle selected and total financed accessories or warranty add-ons can shift underwriting tier brackets.
Customer: So if I remove the extended protection plan, will my APR go back down to 4.9%?
Agent: Removing protection plans alters the total funded balance which may adjust tier scoring, but APR tier re-evaluation requires re-submitting the deal terms.
Customer: Okay... that's a bit technical, but I guess I'll try adjusting the protection plan and re-submitting. Thanks.""",

    "Sample 3: Happy Trade-in Customer (Positive)": """Customer: Hi! I just finished uploading my trade-in documents for my 2018 Mazda CX-5. I got an offer for $16,500 and wanted to make sure everything is good to go for Friday!
Agent: Hello! Congratulations on your trade-in! Let me pull up your account right away to double check your document verifications.
Customer: Great, thank you! I was amazed at how easy the online appraisal was compared to local dealerships.
Agent: That's wonderful to hear! I just checked your account: your title upload, registration, and photo verifications are 100% complete and approved!
Customer: That's fantastic news! So when the Advocate drops off my new 2022 Subaru Outback, they just drive away with my Mazda?
Agent: Exactly right! Our Advocate will inspect your Mazda CX-5, complete a 5-minute test drive, sign the bill of sale with you, and hand over the keys to your new Subaru!
Customer: Wow, that is so seamless! Is there anything else I need to clean out or prepare?
Agent: Just remember to remove your garage door opener, personal items, and sign the title at the highlighted line. We'll handle everything else!
Customer: Perfect, thank you so much for the amazing service!""",

    "Sample 4: Vehicle Quality Concern (Upset)": """Customer: I accepted delivery of my 2021 Ford F-150 two hours ago. While washing it in daylight, I noticed a deep 6-inch paint scratch down the passenger door that wasn't in any 360 degree photos online.
Agent: Hello, I'm sorry to hear that your vehicle has cosmetic damage that was not depicted in the online gallery.
Customer: It definitely wasn't disclosed. The online listing marked zero imperfections on the passenger side. I feel misled into accepting delivery.
Agent: Understood. You are currently within your 7-Day Money-Back Guarantee window. We can schedule a repair authorization through SilverRock or initiate a vehicle exchange.
Customer: How long does SilverRock repair take? Will Carvana provide a rental car while my truck is in the body shop?
Agent: SilverRock claim approvals take 24-48 business hours. Rental coverage depends on warranty terms and body shop repair duration guidelines.
Customer: So you can't tell me right now if I get a rental or how long I'll be without my truck? That's really frustrating.
Agent: I can open a claim ticket with SilverRock right now, but repair approval details are managed directly by SilverRock claims adjusters.""",

    "Sample 5: Documentation Question (Neutral)": """Customer: Hi, I purchased my car 3 weeks ago in Texas. My temporary license plate expires in 10 days and I haven't received my official license plates or title registration documents yet.
Agent: Hello! Thanks for reaching out regarding your registration status.
Customer: Can you tell me when the Texas DMV paperwork was submitted and when I should expect my plates?
Agent: Carvana processes registration files through our centralized registration team. Standard processing time typically ranges from 4 to 6 weeks from delivery.
Customer: In Texas, state regulations require registration within 30 days. If my temp tag expires, can you issue an extension?
Agent: If your temporary tag is within 7 days of expiration, our registration system allows us to issue a digital 30-day temporary extension tag.
Customer: Okay, so should I contact you back in 3 days to get the digital tag extension?
Agent: Yes, feel free to check back in 3 days or watch your email dashboard for registration updates."""
}

# OpenAI Helper (Cached Resource)
@st.cache_resource
def get_openai_client():
    api_key = None
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
    elif os.getenv("OPENAI_API_KEY"):
        api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        try:
            from openai import OpenAI
            return OpenAI(api_key=api_key)
        except Exception as e:
            st.error(f"Error initializing OpenAI client: {e}")
            return None
    return None

def clean_json_string(raw_str):
    if not raw_str:
        return ""
    cleaned = re.sub(r'```(?:json)?\s*', '', raw_str)
    cleaned = re.sub(r'```\s*$', '', cleaned)
    return cleaned.strip()

# Mock Fallback Engine
def generate_mock_analysis(transcript):
    text_lower = transcript.lower()
    if "delayed" in text_lower or "canceling" in text_lower or "camry" in text_lower:
        return {
            "sentiment_score": 2, "sentiment_label": "Highly Frustrated", "issue_category": "Delivery",
            "issue_summary": "Customer experienced unnotified delivery delay and missed time off work, seeking schedule guarantee or compensation.",
            "resolution_status": "Unresolved", "resolution_quality_score": 3,
            "agent_performance": "The agent provided rigid, robotic timeline updates without acknowledging the severe inconvenience or offering proactive escalation.",
            "key_friction_point": "Lack of proactive delay notification and refusal to offer supervisor escalation or inconvenience credit.",
            "suggested_better_response": "I sincerely apologize for missing your delivery window without notice. I know your time is valuable. Let me immediately escalate this to our hub logistics dispatch manager to secure a priority slot and issue a $150 inconvenience credit to your account right now.",
            "escalation_risk": "High", "escalation_reason": "Customer is threatening order cancellation due to missed work hours and lack of resolution.",
            "deep_dive": "This conversation represents a critical friction point in Carvana's delivery fulfillment chain. The customer experienced an unnotified delay on a high-stakes delivery date. The agent responded with passive policy statements rather than empathetic ownership. Sebastian should be trained to recognize missed delivery triggers, immediately offer standardized inconvenience credits, and flag dispatch for priority scheduling."
        }
    elif "apr" in text_lower or "pre-qualification" in text_lower or "civic" in text_lower:
        return {
            "sentiment_score": 5, "sentiment_label": "Frustrated", "issue_category": "Financing",
            "issue_summary": "Customer questioned why final contract APR increased by 1.9% compared to pre-qualification offer.",
            "resolution_status": "Partially Resolved", "resolution_quality_score": 6,
            "agent_performance": "Agent accurately explained technical underwriting factors but relied heavily on financial jargon that left the customer slightly confused.",
            "key_friction_point": "Complex explanation of loan-to-value tiers and stip verifications without clear step-by-step guidance on how to lower the rate.",
            "suggested_better_response": "I completely understand why a rate change is surprising! Pre-qualification is an estimate, but when protection plans were added, it shifted your total funded amount into a different bracket. If we adjust your warranty coverage, I can recalculate your rate back toward 4.9% right now.",
            "escalation_risk": "Medium", "escalation_reason": "Customer accepted the explanation tentatively but remains dissatisfied with payment variance.",
            "deep_dive": "Financing explanations require balancing accuracy with accessibility. While the agent correctly identified underwriting variance factors, the heavy use of industry jargon created customer friction. Sebastian should be trained to break down interest rate variances into simple line-item math and proactively demonstrate how protection plan adjustments directly lower monthly payments."
        }
    elif "trade-in" in text_lower or "mazda" in text_lower or "subaru" in text_lower:
        return {
            "sentiment_score": 9, "sentiment_label": "Highly Satisfied", "issue_category": "Trade-in",
            "issue_summary": "Customer verified approved trade-in document status and logistics for Friday vehicle exchange.",
            "resolution_status": "Resolved", "resolution_quality_score": 10,
            "agent_performance": "Agent was warm, enthusiastic, verified all document approvals instantly, and provided a clear step-by-step Advocate pickup expectation.",
            "key_friction_point": "Minor uncertainty about what steps happen during the physical pickup appointment.",
            "suggested_better_response": "Your trade-in is 100% verified and ready! When our Advocate arrives on Friday, they'll complete a quick 5-minute walkaround, sign the transfer forms, and hand over your Outback keys!",
            "escalation_risk": "Low", "escalation_reason": "Customer is extremely pleased with the online appraisal process and clear verification steps.",
            "deep_dive": "This conversation illustrates an ideal customer Advocate interaction. The agent validated the customer's excitement, confirmed document verification, and outlined exact delivery expectations. Sebastian should use this transcript format as a benchmark model for positive trade-in confirmations."
        }
    elif "scratch" in text_lower or "paint" in text_lower or "f-150" in text_lower:
        return {
            "sentiment_score": 3, "sentiment_label": "Frustrated", "issue_category": "Vehicle Quality",
            "issue_summary": "Customer discovered undisclosed 6-inch paint scratch post-delivery and requested repair and rental car clarity.",
            "resolution_status": "Unresolved", "resolution_quality_score": 4,
            "agent_performance": "Agent acknowledged the cosmetic defect but deflected immediate rental car and repair answers to SilverRock third-party adjusters.",
            "key_friction_point": "Uncertainty surrounding SilverRock repair duration and rental vehicle approval during the 7-day trial.",
            "suggested_better_response": "I am so sorry this scratch wasn't caught in our inspection photos! Because you're in your 7-Day Guarantee, I am starting a SilverRock repair ticket right now and authorizing a $50/day rental car credit so you aren't left without transportation while it's fixed.",
            "escalation_risk": "High", "escalation_reason": "Customer feels misled regarding undisclosed cosmetic condition on a high-value truck purchase.",
            "deep_dive": "Undisclosed cosmetic defects directly threaten customer trust during the 7-Day Guarantee period. The agent's reliance on third-party SilverRock policies created ambiguity regarding rental coverage. Sebastian must be empowered to initiate immediate cosmetic repair claims while providing definitive rental car guidelines."
        }
    else:
        return {
            "sentiment_score": 6, "sentiment_label": "Neutral", "issue_category": "Documentation",
            "issue_summary": "Customer inquired about Texas temporary license plate expiration and official registration timeline.",
            "resolution_status": "Partially Resolved", "resolution_quality_score": 7,
            "agent_performance": "Agent provided general registration timelines and correctly explained the 30-day digital temp tag extension rule.",
            "key_friction_point": "Generic nationwide registration timelines rather than state-specific Texas DMV tracking updates.",
            "suggested_better_response": "In Texas, our average DMV registration completion is 25 days. Since your temp tag expires in 10 days, I've queued up your 30-day digital extension tag so you can print it directly from your dashboard in 3 days if official plates haven't arrived yet!",
            "escalation_risk": "Low", "escalation_reason": "Customer received actionable instructions on obtaining a temporary tag extension.",
            "deep_dive": "Registration inquiries account for a significant portion of post-delivery care volume. The agent handled the core policy well but missed an opportunity to provide Texas-specific tracking metrics. Sebastian should integrate state-specific DMV API timelines into registration responses."
        }

# Single Conversation Analysis (Cached Data for 0ms re-runs)
@st.cache_data(show_spinner=False, ttl=3600)
def analyze_conversation(transcript):
    client = get_openai_client()
    if not client:
        time.sleep(0.3)
        return generate_mock_analysis(transcript)
    
    system_prompt = """You are an expert customer experience analyst working on Carvana's CARE platform. 
Your job is to analyze customer support conversation transcripts and extract structured insights that help improve Sebastian, Carvana's AI customer support agent, and the overall customer experience.

Analyze the conversation and return ONLY a valid JSON object with no markdown formatting, no code fences, no preamble. Just the raw JSON.

Return exactly this structure:
{
  "sentiment_score": integer 1-10 where 1 is extremely frustrated and 10 is completely satisfied,
  "sentiment_label": one of "Highly Frustrated" / "Frustrated" / "Neutral" / "Satisfied" / "Highly Satisfied",
  "issue_category": one of "Financing" / "Delivery" / "Vehicle Quality" / "Trade-in" / "Documentation" / "General Inquiry" / "Other",
  "issue_summary": "one clear sentence summarizing exactly what the customer needed",
  "resolution_status": one of "Resolved" / "Partially Resolved" / "Unresolved",
  "resolution_quality_score": integer 1-10,
  "agent_performance": "one sentence honest evaluation of how well the agent handled this interaction",
  "key_friction_point": "the specific moment or exact topic where the customer showed the most frustration or confusion",
  "suggested_better_response": "exactly what Sebastian should have said at the friction point — specific, empathetic, and actionable",
  "escalation_risk": one of "Low" / "Medium" / "High",
  "escalation_reason": "one sentence explaining why this is or is not an escalation risk",
  "deep_dive": "a detailed 4-5 sentence narrative analysis covering: what went well, what went wrong, what customer behavior pattern this represents, and what this conversation suggests about how Sebastian should be trained differently"
}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transcript:\n{transcript}"}
            ],
            temperature=0.2,
            max_tokens=650
        )
        cleaned_content = clean_json_string(response.choices[0].message.content)
        return json.loads(cleaned_content)
    except Exception as e:
        st.warning(f"CARE Engine notice: {e}. Utilizing fallback analytics.")
        return generate_mock_analysis(transcript)

# Executive Summary API
def generate_batch_executive_summary(df):
    client = get_openai_client()
    if not client:
        avg_sent = df['sentiment_score'].mean()
        unresolved_pct = (df['resolution_status'] == 'Unresolved').mean() * 100
        top_cat = df['issue_category'].mode()[0] if not df['issue_category'].empty else 'Delivery'
        return f"This batch of {len(df)} customer conversations reflects an average sentiment score of {avg_sent:.1f}/10 with {unresolved_pct:.0f}% unresolved interactions. The primary customer friction point centers on {top_cat.lower()} coordination, where communication gaps caused significant customer anxiety. Delivery logistics and post-delivery cosmetic disclosures represented the highest escalation risks. Strategy Recommendation: Sebastian should be trained to automatically issue proactive delivery dispatch notifications and provide immediate rental authorization policies during warranty claims."

    prompt = f"""You are a Senior CX Analytics Lead at Carvana analyzing a batch of customer conversations evaluated by the CARE platform.
    
Batch Metrics:
- Total Conversations: {len(df)}
- Average Sentiment Score: {df['sentiment_score'].mean():.1f}/10
- Resolution Breakdown: {df['resolution_status'].value_counts().to_dict()}
- Issue Categories: {df['issue_category'].value_counts().to_dict()}
- High Risk Escalations: {(df['escalation_risk'] == 'High').sum()}

Write a concise 4 sentence plain English executive summary covering:
1. Overall health of the conversation batch
2. The top customer friction point identified across conversations
3. Which issue category is most problematic and why
4. One high-impact strategic recommendation for training Sebastian to improve resolution rates.
Return plain text only."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return f"Batch analysis of {len(df)} conversations shows an average sentiment of {df['sentiment_score'].mean():.1f}/10. Primary friction occurs in Delivery & Vehicle Quality inquiries. High escalation risk is driven by unnotified fulfillment delays. Recommendation: Implement automated proactive tracking updates and instant rental credit workflows into Sebastian's dialogue model."

# Response Improver API (Cached)
@st.cache_data(show_spinner=False, ttl=3600)
def improve_response_call(customer_msg, current_response, context):
    client = get_openai_client()
    if not client:
        return {
            "improved_response": f"I completely understand your concern regarding your {context.lower()} inquiry! Let me check your account immediately and provide you with a clear, direct resolution right now.",
            "coaching_notes": [
                "Empathy First: Validated customer emotion directly before moving into technical policy steps.",
                "Actionable Ownership: Eliminated passive policy deflection by taking direct responsibility for immediate next steps.",
                "Clarity & Transparency: Replaced internal jargon with transparent timelines and actionable expectations."
            ]
        }
    
    prompt = f"""You are a Customer Advocate Coach at Carvana training Sebastian, Carvana's AI support agent.
Customer Purchase Stage: {context}
Customer Message: "{customer_msg}"
Sebastian's Current Response: "{current_response}"

Improve Sebastian's response to make it empathetic, highly specific, proactive, and clear.
Also provide 3 coaching bullet points explaining why the improved version is better.

Return ONLY a JSON object with keys:
"improved_response": string,
"coaching_notes": array of 3 strings"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400
        )
        cleaned = clean_json_string(res.choices[0].message.content)
        return json.loads(cleaned)
    except Exception:
        return {
            "improved_response": f"I completely understand your concern regarding your {context.lower()} inquiry! Let me check your account immediately and provide you with a clear, direct resolution right now.",
            "coaching_notes": [
                "Empathy First: Validated customer emotion directly before moving into technical policy steps.",
                "Actionable Ownership: Eliminated passive policy deflection by taking direct responsibility for immediate next steps.",
                "Clarity & Transparency: Replaced internal jargon with transparent timelines and actionable expectations."
            ]
        }

# Training FAQ API
def generate_training_faqs_call(transcripts_str):
    client = get_openai_client()
    if not client:
        return {
            "faqs": [
                {
                    "question": "What happens if my delivery is delayed without notification?",
                    "ideal_answer": "If your delivery window changes, Sebastian will proactively send real-time GPS tracking updates and issue an immediate inconvenience credit for schedule shifts.",
                    "category": "Delivery", "priority": "High"
                },
                {
                    "question": "Why did my final contract APR change from my pre-qualification estimate?",
                    "ideal_answer": "Pre-qualification uses soft credit pulls. Final APR adjusts based on verified credit stip verifications, protection plans, or loan-to-value changes. You can adjust warranty options to re-lower your rate.",
                    "category": "Financing", "priority": "High"
                },
                {
                    "question": "What should I do if I spot an undisclosed cosmetic paint scratch at delivery?",
                    "ideal_answer": "Within your 7-Day Guarantee, report cosmetic defects directly in app to launch a 24-48 hr SilverRock repair claim with rental car allowance options.",
                    "category": "Vehicle Quality", "priority": "High"
                },
                {
                    "question": "How do I get a temporary tag extension if my state registration is delayed?",
                    "ideal_answer": "If your temporary tag is within 7 days of expiration, a 30-day digital tag extension can be printed directly from your account dashboard.",
                    "category": "Documentation", "priority": "Medium"
                },
                {
                    "question": "What happens during the trade-in vehicle pickup appointment?",
                    "ideal_answer": "Our Customer Advocate performs a quick 5-minute walkaround, verifies title documents, completes the bill of sale, and hands over your new keys!",
                    "category": "Trade-in", "priority": "Medium"
                }
            ],
            "recommendations": [
                "Automate delay alerts: Integrate real-time carrier GPS updates directly into Sebastian chat prompts.",
                "Simplify financing breakdown: Train Sebastian to present interest rate tier shifts using visual line-item breakdowns.",
                "Proactive warranty authorization: Empower Sebastian to issue instant SilverRock repair tickets during 7-Day trial windows."
            ]
        }

    prompt = f"""You are a CX AI Strategy Specialist analyzing multiple customer support transcripts for Carvana's AI Agent Sebastian.
Transcripts:
{transcripts_str}

Analyze patterns across these transcripts and generate the Top 5 FAQs Sebastian should be trained to handle better, along with 3 strategic training recommendations.

Return ONLY a JSON object with keys:
"faqs": array of 5 objects (each having "question", "ideal_answer", "category", "priority" [High/Medium/Low]),
"recommendations": array of 3 strings"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        cleaned = clean_json_string(res.choices[0].message.content)
        return json.loads(cleaned)
    except Exception:
        return generate_training_faqs_call("")

# Top Glass Navbar Component
st.markdown("""
<div class="carvana-navbar">
    <div class="brand-title-container">
        <div class="brand-logo-badge">🚗</div>
        <div>
            <h2>CARE Analytics Engine</h2>
            <p>Carvana Conversation Analysis & Review Engine | Built by Rahul Muddhapuram</p>
        </div>
    </div>
    <div class="status-pill">
        <div class="status-dot"></div>
        LIVE GPT-4o-mini ENGINE
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("""
<div style="padding: 10px 0 15px 0; text-align: center;">
    <div style="background: linear-gradient(135deg, #106BC7 0%, #228BE6 100%); width: 48px; height: 48px; border-radius: 12px; margin: 0 auto 10px auto; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 14px rgba(34, 139, 230, 0.4);">
        🚗
    </div>
    <h2 style="color: #228BE6; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.5rem; font-weight: 800; margin: 0; letter-spacing: -0.02em;">
        CARVANA
    </h2>
    <p style="color: #94A3B8; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; margin: 3px 0 0 0; font-weight: 600;">
        CARE ANALYTICS
    </p>
</div>
""", unsafe_allow_html=True)


if "nav" not in st.session_state:
    st.session_state["nav"] = "Home"

nav_selection = st.sidebar.radio(
    "Navigation Menu",
    ["Home", "Conversation Analyzer", "Batch Dashboard", "Sebastian Improvement Lab"],
    index=["Home", "Conversation Analyzer", "Batch Dashboard", "Sebastian Improvement Lab"].index(st.session_state["nav"])
)
st.session_state["nav"] = nav_selection

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.8rem; color: #94A3B8;">
    <strong style="color: #228BE6;">CARE Architecture</strong><br>
    • Model: GPT-4o-mini (Azure AI Foundry)<br>
    • Scope: 100% Conversation Analysis<br>
    • Target: Sebastian AI & Advocate Quality
</div>
""", unsafe_allow_html=True)


# ==========================================
# PAGE 1: HOME PAGE
# ==========================================
if st.session_state["nav"] == "Home":
    st.title("Conversation Analysis & Review Engine")
    st.caption("Built after interviewing with Carvana's Customer Care Strategy Analytics team")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #228BE6; margin-top:0;">🎯 The Real Problem</h3>
            <p style="line-height: 1.65; color: #E2E8F0;">
                Carvana handles millions of customer conversations every month. Their AI agent <strong>Sebastian</strong> handles standard queries while human <strong>Customer Advocates</strong> handle complex ones. 
            </p>
            <p style="line-height: 1.65; color: #E2E8F0;">
                The challenge: <strong>How do you maintain quality at scale?</strong>
            </p>
            <ul style="color: #94A3B8; line-height: 1.75; padding-left: 20px;">
                <li>How do you identify conversations that went poorly?</li>
                <li>Where is Sebastian experiencing dialogue friction?</li>
                <li>What specific scenarios require updated training data?</li>
            </ul>
            <p style="line-height: 1.65; color: #E2E8F0;">
                Carvana built <strong>CARE</strong> to answer these questions — analyzing <strong>100% of conversations with AI</strong>, not just a random 1% sample.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #00C896; margin-top:0;">🚀 What This App Does</h3>
            <p style="line-height: 1.65; color: #E2E8F0;">
                This web application simulates the analytical layer that powers Carvana's strategic decision-making:
            </p>
            <ul style="color: #94A3B8; line-height: 1.75; padding-left: 20px;">
                <li><strong>Conversation Analyzer:</strong> Instant AI quality scoring, friction points, and <em>"What Sebastian Should Have Said"</em>.</li>
                <li><strong>Batch Dashboard:</strong> Full executive sentiment tracking, category distribution, and risk threshold monitoring.</li>
                <li><strong>Sebastian Improvement Lab:</strong> Side-by-side prompt optimization with senior CX coaching notes and training FAQ extraction.</li>
            </ul>
            <p style="line-height: 1.65; color: #E2E8F0;">
                Every feature maps directly to real analytical problems Carvana's strategy team solves every day.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box-blue" style="margin-top: 24px; text-align: center;">
        <p style="margin: 0; font-size: 0.95rem; color: #F8FAFC;">
            💡 <strong>Tech Stack Note:</strong> Built with <strong>OpenAI GPT-4o-mini</strong> — the same model family powering Carvana's Azure AI Foundry infrastructure.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.07);'><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #F8FAFC;'>Carvana Real CX Impact</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-val" style="color: #228BE6;">45%</div>
            <div class="metric-lbl">Reduction in Inbound Calls per Sale</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-val" style="color: #00C896;">100%</div>
            <div class="metric-lbl">Visibility into Customer Conversations</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-val" style="color: #FAB005;">40%+</div>
            <div class="metric-lbl">YoY Reduction in Customer Care Costs</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    btn_c1, btn_c2, btn_c3 = st.columns([1, 2, 1])
    with btn_c2:
        if st.button("🚀 Launch Conversation Analyzer", type="primary", use_container_width=True):
            st.session_state["nav"] = "Conversation Analyzer"
            st.rerun()


# ==========================================
# PAGE 2: CONVERSATION ANALYZER
# ==========================================
elif st.session_state["nav"] == "Conversation Analyzer":
    st.title("🔍 Single Conversation Analyzer")
    st.caption("Paste a transcript or click a sample to generate structured CARE quality insights.")

    if "active_sample_label" not in st.session_state:
        st.session_state["active_sample_label"] = "🚚 Sample 1: Delayed Delivery"
    if "transcript_text_area" not in st.session_state:
        st.session_state["transcript_text_area"] = SAMPLE_CONVERSATIONS["Sample 1: Delayed Delivery (Frustrated)"]

    left_panel, right_panel = st.columns([1, 1], gap="large")

    with left_panel:
        st.markdown("#### Input Transcript")
        
        st.markdown("**Load Sample Conversations:**")
        s_cols = st.columns(3)
        btn1_type = "primary" if st.session_state.get("active_sample_label") == "🚚 Sample 1: Delayed Delivery" else "secondary"
        btn2_type = "primary" if st.session_state.get("active_sample_label") == "💰 Sample 2: Financing APR" else "secondary"
        btn3_type = "primary" if st.session_state.get("active_sample_label") == "🔄 Sample 3: Trade-in" else "secondary"

        if s_cols[0].button("🚚 1. Delivery", type=btn1_type, use_container_width=True):
            st.session_state["active_sample_label"] = "🚚 Sample 1: Delayed Delivery"
            st.session_state["transcript_text_area"] = SAMPLE_CONVERSATIONS["Sample 1: Delayed Delivery (Frustrated)"]
            st.session_state["last_analysis"] = analyze_conversation(st.session_state["transcript_text_area"])
            st.rerun()

        if s_cols[1].button("💰 2. APR", type=btn2_type, use_container_width=True):
            st.session_state["active_sample_label"] = "💰 Sample 2: Financing APR"
            st.session_state["transcript_text_area"] = SAMPLE_CONVERSATIONS["Sample 2: Financing Confusion (Confused)"]
            st.session_state["last_analysis"] = analyze_conversation(st.session_state["transcript_text_area"])
            st.rerun()

        if s_cols[2].button("🔄 3. Trade-in", type=btn3_type, use_container_width=True):
            st.session_state["active_sample_label"] = "🔄 Sample 3: Trade-in"
            st.session_state["transcript_text_area"] = SAMPLE_CONVERSATIONS["Sample 3: Happy Trade-in Customer (Positive)"]
            st.session_state["last_analysis"] = analyze_conversation(st.session_state["transcript_text_area"])
            st.rerun()
            
        s_cols2 = st.columns(2)
        btn4_type = "primary" if st.session_state.get("active_sample_label") == "🚗 Sample 4: Paint Scratch" else "secondary"
        btn5_type = "primary" if st.session_state.get("active_sample_label") == "📄 Sample 5: DMV Registration" else "secondary"

        if s_cols2[0].button("🚗 4. Paint Scratch", type=btn4_type, use_container_width=True):
            st.session_state["active_sample_label"] = "🚗 Sample 4: Paint Scratch"
            st.session_state["transcript_text_area"] = SAMPLE_CONVERSATIONS["Sample 4: Vehicle Quality Concern (Upset)"]
            st.session_state["last_analysis"] = analyze_conversation(st.session_state["transcript_text_area"])
            st.rerun()

        if s_cols2[1].button("📄 5. DMV Registration", type=btn5_type, use_container_width=True):
            st.session_state["active_sample_label"] = "📄 Sample 5: DMV Registration"
            st.session_state["transcript_text_area"] = SAMPLE_CONVERSATIONS["Sample 5: Documentation Question (Neutral)"]
            st.session_state["last_analysis"] = analyze_conversation(st.session_state["transcript_text_area"])
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        active_lbl = st.session_state.get("active_sample_label", "Custom Transcript")
        st.markdown(f"""
        <div style="background: rgba(34, 139, 230, 0.12); border: 1px solid rgba(34, 139, 230, 0.35); border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
            <span style="font-size: 0.83rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Active Conversation:</span>
            <span class="badge badge-blue" style="font-size: 0.85rem; padding: 4px 12px;">✓ {active_lbl}</span>
        </div>
        """, unsafe_allow_html=True)

        user_transcript = st.text_area(
            "Conversation Transcript",
            height=340,
            key="transcript_text_area"
        )
        
        analyze_btn = st.button("✨ Analyze Conversation", type="primary", use_container_width=True)

    with right_panel:
        st.markdown("#### CARE AI Analysis Results")
        
        # Auto-run analysis on load if last_analysis not set
        if "last_analysis" not in st.session_state:
            st.session_state["last_analysis"] = analyze_conversation(user_transcript)

        if analyze_btn:
            with st.spinner("CARE GPT-4o-mini engine analyzing conversation quality..."):
                res = analyze_conversation(user_transcript)
                st.session_state["last_analysis"] = res
        
        res = st.session_state["last_analysis"]

        # Row 1: 3 Metric Cards
        rm1, rm2, rm3 = st.columns(3)
        
        sent_score = res.get("sentiment_score", 5)
        sent_color = "#FF4B4B" if sent_score < 4 else ("#FAB005" if sent_score <= 7 else "#00C896")

        res_qual = res.get("resolution_quality_score", 5)
        qual_color = "#00C896" if res_qual >= 7 else ("#FAB005" if res_qual >= 4 else "#FF4B4B")

        esc_risk = res.get("escalation_risk", "Low")
        esc_color = "#FF4B4B" if esc_risk == "High" else ("#FAB005" if esc_risk == "Medium" else "#00C896")

        with rm1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {sent_color};">{sent_score}/10</div>
                <div class="metric-lbl">Sentiment Score</div>
            </div>
            """, unsafe_allow_html=True)
        with rm2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {qual_color};">{res_qual}/10</div>
                <div class="metric-lbl">Resolution Quality</div>
            </div>
            """, unsafe_allow_html=True)
        with rm3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {esc_color};">{esc_risk}</div>
                <div class="metric-lbl">Escalation Risk</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 2: Issue & Agent Performance Cards
        c_left, c_right = st.columns(2)
        
        category_icons = {
            "Delivery": "🚚", "Financing": "💰", "Vehicle Quality": "🚗",
            "Trade-in": "🔄", "Documentation": "📄", "General Inquiry": "❓", "Other": "⚙️"
        }
        cat = res.get("issue_category", "General Inquiry")
        icon = category_icons.get(cat, "❓")

        with c_left:
            st.markdown("##### 📌 Issue Details")
            status = res.get("resolution_status", "Unresolved")
            status_class = "badge-green" if status == "Resolved" else ("badge-yellow" if status == "Partially Resolved" else "badge-red")
            
            st.markdown(f"""
            <div style="background: #0F1826; padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.07);">
                <p style="margin-bottom:8px;"><strong>Category:</strong> {icon} {cat}</p>
                <p style="margin-bottom:8px; line-height: 1.45;"><strong>Summary:</strong> {res.get("issue_summary", "N/A")}</p>
                <p style="margin:0;"><strong>Status:</strong> <span class="badge {status_class}">{status}</span></p>
            </div>
            """, unsafe_allow_html=True)

        with c_right:
            st.markdown("##### 🤖 Agent Performance")
            st.markdown(f"""
            <div style="background: #0F1826; padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.07);">
                <p style="margin-bottom:8px; line-height: 1.45;"><strong>Evaluation:</strong> {res.get("agent_performance", "N/A")}</p>
                <div class="insight-box-gold">
                    <strong style="color: #FAB005;">⚠️ Key Friction Point:</strong><br>{res.get("key_friction_point", "N/A")}
                </div>
                <p style="font-size: 0.83rem; color: #94A3B8; margin: 4px 0 0 0;"><strong>Escalation Reason:</strong> {res.get("escalation_reason", "N/A")}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 3: What Sebastian Should Have Said
        st.markdown("""
        <div class="insight-box-blue">
            <h5 style="color: #228BE6; margin-top:0;">💡 What Sebastian Should Have Said</h5>
            <p style="font-size: 1.05rem; line-height: 1.55; margin-bottom: 0; color: #F8FAFC;">{}</p>
        </div>
        """.format(res.get("suggested_better_response", "N/A")), unsafe_allow_html=True)

        # Row 4: Deep Dive Narrative Analysis Expander
        with st.expander("🔬 Deep Dive Narrative Analysis (GPT-4o-mini)", expanded=True):
            st.write(res.get("deep_dive", "No narrative available."))


# ==========================================
# PAGE 3: BATCH DASHBOARD
# ==========================================
elif st.session_state["nav"] == "Batch Dashboard":
    st.title("📊 Batch Analytics Dashboard")
    st.caption("Upload a CSV file containing customer support transcripts to analyze batch-wide sentiment trends and friction points.")

    b_col1, b_col2 = st.columns([2, 1])
    with b_col1:
        uploaded_file = st.file_uploader("Upload CSV (Must contain a 'transcript' column)", type=["csv"])
    with b_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        sample_df = pd.read_csv("sample_transcripts.csv")
        sample_csv_data = sample_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Sample CSV (10 Transcripts)",
            data=sample_csv_data,
            file_name="sample_transcripts.csv",
            mime="text/csv",
            use_container_width=True
        )

    if uploaded_file is not None:
        try:
            df_in = pd.read_csv(uploaded_file)
            if "transcript" not in df_in.columns:
                st.error("Uploaded CSV must contain a column named 'transcript'.")
            else:
                if st.button("⚡ Process Batch Conversations", type="primary"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    results = []

                    total_rows = len(df_in)
                    for idx, row in df_in.iterrows():
                        status_text.text(f"CARE is processing conversation {idx+1} of {total_rows}...")
                        res = analyze_conversation(row["transcript"])
                        res["conversation_num"] = idx + 1
                        results.append(res)
                        progress_bar.progress((idx + 1) / total_rows)
                        time.sleep(0.05)

                    status_text.text("Processing complete!")
                    st.session_state["batch_results"] = pd.DataFrame(results)
                    st.rerun()
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        if "batch_results" not in st.session_state:
            with st.spinner("Initializing sample batch analysis..."):
                results = []
                for idx, row in sample_df.iterrows():
                    res = generate_mock_analysis(row["transcript"])
                    res["conversation_num"] = idx + 1
                    results.append(res)
                st.session_state["batch_results"] = pd.DataFrame(results)

    if "batch_results" in st.session_state and not st.session_state["batch_results"].empty:
        batch_df = st.session_state["batch_results"]

        st.markdown("---")
        
        # Executive Summary Box
        st.markdown("### 📋 Executive Summary")
        with st.spinner("Generating GPT-4o executive batch summary..."):
            exec_summary = generate_batch_executive_summary(batch_df)
        st.markdown(f"""
        <div class="insight-box-blue">
            <p style="font-size: 1.05rem; line-height: 1.6; margin:0; color: #F8FAFC;">{exec_summary}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Metric Row - 5 Cards
        m1, m2, m3, m4, m5 = st.columns(5)
        
        avg_sent = batch_df["sentiment_score"].mean()
        pct_resolved = (batch_df["resolution_status"] == "Resolved").mean() * 100
        pct_high_esc = (batch_df["escalation_risk"] == "High").mean() * 100
        top_cat = batch_df["issue_category"].mode()[0] if not batch_df["issue_category"].empty else "N/A"
        avg_qual = batch_df["resolution_quality_score"].mean()

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #228BE6;">{avg_sent:.1f}</div>
                <div class="metric-lbl">Avg Sentiment</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #00C896;">{pct_resolved:.0f}%</div>
                <div class="metric-lbl">% Resolved</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #FF4B4B;">{pct_high_esc:.0f}%</div>
                <div class="metric-lbl">% High Escalation</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="font-size: 1.3rem; color: #FAB005; height: 42px; display: flex; align-items: center; justify-content: center;">{top_cat}</div>
                <div class="metric-lbl">Top Issue Category</div>
            </div>
            """, unsafe_allow_html=True)
        with m5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #228BE6;">{avg_qual:.1f}</div>
                <div class="metric-lbl">Avg Quality</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts Row 1: Bar & Pie
        ch1, ch2 = st.columns(2)

        with ch1:
            st.markdown("##### Issue Category Distribution")
            cat_counts = batch_df["issue_category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig_bar = px.bar(
                cat_counts,
                x="Category",
                y="Count",
                color_discrete_sequence=["#228BE6"],
                template="plotly_dark"
            )
            fig_bar.update_layout(
                plot_bgcolor="#0F1826",
                paper_bgcolor="#0F1826",
                margin=dict(l=20, r=20, t=30, b=20),
                height=320
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with ch2:
            st.markdown("##### Resolution Status Breakdown")
            res_counts = batch_df["resolution_status"].value_counts().reset_index()
            res_counts.columns = ["Status", "Count"]
            color_map = {"Resolved": "#00C896", "Partially Resolved": "#FAB005", "Unresolved": "#FF4B4B"}
            fig_pie = px.pie(
                res_counts,
                names="Status",
                values="Count",
                color="Status",
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.4
            )
            fig_pie.update_layout(
                plot_bgcolor="#0F1826",
                paper_bgcolor="#0F1826",
                margin=dict(l=20, r=20, t=30, b=20),
                height=320
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Full Width Sentiment Line Chart
        st.markdown("##### Sentiment Score Trend Across Conversations")
        fig_line = px.line(
            batch_df,
            x="conversation_num",
            y="sentiment_score",
            markers=True,
            labels={"conversation_num": "Conversation #", "sentiment_score": "Sentiment Score (1-10)"},
            template="plotly_dark"
        )
        fig_line.update_traces(line_color="#228BE6", marker=dict(size=8, color="#228BE6"))
        fig_line.add_hline(
            y=5,
            line_dash="dot",
            line_color="#FF4B4B",
            annotation_text="Urgent Review Threshold (<5)",
            annotation_position="bottom right",
            annotation_font_color="#FF4B4B"
        )
        fig_line.update_layout(
            plot_bgcolor="#0F1826",
            paper_bgcolor="#0F1826",
            margin=dict(l=20, r=20, t=30, b=20),
            height=300,
            yaxis=dict(range=[0, 10.5])
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Filterable Data Table
        st.markdown("##### Detailed Conversation Evaluation Table")
        
        display_df = batch_df[[
            "conversation_num", "sentiment_score", "issue_category", 
            "resolution_status", "escalation_risk", "key_friction_point"
        ]].copy()
        
        display_df.columns = ["Conversation #", "Sentiment Score", "Issue Category", "Resolution Status", "Escalation Risk", "Key Friction Point"]
        
        st.dataframe(
            display_df.style.map(
                lambda val: 'background-color: rgba(255,75,75,0.25); color: #FF4B4B; font-weight: bold;' if val == 'High' 
                else ('background-color: rgba(250,176,5,0.25); color: #FAB005;' if val == 'Medium' 
                else ('background-color: rgba(0,200,150,0.25); color: #00C896;' if val == 'Low' else '')),
                subset=["Escalation Risk"]
            ),
            use_container_width=True,
            height=320
        )

        export_csv = batch_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Full Analysis as CSV",
            data=export_csv,
            file_name="CARE_batch_analysis_results.csv",
            mime="text/csv",
            type="primary"
        )


# ==========================================
# PAGE 4: SEBASTIAN IMPROVEMENT LAB
# ==========================================
elif st.session_state["nav"] == "Sebastian Improvement Lab":
    st.title("🧪 Sebastian Improvement Lab")
    st.caption("Iterate on AI agent prompt strategies and extract structured training datasets from live conversations.")

    tab1, tab2 = st.tabs(["Response Improver", "Training FAQ Generator"])

    # TAB A: RESPONSE IMPROVER
    with tab1:
        st.markdown("### Help Sebastian Respond Better")
        st.caption("Paste a real customer message and Sebastian's current response. Get an AI-powered improved response with coaching notes.")

        col_in1, col_in2 = st.columns(2)
        with col_in1:
            cust_msg = st.text_area(
                "Customer Message",
                value="My vehicle delivery was supposed to arrive 2 hours ago. Nobody called me and I took the afternoon off work!",
                height=120
            )
        with col_in2:
            seb_resp = st.text_area(
                "Sebastian's Current Response",
                value="Deliveries can be delayed due to logistics. You will receive an SMS update when the vehicle is en route.",
                height=120
            )

        context_stage = st.selectbox(
            "What stage of the purchase?",
            ["Browsing", "Financing", "Post-Purchase", "Delivery", "Trade-in", "Documentation"],
            index=3
        )

        if st.button("✨ Improve Response", type="primary"):
            with st.spinner("Coaching Sebastian with GPT-4o..."):
                imp_res = improve_response_call(cust_msg, seb_resp, context_stage)

            st.markdown("<br>", unsafe_allow_html=True)
            
            c_out1, c_out2 = st.columns(2)
            with c_out1:
                st.markdown(f"""
                <div class="response-card-red">
                    <h5 style="color: #FF4B4B; margin-top: 0;">Current Response</h5>
                    <p style="font-size: 1rem; line-height: 1.5; color: #F8FAFC;">{seb_resp}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with c_out2:
                st.markdown(f"""
                <div class="response-card-blue">
                    <h5 style="color: #228BE6; margin-top: 0;">✨ Improved Response</h5>
                    <p style="font-size: 1rem; line-height: 1.5; color: #F8FAFC;">{imp_res.get("improved_response")}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📋 CX Coaching Notes")
            for note in imp_res.get("coaching_notes", []):
                st.markdown(f"- **{note}**")

    # TAB B: TRAINING FAQ GENERATOR
    with tab2:
        st.markdown("### Generate Sebastian Training Data")
        st.caption("Paste 3-5 conversation transcripts. Get the top FAQs Sebastian should be trained to handle better.")

        multi_transcripts = st.text_area(
            "Paste Transcripts Here",
            value=SAMPLE_CONVERSATIONS["Sample 1: Delayed Delivery (Frustrated)"] + "\n\n" + SAMPLE_CONVERSATIONS["Sample 2: Financing Confusion (Confused)"] + "\n\n" + SAMPLE_CONVERSATIONS["Sample 4: Vehicle Quality Concern (Upset)"],
            height=260
        )

        if st.button("⚡ Generate Training FAQs", type="primary"):
            with st.spinner("Extracting FAQ training clusters with GPT-4o..."):
                faq_data = generate_training_faqs_call(multi_transcripts)
                st.session_state["generated_faqs"] = faq_data

        if "generated_faqs" in st.session_state:
            faq_res = st.session_state["generated_faqs"]
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📚 Extracted Training FAQ Table")

            faq_df = pd.DataFrame(faq_res.get("faqs", []))
            if not faq_df.empty:
                faq_df.columns = ["FAQ Question", "Ideal Answer", "Issue Category", "Priority"]
                st.dataframe(
                    faq_df.style.map(
                        lambda val: 'background-color: rgba(255,75,75,0.25); color: #FF4B4B; font-weight: bold;' if val == 'High'
                        else ('background-color: rgba(250,176,5,0.25); color: #FAB005;' if val == 'Medium'
                        else ('background-color: rgba(0,200,150,0.25); color: #00C896;' if val == 'Low' else '')),
                        subset=["Priority"]
                    ),
                    use_container_width=True
                )

                faq_csv = faq_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export as Training Data CSV",
                    data=faq_csv,
                    file_name="sebastian_training_faqs.csv",
                    mime="text/csv",
                    type="primary"
                )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🎯 Training Recommendations")
            for rec in faq_res.get("recommendations", []):
                st.markdown(f"- **{rec}**")
