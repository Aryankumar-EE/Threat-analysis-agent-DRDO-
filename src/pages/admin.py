import streamlit as st
import json
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from workflow.graph import graph
from agents.retrieval_agent import load_dataset

st.set_page_config(
    page_title="DRDO Intelligent Safety Guard",
    page_icon="🛡️",
    layout="wide"
)
if "knowledge_loaded" not in st.session_state:

    st.session_state.knowledge_loaded = False
st.markdown("""
<style>

.stApp{
background-color:#071330;
}

[data-testid="stMetric"]{
background:#102A54;
border:1px solid #3B82F6;
padding:20px;
border-radius:15px;
box-shadow:0 0 15px rgba(59,130,246,.3);
}

.stTabs [data-baseweb="tab"]{
font-size:18px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background: linear-gradient(90deg,#0f172a,#1e3a8a);
border:1px solid #334155;
">

<h3>🇮🇳 AI-Powered Multi-Agent Threat Intelligence & Decision Support System</h3>

<p>
Extraction Agent • Retrieval Agent • Verification Agent • Threat Scoring • Recommendations • Executive Reporting
</p>

</div>
""", unsafe_allow_html=True)



st.title("🛡️ DRDO Intelligent Safety Guard")
st.subheader("Multi-Agent Threat Intelligence System")
st.sidebar.title("🛡️ Command Center")

st.sidebar.success("System Online")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Workflow

📄 Incident

⬇️

🤖 Extraction Agent

⬇️

🔍 Retrieval Agent

⬇️

✅ Verification Agent

⬇️

⚠️ Threat Agent

⬇️

🛡️ Recommendation Agent

⬇️

