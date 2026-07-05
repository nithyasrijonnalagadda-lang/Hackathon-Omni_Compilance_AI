import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

# 1. Page Configuration & Styling
st.set_page_config(page_title="OmniCompliance AI", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .report-box { 
        padding: 25px; 
        border-radius: 10px; 
        background-color: #f8f9fa; 
        border-left: 5px solid #007bff; 
        margin-bottom: 20px; 
        color: #333333; 
    }
    .report-box h1, .report-box h2, .report-box h3 { color: #111111; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ OmniCompliance AI")
st.subheader("Autonomous Multi-Agent Incident Response & Compliance Orchestrator")
st.write("Input a high-risk industry incident below. Our specialized AI agent swarm will handle legal compliance, HR procedures, and client communication simultaneously.")

# 2. Sidebar Configurations for Gemini
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("Please enter your Gemini API Key in the sidebar to activate the agents.")
else:
    # Initialize the Gemini Model using CrewAI's LLM class
    gemini_llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=api_key,
        temperature=0.4
    )

    # 3. User Input Section
    st.markdown("### 🚨 Step 1: Report the Incident")
    incident_input = st.text_area(
        "Describe the incident in plain text (Include location, what happened, who was involved, and severity):",
        placeholder="Example: At 10:30 AM in Manufacturing Plant Floor B, Sensor 4B overheated, leaking minor chemical coolant. Operator John Doe sustained a first-degree chemical burn on his forearm while attempting to close the secondary valve. The area has been evacuated, but shipments from B2B Client 'Apex Logistics' might experience a 24-hour dispatch delay.",
        height=150
    )

    if st.button("🔥 Initialize Agent Swarm Execution", type="primary"):
        if not incident_input.strip():
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
            
            # Using st.markdown inside our styled box wrapper to make sure text prints natively
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