import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

# 1. High-End Page Configuration & Premium Cyberpunk/Dark Styling
st.set_page_config(page_title="OmniCompliance AI", page_icon="🛡️", layout="wide")

# Premium CSS Injection for high-end animations and layout enhancements
st.markdown("""
    <style>
    /* Global Background and Typography Smoothing */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* Elegant Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Glowing Title Animation */
    .hero-title {
        font-size: 3rem !important;
        font-weight: 700;
        background: linear-gradient(45deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        animation: fadeIn 1.5s ease-in-out;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.25rem;
        margin-bottom: 25px;
        font-weight: 300;
    }

    /* Premium Glassomorphic Dashboard Report Box with subtle pulse glow */
    .report-box { 
        padding: 30px; 
        border-radius: 16px; 
        background: rgba(30, 41, 59, 0.4); 
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08); 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        margin-top: 25px;
        margin-bottom: 25px; 
        color: #e2e8f0;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .report-box:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.15);
    }

    /* Target headers inside markdown outputs to look sharp */
    .report-box h1, .report-box h2, .report-box h3 { 
        color: #38bdf8 !important; 
        font-weight: 600;
        margin-top: 15px;
    }
    
    /* Custom Styling for interactive elements and form fields */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.3);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Smooth fade-in animation keyframe */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# Render Header UI with high-end text gradients
st.markdown("<h1 class='hero-title'>🛡️ OmniCompliance AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Autonomous Multi-Agent Incident Response &amp; Compliance Orchestrator</p>", unsafe_allow_html=True)
st.write("Input a high-risk industry incident below. Our specialized AI agent swarm will handle legal compliance, HR procedures, and client communication simultaneously.")

# 2. Sidebar Configurations for Gemini
st.sidebar.header("🔑 Configuration")

# Check if a secret key exists in your Streamlit Cloud background settings
backend_secret_key = st.secrets.get("GEMINI_API_KEY", "")

# Let users enter a key, but default it to your backend key so it stays hidden but active
api_key_input = st.sidebar.text_input(
    "Enter Gemini API Key (Optional for Judges)", 
    type="password",
    placeholder="Using backend deployment key..." if backend_secret_key else ""
)

# Determine the final key to use (prioritize manual input, fallback to background secret)
final_api_key = api_key_input if api_key_input.strip() else backend_secret_key

gemini_llm = None

if not final_api_key:
    st.info("Please enter your Gemini API Key in the sidebar to activate the agents.")
else:
    # Initialize the Gemini Model using CrewAI's LLM class
    gemini_llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=final_api_key,
        temperature=0.4
    )

# 3. User Input Section
st.markdown("### 🚨 Step 1: Report the Incident")

incident_input = st.text_area(
    "Describe the incident in plain text (Include location, what happened, who was involved, and severity):",
    placeholder="Example: At 10:30 AM in Manufacturing Plant Floor B, Sensor 4B overheated, leaking minor chemical coolant...",
    height=150
)

if st.button("🔥 Initialize Agent Swarm Execution", type="primary"):
    if not final_api_key:
        st.error("Cannot run execution without a valid Gemini API Key. Please insert it in the sidebar or backend settings.")
    elif not incident_input.strip():
        st.error("Please provide an incident description first.")
    else:
        # 4. Defining the 4 Autonomous Agents
        
        # Agent 1: Legal Compliance
        legal_agent = Agent(
            role='Chief Legal Compliance Officer',
            goal='Analyze incidents for regulatory impact, legal compliance violations, and strict reporting deadlines.',
            backstory='You are an expert corporate attorney specialized in industrial safety regulations, OSHA compliance, and legal liability mitigation. You parse incidents to find legal vulnerabilities.',
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

        # Agent 2: HR Safety
        hr_agent = Agent(
            role='Director of HR and Employee Safety',
            goal='Ensure employee welfare, outline immediate medical/insurance workflows, and guide management on worker protocols.',
            backstory='You are a seasoned HR executive focused on workplace safety protocols, internal company policies, and employee care. You prioritize staff well-being and corporate internal policy adherence.',
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

        # Agent 3: PR & Client Support
        pr_agent = Agent(
            role='VP of B2B Client Relations and PR Strategy',
            goal='Draft diplomatic, accurate communications for corporate clients affected by downstream supply chain or service delays.',
            backstory='You are a master communicator who handles high-stakes enterprise client relations. You know exactly how to manage expectations regarding delays without exposing the company to premature legal fault.',
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

        # Agent 4: Chief Orchestrator (The Leader)
        orchestrator_agent = Agent(
            role='Executive Incident Commander',
            goal='Consolidate and synthesize the specialized reports from Legal, HR, and PR into a single, cohesive master executive brief.',
            backstory='You are the crisis manager. You do not do the granular research yourself; instead, you review the compliance, HR, and PR drafts, ensure they do not contradict each other, and organize them into a boardroom-ready execution report.',
            verbose=True,
            allow_delegation=True,
            llm=gemini_llm
        )

        # 5. Defining the Tasks
        task_legal = Task(
            description=f"Analyze this incident: '{incident_input}'. Identify potential regulatory infractions (e.g., OSHA, safety laws). Determine if formal governmental filing is required and note the mandatory legal deadlines.",
            expected_output="A structured Legal Vulnerability and Regulatory Compliance report.",
            agent=legal_agent
        )

        task_hr = Task(
            description=f"Analyze this incident: '{incident_input}'. Outline immediate next steps for HR, worker medical care, employee leave protocols, and supervisor checklists.",
            expected_output="An HR Action Plan and Supervisor Safety Compliance Checklist.",
            agent=hr_agent
        )

        task_pr = Task(
            description=f"Analyze this incident: '{incident_input}'. Draft a professional, reassuring B2B email notice to any affected clients explaining potential operational adjustments or delays without claiming legal liability.",
            expected_output="A ready-to-send professional email draft meant for enterprise clients.",
            agent=pr_agent
        )

        task_orchestration = Task(
            description="Gather outputs from the Legal Task, HR Task, and PR Task. Review them for completeness. Synthesize them into one beautifully organized Executive Incident Brief containing clear Markdown headings.",
            expected_output="A complete, single consolidated Markdown Executive Incident Brief summarizing sections from all departments.",
            agent=orchestrator_agent
        )

        # 6. Kick off the Swarm Execution
        with st.spinner("🕵️ Agents are collaborating, verifying details, and generating legal/HR frameworks... Please wait..."):
            
            # Assemble the Crew
            incident_crew = Crew(
                agents=[legal_agent, hr_agent, pr_agent, orchestrator_agent],
                tasks=[task_legal, task_hr, task_pr, task_orchestration],
                process=Process.sequential, 
                verbose=True
            )
            
            # Execute the workflow
            crew_output = incident_crew.kickoff()
            
            # Safely extract text result from CrewOutput
            result_text = getattr(crew_output, 'raw', str(crew_output))

        # 7. Rendering the Results beautifully on the Dashboard
        st.success("✅ Agent Swarm successfully executed and resolved the workflow!")
        st.markdown("### 📋 Generated Executive Summary Dashboard")
        
        # Using st.markdown inside our premium styled box wrapper
        st.markdown(f"<div class='report-box'>", unsafe_allow_html=True)
        st.markdown(result_text)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Download Button for the Report
        st.download_button(
            label="📥 Download Executive Incident Brief (Markdown File)",
            data=result_text,
            file_name="Executive_Incident_Brief.md",
            mime="text/markdown"
        )