📑 Report Agent
""")

st.sidebar.write("🤖 Agents : 6")
st.sidebar.write("🧠 LLM : Llama 3.1")
st.sidebar.write("📂 Incidents : 80")
st.sidebar.write("🗄️ Vector DB : FAISS")
st.sidebar.write("🔄 Framework : LangGraph")

st.sidebar.markdown("---")

st.sidebar.info(
    "AI-Powered Threat Intelligence & Decision Support"
)

st.sidebar.success("🟢 Online")

st.sidebar.write("Agents Active: 6")
st.sidebar.write("Framework: LangGraph")
st.sidebar.write("Vector DB: FAISS")
st.sidebar.write("LLM: Llama 3.1")
st.sidebar.write("Dataset: 80 Incidents")

# ==========================================
# STEP 1 : HISTORICAL DATASET
# ==========================================

st.header("📚 Step 1 : Load Historical Knowledge Base")

dataset_file = st.file_uploader(
    "Upload Historical Dataset",
    type=["json"],
    key="dataset"
)

dataset_loaded = False

if dataset_file:

    dataset = json.load(dataset_file)

    if not st.session_state.knowledge_loaded:

       load_dataset(dataset)

       st.session_state.knowledge_loaded = True

    dataset_loaded = True

    if st.session_state.knowledge_loaded:

      st.success(
         f"Knowledge Base Ready ({len(dataset)} incidents)"
      )

st.divider()

# ==========================================
# STEP 2 : NEW INCIDENT
# ==========================================

st.header("🚨 Step 2 : Upload New Incident")

uploaded_file = st.file_uploader(
    "Upload New Incident",
    type=["txt","json"],
    key="incident"
)

if uploaded_file:

    if not dataset_loaded:

        st.error(
            "Please load a Historical Dataset first."
        )

        st.stop()

    if uploaded_file.name.endswith(".txt"):

        content = uploaded_file.read().decode("utf-8")

        incident = {
            "doc_id": "UPLOAD001",
            "title": uploaded_file.name,
            "content": content,
            "location": "User Upload"
        }

    else:

        data = json.load(uploaded_file)
        st.write("Type of data:", type(data))

        if isinstance(data, list):
            st.write("First record:")
            st.write(data[0])

        elif isinstance(data, dict):
            st.write("Dictionary keys:")
            st.write(list(data.keys()))

        if isinstance(data, list):

            options = [
                f"{item['doc_id']} - {item.get('title', item.get('event', 'No Title'))}"
                for item in data
            ]

            selected = st.selectbox(
                "Select Incident",
                range(len(options)),
                format_func=lambda i: options[i]
            )

            incident = data[selected]

        else:

            incident = data

    st.success("Incident Loaded Successfully")

    with st.expander("📄 Incident Details"):
      st.json(incident)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
      run_pipeline = st.button(
        "🚀 Run Threat Analysis",
        use_container_width=True
    )

    if run_pipeline:

        with st.spinner("Running Agents..."):

            initial_state = {

                "incident": incident,

                "entities": {},
                "evidence": [],

                "verified_claims": {},
                "confidence_score": 0.0,

                "threat_score": 0.0,
                "severity_level": "",

                "threat_report": {},
                "recommendations": {},

                "report": ""
            }
            result = graph.invoke(initial_state)

        st.success("Pipeline Completed")
        severity = result["severity_level"]

        if severity == "Critical":        

            st.error(
            "🚨 CRITICAL THREAT DETECTED"
    )

        elif severity == "High":        

            st.warning(
                "⚠️ HIGH RISK THREAT DETECTED"
            )

        elif severity == "Medium":

            st.info(
                "📡 MEDIUM RISK THREAT DETECTED"
            )

        else:

            st.success(
                "✅ LOW RISK THREAT DETECTED"
            )
        col1, col2, col3 = st.columns(3)

        with col1:
         st.metric(
          "Threat Score",
           result["threat_score"]
    )

        with col2:
         st.metric(
        "Severity",
        result["severity_level"]
    )

        with col3:
         st.metric(
        "Confidence",
        f"{result.get('confidence_score',0)*100:.0f}%"
    )
         
        st.markdown("## 📊 Threat Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🚨 Threat Score", result["threat_score"])

        with col2:
            st.metric("⚠️ Severity", result["severity_level"])

        with col3:
            st.metric(
                "✅ Confidence",
                f"{result.get('confidence_score',0)*100:.0f}%"
            )

        with col4:
            st.metric(
                "📄 Evidence",
                len(result["evidence"])
            )

        st.divider()         

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            [
                "Entities",
                "Evidence",
                "Verification",
                "Threat",
                "Recommendations",
                "Report"
            ]
        )
        st.info(
        """
        🤖 Agent Mapping

        📌 Entities → Extraction Agent

        📚 Evidence → Retrieval Agent

        ✅ Verification → Verification Agent

        ⚠️ Threat → Threat Scoring Agent

        🛡️ Recommendations → Recommendation Agent

        📄 Report → Report Generation Agent
        """
)

        with tab1:

            st.subheader("Extracted Entities")

            st.json(result["entities"])
            agent_data = pd.DataFrame({

            "Agent": [
                "Extraction",
                "Retrieval",
                "Verification",
                "Threat",
                "Recommendation",
                "Report"
            ],

            "Status": [
                1,
                1,
                1,
                1,
                1,
                1
            ]
        })

        fig = px.bar(
            agent_data,
            x="Agent",
            y="Status",
            title="Agent Execution Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        with tab2:

            st.subheader("Retrieved Evidence")

            for item in result["evidence"]:

                st.write(
                    f"**{item.get('doc_id')}** | "
                    f"{item.get('title')}"
                )
            pie_data = pd.DataFrame({
                "Category": [
                    "Evidence",
                    "Verified Claims",
                 "Recommendations"
                ],
                "Count": [
                    len(result["evidence"]),
                    len(result["verified_claims"]),
                 len(
                     result["recommendations"].get(
                          "immediate_actions",
                          []
                      )
                    )
                ]
            })

            fig = px.pie(
                pie_data,
                values="Count",
                names="Category",
                title="Threat Analysis Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )    

        with tab3:

            st.subheader("Verification")

            st.json(result["verified_claims"])

            st.metric(
                "Confidence Score",
                result.get("confidence_score", 0)
            )

        with tab4:

           st.subheader("Threat Assessment")
           fig = go.Figure(go.Indicator(
                mode="gauge+number",

               value=result["threat_score"],

               title={"text":"Threat Level"},

               gauge={
                   "axis":{"range":[0,10]},

                   "bar":{"color":"red"},

                   "steps":[
                       {"range":[0,3],"color":"green"},
                       {"range":[3,6],"color":"yellow"},
                       {"range":[6,10],"color":"red"}
                   ]
               }
           ))

           st.plotly_chart(
                 fig,
                 use_container_width=True
                 )

           with col1:
                  st.metric(
                  "Threat Score",
                  result["threat_score"]
                    )

           with col2:
                   st.metric(
                   "Severity",
                   result["severity_level"]
                 )

           with col3:
                   st.metric(
                   "Verification Confidence",
                   f"{result.get('confidence_score',0)*100:.0f}%"
             )
                   severity = result["severity_level"]

                   if severity == "Critical":
                    st.error(f"🚨 Severity: {severity}")

                   elif severity == "High":
                    st.warning(f"⚠️ Severity: {severity}")

                   else:
                    st.success(f"✅ Severity: {severity}")
        with tab5:

            st.subheader("Recommendations")

            recommendations = result["recommendations"]

            st.write("### Immediate Actions")

            for action in recommendations.get(
                "immediate_actions",
                []
            ):

                if isinstance(action, dict):

                    st.write(
                        f"✅ {action.get('action')}"
                    )

                else:

                    st.write(f"✅{action}")

            st.write("### Monitoring Tasks")

            for task in recommendations.get(
                "monitoring_tasks",
                []
            ):

                if isinstance(task, dict):

                    st.write(
                        f"📡 {task.get('task')}"
                    )

                else:

                    st.write(f"📡 {task}")

            st.write("### Escalation")

            esc = recommendations.get(
                 "escalation",
                  {}
                  )

            st.error(
               f"""
            🚨 Escalation Required: {esc.get('should_escalate')}

            Team: {esc.get('escalate_to')}

            Urgency: {esc.get('urgency')}

            Reason: {esc.get('reason')}
            """
            )

            st.write("### Risk Mitigation")

            for item in recommendations.get(
                "risk_mitigation",
                []
            ):

                if isinstance(item, dict):

                    st.write(
                        f"🛡️ {item.get('mitigation')}"
                    )

                else:

                    st.write(f"🛡️ {item}")

        with tab6:

            st.subheader("Final Report")

            st.text(result["report"])
            st.download_button(
              label="📥 Download Intelligence Report",
              data=json.dumps(result, indent=4),
              file_name="final_intelligence_report.json",
              mime="application/json"
         )