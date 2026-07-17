import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
import os
import pandas as pd
import time

# 1. High-End Page Configuration & Premium Cyberpunk/Dark Styling
st.set_page_config(page_title="OmniCompliance AI | Control Center", page_icon="🛡️", layout="wide")

# Advanced CSS Injection - Custom Variables, Telemetry Grid, Auth Panel, and Node Aesthetics
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #070a12 0%, #0f172a 60%, #1e1b4b 100%) !important;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(7, 10, 18, 0.8) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(0, 242, 254, 0.15) !important;
    }
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
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
    }
    
    /* Target custom container elements securely */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stCustomComponentV1"]) {
        max-width: 520px;
        margin: 30px auto !important;
    }
    .auth-box-layout {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(0, 242, 254, 0.25) !important;
        padding: 30px !important;
        border-radius: 16px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== AUTHENTICATION INITIALIZATION ====================
if "users_db" not in st.session_state:
    st.session_state.users_db = {"admin": "admin123"}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ==================== AUTHENTICATION INTERFACE ====================
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #00f2fe; font-family: sans-serif; margin-top: 50px;'>🛡️ OMNICOMPLIANCE CORE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 30px;'>Secure Enterprise Sovereign Identity Gateway</p>", unsafe_allow_html=True)
    
    # Restrict total column spans to center the structural fields neatly
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        auth_tab, register_tab = st.tabs(["🔒 Secure Authenticated Sign-In", "📝 Provision New Credentials"])
        
        with auth_tab:
            # Native container with class anchoring for layout containment
            with st.container(border=False):
                st.markdown("<div class='auth-box-layout'>", unsafe_allow_html=True)
                login_user = st.text_input("Identity Alias (Username)", key="login_user_input")
                login_pass = st.text_input("Security Passkey (Password)", type="password", key="login_pass_input")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔓 Access Command Infrastructure", type="primary", use_container_width=True):
                    if login_user in st.session_state.users_db and st.session_state.users_db[login_user] == login_pass:
                        st.session_state.authenticated = True
                        st.session_state.current_user = login_user
                        st.success("Access Granted. Synchronizing cluster matrices...")
                        time.sleep(1.0)
                        st.rerun()
                    else:
                        st.error("Authentication Rejected: Invalid identity tokens.")
                st.markdown("</div>", unsafe_allow_html=True)
            
        with register_tab:
            with st.container(border=False):
                st.markdown("<div class='auth-box-layout'>", unsafe_allow_html=True)
                reg_user = st.text_input("Desired Identity Alias", key="reg_user_input")
                reg_pass = st.text_input("Set Security Passkey", type="password", key="reg_pass_input")
                reg_confirm = st.text_input("Confirm Security Passkey", type="password", key="reg_confirm_input")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🧬 Provision Sovereign Account", use_container_width=True):
                    if not reg_user.strip() or not reg_pass.strip():
                        st.error("Provisioning Aborted: Credentials cannot be empty.")
                    elif reg_user in st.session_state.users_db:
                        st.error("Provisioning Aborted: Identity alias already registered.")
                    elif reg_pass != reg_confirm:
                        st.error("Provisioning Aborted: Passkey verification mismatch.")
                    else:
                        st.session_state.users_db[reg_user] = reg_pass
                        st.success("Identity Provisioned! Switch tab to sign-in.")
                st.markdown("</div>", unsafe_allow_html=True)

else:
    # ==================== PROTECTED SYSTEM WORKSPACE ====================
    st.markdown("<h1 class='hero-title'>🛡️ OmniCompliance AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1.25rem; margin-top:5px; margin-bottom: 30px;'>Autonomous Multi-Agent Crisis Infrastructure &amp; Orchestration Platform</p>", unsafe_allow_html=True)

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

    tab1, tab2, tab3 = st.tabs(["🚨 Incident Command Center", "📊 Swarm Node Topology", "🛡️ Compliance & Audit Vault"])

    backend_secret_key = st.secrets.get("GEMINI_API_KEY", "")

    st.sidebar.markdown(f"👤 **Operator:** `@{st.session_state.current_user}`")
    st.sidebar.header("⚙️ Swarm Core Engine")
    selected_model = st.sidebar.selectbox(
        "Preferred LLM Base Tier",
        ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"],
        index=0
    )

    api_key_input = st.sidebar.text_input(
        "Manual API Token (Optional Override)", 
        type="password",
        placeholder="Using redundant background pool..." if backend_secret_key else ""
    )

    if st.sidebar.button("🔒 Sever Connection (Sign Out)", type="secondary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()

    keys_to_try = []
    if api_key_input.strip():
        keys_to_try = [api_key_input.strip()]
    elif isinstance(backend_secret_key, str) and backend_secret_key.strip():
        keys_to_try = [k.strip() for k in backend_secret_key.split(",") if k.strip()]

    if not keys_to_try:
        st.sidebar.warning("Operational Warning: No active credentials detected.")

    # ==================== TAB 1: OPERATIONAL TERMINAL ====================
    with tab1:
        st.markdown("### 📝 Input Emergency Incident Log")
        incident_input = st.text_area(
            "Paste high-stakes raw text notification logs here:",
            placeholder="Example: At 10:30 AM on Plant Floor B, Sensor 4B overheated...",
            height=160
        )
        
        if incident_input.strip():
            word_count = len(incident_input.split())
            severity_label = "🔴 HIGH CRISIS THREAT" if any(x in incident_input.lower() for x in ["leak", "injured", "fire", "burn", "collapse", "hospital", "overheated"]) else "🟡 ELEVATED RISK PROFILE"
            st.markdown(f"<p style='color:#94a3b8; font-size:0.9rem;'>Pre-Assessment Telemetry: <b>{word_count} words</b> | System Routing Matrix: <span style='color:#f43f5e;'><b>{severity_label}</b></span></p>", unsafe_allow_html=True)

        if st.button("🔥 Execute Enterprise Swarm Pipeline", type="primary"):
            if not keys_to_try:
                st.error("Execution Aborted: Configure credentials.")
            elif not incident_input.strip():
                st.error("Execution Aborted: Incident logs missing.")
            else:
                result_text = None
                execution_successful = False
                
                log_container = st.expander("🛠️ System Core Failover Analytics Matrix", expanded=True)
                
                model_fallback_pool = [selected_model, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"]
                model_fallback_pool = list(dict.fromkeys(model_fallback_pool))
                
                pipeline_broken = False
                
                for operational_model in model_fallback_pool:
                    if execution_successful:
                        break
                        
                    for index, active_key in enumerate(keys_to_try):
                        try:
                            log_container.info(f"⏳ Synchronizing network lanes to clear active concurrency caps...")
                            time.sleep(2.0)
                            
                            os.environ["GEMINI_API_KEY"] = active_key
                            
                            gemini_llm = LLM(
                                model=f"gemini/{operational_model}",
                                api_key=active_key,
                                temperature=0.35
                            )
                            
                            legal_agent = Agent(
                                role='Chief Legal Compliance Officer',
                                goal='Analyze raw incident indicators for regulatory impacts and reporting compliance timelines.',
                                backstory='Elite corporate compliance attorney specialized in mitigating operational liability.',
                                verbose=True, allow_delegation=False, llm=gemini_llm, max_iter=2
                            )

                            hr_agent = Agent(
                                role='Director of HR and Employee Safety',
                                goal='Direct physical employee safety logistics and manage leadership care protocols.',
                                backstory='Senior Executive championing workplace welfare pipelines.',
                                verbose=True, allow_delegation=False, llm=gemini_llm, max_iter=2
                            )

                            pr_agent = Agent(
                                role='VP of B2B Client Relations and PR Strategy',
                                goal='Structure reassuring communications updates for enterprise buyers.',
                                backstory='Crisis communication architect managing client confidence.',
                                verbose=True, allow_delegation=False, llm=gemini_llm, max_iter=2
                            )

                            orchestrator_agent = Agent(
                                role='Executive Incident Commander',
                                goal='Consolidate and synthesize agency inputs into a single boardroom brief.',
                                backstory='Chief Risk Analyst who refines asset portfolios.',
                                verbose=True, allow_delegation=True, llm=gemini_llm, max_iter=2
                            )

                            task_legal = Task(
                                description=f"Analyze input log: {incident_input}. Map regulatory vulnerabilities.",
                                expected_output="Structured Compliance Audit.",
                                agent=legal_agent
                            )

                            task_hr = Task(
                                description=f"Analyze input log: {incident_input}. Define safety checklist protocols.",
                                expected_output="Safety Field Plan.",
                                agent=hr_agent
                            )

                            task_pr = Task(
                                description=f"Analyze input log: {incident_input}. Draft a risk-mitigated buyer update statement.",
                                expected_output="B2B Client Update.",
                                agent=pr_agent
                            )

                            task_orchestration = Task(
                                description="Combine legal, safety, and client communication briefs into a comprehensive Markdown Brief.",
                                expected_output="Executive Incident Brief document with sharp titles.",
                                agent=orchestrator_agent
                            )

                            anim_container = st.empty()
                            anim_container.markdown(f"""
                                <div class='cyber-scanner'>
                                    <h4 style='color: #00f2fe; margin: 0;'>🚀 Active Swarm Cluster Initialized</h4>
                                    <p style='color: #94a3b8; margin: 6px 0 0 0; font-size: 0.95rem;'>Deploying agents on <b>{operational_model}</b> via credential block #{index+1}...</p>
                                </div>
                            """, unsafe_allow_html=True)

                            with st.spinner("Processing Swarm Matrix Logic..."):
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
                            final_model_used = operational_model
                            break
                            
                        except Exception as e:
                            error_str = str(e)
                            anim_container.empty()
                            
                            if any(ind in error_str for ind in ["429", "503", "404", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "NOT_FOUND"]):
                                log_container.warning(f"🔄 Failover Event: {operational_model} (Token #{index+1}) throttled. Switching context routing pathway...")
                                time.sleep(1.5)
                                continue
                            else:
                                log_container.error(f"Internal Interruption: {error_str}")
                                pipeline_broken = True
                                break
                                
                    if pipeline_broken:
                        break
                else:
                    if not execution_successful:
                        st.error("❌ System Infrastructure Alert: All fallback combinations exhausted. Verify status paths or key permissions.")
                    
                if execution_successful and result_text:
                    st.toast("⚡ Security Core Matrix Upgraded to Phase 2.", icon="🛡️")
                    st.toast("🧬 Strategic Vectors Compiled successfully.", icon="⚙️")
                    
                    st.markdown(f"""
                        <div class='tech-upgrade-banner'>
                            <span style='color: #22c55e; font-weight: 800; font-family: monospace; letter-spacing: 1px;'>[🟢 SWARM PIPELINE SECURED VIA {final_model_used.upper()}]</span>
                            <p style='color: #ffffff; margin: 6px 0 0 0; font-size: 1.05rem;'>Dynamic context compilation completed. Structured payload successfully generated.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 📋 System Synthesis Output Panel")
                    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
                    st.markdown(result_text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # --- Multi-Format Export Matrix Section ---
                    st.markdown("#### 📥 Export Sovereign Incident Assets")
                    
                    plain_text = result_text.replace("#", "").replace("**", "").replace("`", "")
                    
                    html_content = ""
                    for line in result_text.split('\n'):
                        stripped = line.strip()
                        if stripped.startswith('### '):
                            html_content += f"<h3>{stripped[4:]}</h3>\n"
                        elif stripped.startswith('## '):
                            html_content += f"<h2>{stripped[3:]}</h2>\n"
                        elif stripped.startswith('# '):
                            html_content += f"<h1>{stripped[2:]}</h1>\n"
                        elif stripped.startswith('* ') or stripped.startswith('- '):
                            html_content += f"<li>{stripped[2:]}</li>\n"
                        elif stripped:
                            temp_line = stripped
                            while "**" in temp_line:
                                temp_line = temp_line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
                            html_content += f"<p>{temp_line}</p>\n"
                        else:
                            html_content += "<br>\n"
                    
                    html_document = f"""<!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>OmniCompliance AI - Executive Incident Brief</title>
                        <style>
                            body {{
                                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                                line-height: 1.6;
                                color: #1e293b;
                                max-width: 800px;
                                margin: 40px auto;
                                padding: 0 20px;
                                background-color: #f8fafc;
                            }}
                            .container {{
                                background: #ffffff;
                                padding: 40px;
                                border-radius: 8px;
                                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
                                border-top: 6px solid #00f2fe;
                            }}
                            h1, h2, h3 {{ color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
                            code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
                            pre {{ background: #f1f5f9; padding: 15px; border-radius: 6px; overflow-x: auto; }}
                            li {{ margin-bottom: 6px; color: #334155; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            {html_content}
                        </div>
                    </body>
                    </html>
                    """

                    dl_col1, dl_col2, dl_col3 = st.columns(3)
                    
                    with dl_col1:
                        st.download_button(
                            label="📄 Download Plain Text (.txt)",
                            data=plain_text,
                            file_name="OmniCompliance_Executive_Brief.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with dl_col2:
                        st.download_button(
                            label="🌐 Download Web Document (.html)",
                            data=html_document,
                            file_name="OmniCompliance_Executive_Brief.html",
                            mime="text/html",
                            use_container_width=True
                        )
                        
                    with dl_col3:
                        st.download_button(
                            label="💻 Download Developer Markdown (.md)",
                            data=result_text,
                            file_name="OmniCompliance_Executive_Brief.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

    # ==================== TAB 2: ARCHITECTURE BLUEPRINT ====================
    with tab2:
        st.markdown("### 🗺️ Multi-Agent Swarm Communication Blueprint")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("""
            <div class='node-card'>
                <div class='node-header'>⚖️ 1. Legal Compliance Node</div>
            </div>
            <div class='node-card'>
                <div class='node-header'>🏥 2. HR Safety Node</div>
            </div>
            <div class='node-card'>
                <div class='node-header'>📢 3. B2B Communications Node</div>
            </div>
            <div class='node-card' style='border-color: #a855f7;'>
                <div class='node-header' style='color:#a855f7;'>👑 4. Executive Orchestrator Node</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.code("""
[ Raw Text Incident Input ] ──► [ Specialized Sub-Agents ] ──► [ Executive Orchestrator Synthesis ]
            """, language="text")

    # ==================== TAB 3: AUDIT VAULT ====================
    with tab3:
        st.markdown("### 🗄️ Enterprise Incident Audit Ledger")
        mock_ledger_data = pd.DataFrame({
            "Incident ID": ["OC-2026-8891", "OC-2026-7742"],
            "Timestamp": ["2026-07-15 09:30", "2026-06-12 14:10"],
            "Facility Context": ["Manufacturing Unit B", "Logistics Hub East"],
            "Risk Profile Tier": ["High", "Medium"]
        })
        st.dataframe(mock_ledger_data, use_container_width=True)
