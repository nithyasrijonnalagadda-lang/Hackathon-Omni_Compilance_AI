import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
import requests
from streamlit_lottie import st_lottie

# 1. High-End Page Configuration & Premium Cyberpunk/Dark Styling
st.set_page_config(page_title="OmniCompliance AI", page_icon="🛡️", layout="wide")

def load_lottieurl(url: str):
    try:
        # Using a highly reliable, heavily cached public Lottie JSON URL
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

# Aesthetic, premium data-scanning/shield loop animation
lottie_url = "https://assets10.lottiefiles.com/packages/lf20_5tl1vbyu.json"
lottie_ai_scanner = load_lottieurl(lottie_url)

# Aggressive CSS Injection - Overriding Streamlit's core layout framework directly
st.markdown("""
    <style>
    /* Force completely custom background across the entire app window */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%) !important;
    }
    
    /* Sleek Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 15, 30, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* High-End Tech Gradient Title */
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        font-family: 'Inter', system-ui, sans-serif;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #9b51e0 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    
    /* Modern UI Input adjustments */
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
    }
    
    /* Premium Glassomorphic Result Box with glowing accent link border */
    .report-box { 
        padding: 35px; 
        border-radius: 18px; 
        background: rgba(17, 24, 39, 0.5) !important; 
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.1); 
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.15);
        color: #f1f5f9 !important;
    }
    
    .report-box h1, .report-box h2, .report-box h3 { 
        color: #00f2fe !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Render Custom Headings
st.markdown("<h1 class='hero-title'>🛡️ OmniCompliance AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.2rem; margin-top:5px; margin-bottom: 25px;'>Autonomous Multi-Agent Incident Response &amp; Compliance Orchestrator</p>", unsafe_allow_html=True)
st.write("Input a high-risk industry incident below. Our specialized AI agent swarm will handle legal compliance, HR procedures, and client communication simultaneously.")

# 2. Sidebar Configurations for Gemini
st.sidebar.header("🔑 Configuration")
backend_secret_key = st.secrets.get("GEMINI_API_KEY", "")

api_key_input = st.sidebar.text_input(
    "Enter Gemini API Key (Optional for Judges)", 
    type="password",
    placeholder="Using backend deployment key..." if backend_secret_key else ""
)

final_api_key = api_key_input if api_key_input.strip() else backend_secret_key
gemini_llm = None

if not final_api_key:
    st.info("Please enter your Gemini API Key in the sidebar to activate the agents.")
else:
    gemini_llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=final_api_key,
        temperature=0.4
    )

# 3. User Input Section
st.markdown("### 🚨 Step 1: Report the Incident")
incident_input = st.text_area(
    "Describe the incident in plain text (Include location, what happened, who was involved, and severity):",
    placeholder="Example: At 10:30 AM in Manufacturing Plant Floor B, Sensor 4B overheated...",
    height=150
)

if st.button("🔥 Initialize Agent Swarm Execution", type="primary"):
    if not final_api_key:
        st.error("Cannot run execution without a valid Gemini API Key.")
    elif not incident_input.strip():
        st.error("Please provide an incident description first.")
    else:
        # 4. Defining Agents
        legal_agent = Agent(
            role='Chief Legal Compliance Officer',
            goal='Analyze incidents for regulatory impact, legal compliance violations, and strict reporting deadlines.',
            backstory='You are an expert corporate attorney specialized in industrial safety regulations, OSHA compliance, and legal liability mitigation.',
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

        hr_agent = Agent(
            role='Director of HR and Employee Safety',
            goal='Ensure employee welfare, outline immediate medical/insurance workflows, and guide management on worker protocols.',
            backstory='You are a seasoned HR executive focused on workplace safety protocols and employee care.',
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

        pr_agent = Agent(
            role='VP of B2B Client Relations and PR Strategy',
            goal='Draft diplomatic, accurate communications for corporate clients affected by downstream supply chain or service delays.',
            backstory='You are a master communicator who handles high-stakes enterprise client relations.',
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

        orchestrator_agent = Agent(
            role='Executive Incident Commander',
            goal='Consolidate and synthesize the specialized reports from Legal, HR, and PR into a master executive brief.',
            backstory='You are the crisis manager. You review departmental drafts and organize them into an execution report.',
            verbose=True,
            allow_delegation=True,
            llm=gemini_llm
        )

        # 5. Defining Tasks
        task_legal = Task(
            description=f"Analyze this incident: '{incident_input}'. Identify potential regulatory infractions (e.g., OSHA). Note mandatory legal deadlines.",
            expected_output="A structured Legal Vulnerability and Regulatory Compliance report.",
            agent=legal_agent
        )

        task_hr = Task(
            description=f"Analyze this incident: '{incident_input}'. Outline immediate next steps for HR, worker care, and supervisor checklists.",
            expected_output="An HR Action Plan and Supervisor Safety Compliance Checklist.",
            agent=hr_agent
        )

        task_pr = Task(
            description=f"Analyze this incident: '{incident_input}'. Draft a professional, reassuring B2B email notice to clients explaining adjustments without claiming liability.",
            expected_output="A ready-to-send professional email draft.",
            agent=pr_agent
        )

        task_orchestration = Task(
            description="Gather outputs from Legal, HR, and PR. Synthesize them into one beautifully organized Executive Incident Brief containing clear Markdown headings.",
            expected_output="A complete Markdown Executive Incident Brief summarizing sections from all departments.",
            agent=orchestrator_agent
        )

        # 6. Kick off the Swarm Execution with Visible Animation Containers
        # Place the loading animation clearly on the main layout page layout block
        anim_container = st.container()
        with anim_container:
            if lottie_ai_scanner:
                st_lottie(lottie_ai_scanner, height=250, key="swarm_animation")
            else:
                st.warning("⚠️ High-end animation loading fallback applied. Processing data context...")

        with st.spinner("🕵️ Swarm Agents are actively collaborating, generating operational frameworks..."):
            incident_crew = Crew(
                agents=[legal_agent, hr_agent, pr_agent, orchestrator_agent],
                tasks=[task_legal, task_hr, task_pr, task_orchestration],
                process=Process.sequential, 
                verbose=True
            )
            crew_output = incident_crew.kickoff()
            result_text = getattr(crew_output, 'raw', str(crew_output))
        
        # Clear the animation placeholder once execution is complete
        anim_container.empty()

        # 7. Rendering final premium dashboard view
        st.success("✅ Agent Swarm successfully completed crisis workflow execution!")
        st.markdown("### 📋 Generated Executive Summary Dashboard")
        
        st.markdown(f"<div class='report-box'>", unsafe_allow_html=True)
        st.markdown(result_text)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Download Executive Incident Brief (Markdown File)",
            data=result_text,
            file_name="Executive_Incident_Brief.md",
            mime="text/markdown"
        )
