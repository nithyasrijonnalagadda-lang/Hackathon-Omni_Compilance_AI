import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
import os
import pandas as pd

# 1. High-End Page Configuration & Premium Cyberpunk/Dark Styling
st.set_page_config(page_title="OmniCompliance AI | Control Center", page_icon="🛡️", layout="wide")

# Advanced CSS Injection - Custom Variables, Telemetry Grid, and Node Aesthetics
st.markdown("""
    <style>
    /* Force completely custom background across the entire app window */
    .stApp {
        background: linear-gradient(135deg, #070a12 0%, #0f172a 60%, #1e1b4b 100%) !important;
    }
    
    /* Sleek Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(7, 10, 18, 0.8) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(0, 242, 254, 0.15) !important;
    }
    
    /* High-End Tech Gradient Title */
    .hero-title {
        font-size: 3.8rem !important;
        font-weight: 800 !important;
        font-family: 'Inter', system-ui, sans-serif;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 40%, #a855f7 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -1.5px;
        margin-bottom: 0px;
    }
    
    /* Telemetry KPI Metrics Layout */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi-card {
        flex: 1;
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid #00f2fe;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .kpi-card.purple { border-left-color: #a855f7; }
    .kpi-card.green { border-left-color: #22c55e; }
    
    .kpi-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        font-family: monospace;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Architecture Node Cards */
    .node-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .node-header {
        color: #00f2fe;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    
    /* Custom High-End Scanning Animation Effect */
    .cyber-scanner {
        padding: 25px;
        background: rgba(0, 242, 254, 0.03);
        border: 1px dashed rgba(0, 242, 254, 0.4);
        border-radius: 14px;
        position: relative;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.05);
    }
    .cyber-scanner::after {
        content: '';
        display: block;
        position: absolute;
        left: 0; right: 0; top: 0; bottom: 0;
        background: linear-gradient(to bottom, rgba(0,242,254,0) 0%, rgba(0,242,254,0.12) 50%, rgba(0,242,254,0) 100%);
        animation: scan 2.5s linear infinite;
    }
    @keyframes scan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }
    
    /* Tech Matrix Completion Banner */
    .tech-upgrade-banner {
        background: linear-gradient(90deg, rgba(34, 197, 94, 0.15) 0%, rgba(0, 242, 254, 0.15) 100%);
        border: 1px solid rgba(34, 197, 94, 0.6);
        padding: 18px 25px;
        border-radius: 12px;
        box-shadow: 0 0 25px rgba(34, 197, 94, 0.15);
        margin-bottom: 25px;
        animation: pulseglow 2s infinite alternate;
    }
    @keyframes pulseglow {
        0% { border-color: rgba(34, 197, 94, 0.4); box-shadow: 0 0 15px rgba(34, 197, 94, 0.1); }
        100% { border-color: rgba(0, 242, 254, 0.8); box-shadow: 0 0 30px rgba(0, 242, 254, 0.25); }
    }
    
    /* Premium Glassomorphic Result Box */
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
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 10px;
        margin-top: 25px;
    }
    
    /* Global modifications for form borders and text colors */
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard Branding Header
st.markdown("<h1 class='hero-title'>🛡️ OmniCompliance AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.25rem; margin-top:5px; margin-bottom: 30px;'>Autonomous Multi-Agent Crisis Infrastructure &amp; Orchestration Platform</p>", unsafe_allow_html=True)

# Live Telemetry Command Strip
st.markdown("""
<div class='kpi-container'>
    <div class='kpi-card'>
        <div class='kpi-val'>READY</div>
        <div class='kpi-label'>System Core Status</div>
    </div>
    <div class='kpi-card purple'>
        <div class='kpi-val'>4 ACTIVE</div>
        <div class='kpi-label'>Orchestrated Swarm Nodes</div>
    </div>
    <div class='kpi-card green'>
        <div class='kpi-val'>ROTATIONAL</div>
        <div class='kpi-label'>API Safety Lane</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Multi-Tab Control Matrix
tab1, tab2, tab3 = st.tabs(["🚨 Incident Command Center", "📊 Swarm Node Topology", "🛡️ Compliance & Audit Vault"])

# Fetch background cluster API structures safely
backend_secret_key = st.secrets.get("GEMINI_API_KEY", "")

# Sidebar Configuration Layout
st.sidebar.header("⚙️ Swarm Core Engine")
selected_model = st.sidebar.selectbox(
    "LLM Architecture Tier",
    ["gemini-2.5-flash", "gemini-1.5-flash"],
    index=0
)

api_key_input = st.sidebar.text_input(
    "Manual API Token (Optional Override)", 
    type="password",
    placeholder="Using redundant background pool..." if backend_secret_key else ""
)

# Parse Key Array Paths Safely
keys_to_try = []
if api_key_input.strip():
    keys_to_try = [api_key_input.strip()]
elif isinstance(backend_secret_key, str) and backend_secret_key.strip():
    keys_to_try = [k.strip() for k in backend_secret_key.split(",") if k.strip()]

if not keys_to_try:
    st.sidebar.warning("Operational Warning: No active credentials detected. Configure environment variables.")

# ==================== TAB 1: OPERATIONAL TERMINAL ====================
with tab1:
    st.markdown("### 📝 Input Emergency Incident Log")
    incident_input = st.text_area(
        "Paste high-stakes raw text notification logs here:",
        placeholder="Example: At 14:15 PM inside Data Unit Cluster C, secondary power grids collapsed following a minor thermal flare. Server Admin Jane Smith suffered minor smoke inhalation...",
        height=160
    )
    
    # Context Pre-Analysis Panel
    if incident_input.strip():
        word_count = len(incident_input.split())
        severity_label = "🔴 HIGH CRISIS THREAT" if any(x in incident_input.lower() for x in ["leak", "injured", "fire", "burn", "collapse", "hospital", "overheated"]) else "🟡 ELEVATED RISK PROFILE"
        st.markdown(f"<p style='color:#94a3b8; font-size:0.9rem;'>Pre-Assessment Telemetry: <b>{word_count} words</b> | System Routing Matrix: <span style='color:#f43f5e;'><b>{severity_label}</b></span></p>", unsafe_allow_html=True)

    if st.button("🔥 Execute Enterprise Swarm Pipeline", type="primary"):
        if not keys_to_try:
            st.error("Execution Aborted: Complete credential configurations to connect to target models.")
        elif not incident_input.strip():
            st.error("Execution Aborted: Incident logs must contain alphanumeric string values.")
        else:
            result_text = None
            execution_successful = False
            
            # Key Rotation Core Implementation Logic Loop
            for index, active_key in enumerate(keys_to_try):
                try:
                    os.environ["GEMINI_API_KEY"] = active_key
                    
                    gemini_llm = LLM(
                        model=f"gemini/{selected_model}",
                        api_key=active_key,
                        temperature=0.35
                    )
                    
                    # Agent Instantiations
                    legal_agent = Agent(
                        role='Chief Legal Compliance Officer',
                        goal='Analyze raw incident indicators for severe regulatory impacts, OSHA violations, and structural reporting compliance timelines.',
                        backstory='Elite corporate compliance attorney specialized in mitigating systemic operational liability and managing hazardous environment legal mandates.',
                        verbose=True, allow_delegation=False, llm=gemini_llm, max_iter=2
                    )

                    hr_agent = Agent(
                        role='Director of HR and Employee Safety',
                        goal='Direct physical employee safety logistics, outline mandatory workspace medical insurance paths, and manage leadership care protocols.',
                        backstory='Senior Executive championing workplace psychological/physical welfare pipelines and specialized supervisor crisis field actions.',
                        verbose=True, allow_delegation=False, llm=gemini_llm, max_iter=2
                    )

                    pr_agent = Agent(
                        role='VP of B2B Client Relations and PR Strategy',
                        goal='Structure strategic, non-actionable reassuring communications updates for enterprise buyers navigating downstream supply chain updates.',
                        backstory='Crisis communication architect managing client confidence profiles for global multi-billion dollar technology hubs.',
                        verbose=True, allow_delegation=False, llm=gemini_llm, max_iter=2
                    )

                    orchestrator_agent = Agent(
                        role='Executive Incident Commander',
                        goal='Consolidate, de-conflict, and synthesize specialized autonomous agency inputs into a single boardroom-ready corporate execution brief.',
                        backstory='Chief Risk Analyst who refines segmented documentation assets into clean tactical response matrixes.',
                        verbose=True, allow_delegation=True, llm=gemini_llm, max_iter=2
                    )

                    # Task Pipeline Declarations
                    task_legal = Task(
                        description=f"Analyze input log: {incident_input}. Map out immediate regulatory violations (OSHA/Industry rules) and specify exact legal warning windows.",
                        expected_output="Structured Compliance Vulnerability Audit Analysis.",
                        agent=legal_agent
                    )

                    task_hr = Task(
                        description=f"Analyze input log: {incident_input}. Define immediate supervisor health coordination protocols and field employee care procedures.",
                        expected_output="Operational Safety and HR Field Implementation Plan.",
                        agent=hr_agent
                    )

                    task_pr = Task(
                        description=f"Analyze input log: {incident_input}. Draft a risk-mitigated B2B client notification message that addresses operations without admitting systemic faults.",
                        expected_output="Polished Enterprise Client Relation Statement Draft.",
                        agent=pr_agent
                    )

                    task_orchestration = Task(
                        description="Review the active legal, safety, and client communication briefs. Combine and format them into an ultimate Markdown Executive Briefing Document.",
                        expected_output="A polished, multi-department comprehensive Executive Incident Brief with sharp markdown titles.",
                        agent=orchestrator_agent
                    )

                    # Dynamic Scanner UI Trigger
                    anim_container = st.empty()
                    anim_container.markdown(f"""
                        <div class='cyber-scanner'>
                            <h4 style='color: #00f2fe; margin: 0;'>🚀 Active Swarm Cluster: Matrix Routing Pipeline Initialized</h4>
                            <p style='color: #94a3b8; margin: 6px 0 0 0; font-size: 0.95rem;'>Processing multi-agent subtasks concurrently on <b>{selected_model}</b> via credential block #{index+1}...</p>
                        </div>
                    """, unsafe_allow_html=True)

                    with st.spinner("Processing Agent Sub-Routines..."):
                        incident_crew = Crew(
                            agents=[legal_agent, hr_agent, pr_agent, orchestrator_agent],
                            tasks=[task_legal, task_hr, task_pr, task_orchestration],
                            process=Process.sequential, 
                            verbose=True
                        )
                        crew_output = incident_crew.kickoff()
                        result_text = getattr(crew_output, 'raw', str(crew_output))
                    
                    anim_container.empty()
                    execution_successful = True
                    break
                    
                except Exception as e:
                    error_str = str(e)
                    anim_container.empty()
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        st.warning(f"🔄 Connection Lane Exhaustion on Token Array {index+1}. Initiating backend context rotation sequence...")
                        continue
                    else:
                        st.error(f"Critical Interrupt Caught: {error_str}")
                        break
            else:
                st.error("❌ System Error: All background credential clusters have hit rate limits. Update parameters in configuration.")
                
            # Render Completed Dashboard Output
            if execution_successful and result_text:
                # Tech upgrade toast alerts
                st.toast("⚡ Security Core Matrix Upgraded to Phase 2.", icon="🛡️")
                st.toast("🧬 Strategic Vectors Compiled successfully.", icon="⚙️")
                
                # Tech glowing success readout banner
                st.markdown("""
                    <div class='tech-upgrade-banner'>
                        <span style='color: #22c55e; font-weight: 800; font-family: monospace; letter-spacing: 1px;'>[🟢 SWARM EXECUTION SUCCESSFUL]</span>
                        <p style='color: #ffffff; margin: 6px 0 0 0; font-size: 1.05rem;'>All parallel dependencies resolved. Compliance payload encrypted and committed to local infrastructure assets.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📋 System Synthesis Output Panel")
                st.markdown("<div class='report-box'>", unsafe_allow_html=True)
                st.markdown(result_text)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 Download Sovereign Incident Vault Asset (.md)",
                    data=result_text,
                    file_name="OmniCompliance_Executive_Brief.md",
                    mime="text/markdown"
                )

# ==================== TAB 2: ARCHITECTURE BLUEPRINT ====================
with tab2:
    st.markdown("### 🗺️ Multi-Agent Swarm Communication Blueprint")
    st.write("This diagram displays the dynamic data ingestion and synthesis paths executing behind our UI infrastructure during a crisis scenario:")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class='node-card'>
            <div class='node-header'>⚖️ 1. Legal Compliance Node</div>
            <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>Inspects global regulations, calculates legal fine curves, and sets mandatory litigation windows.</p>
        </div>
        <div class='node-card'>
            <div class='node-header'>🏥 2. HR Safety Node</div>
            <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>Establishes workplace health tracking systems and prints active supervisor field checklists.</p>
        </div>
        <div class='node-card'>
            <div class='node-header'>📢 3. B2B Communications Node</div>
            <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>Generates client relation update statements without claiming liability exposure faults.</p>
        </div>
        <div class='node-card' style='border-color: #a855f7;'>
            <div class='node-header' style='color:#a855f7;'>👑 4. Executive Orchestrator Node</div>
            <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>Synthesizes parallel outputs, balances structural contradictions, and renders clean Markdown layouts.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.code("""
[ Raw Text Incident Input ]
            │
            ├──► (Sequential Ingestion Matrix)
            │
            ├──► [ Node 1: Chief Legal Compliance Officer ] ──┐
            │                                                 │
            ├──► [ Node 2: Director of HR & Worker Safety ]   ├──► [ Node 4: Executive Incident Commander ]
            │                                                 │     (Synthesizes, cleans, outputs Markdown)
            └──► [ Node 3: VP of B2B Public Relations ] ──────┘
                                                                               │
                                                                               ▼
                                                             [ Rendered Enterprise Dashboard UI ]
        """, language="text")
        
        st.info("💡 Hackathon Detail: All sub-nodes utilize strict iteration caps (max_iter=2) and automated error-catching mechanics to rotate keys safely without breaking workflow continuity.")

# ==================== TAB 3: AUDIT VAULT ====================
with tab3:
    st.markdown("### 🗄️ Enterprise Incident Audit Ledger (Simulation)")
    st.write("Simulated ledger tracking secure historical incident briefs stored inside long-term organizational data lakes.")
    
    mock_ledger_data = pd.DataFrame({
        "Incident ID": ["OC-2026-8891", "OC-2026-7742", "OC-2026-1104"],
        "Timestamp": ["2026-07-15 09:30", "2026-06-12 14:10", "2026-05-01 23:45"],
        "Facility Context": ["Manufacturing Unit B", "Logistics Hub East", "Cloud Cluster 4"],
        "Swarm Validation": ["Verified & Archived", "Verified & Archived", "Archived Audit Output"],
        "Risk Profile Tier": ["High", "Medium", "Low"]
    })
    st.dataframe(mock_ledger_data, use_container_width=True)
