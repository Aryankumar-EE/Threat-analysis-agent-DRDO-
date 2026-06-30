import streamlit as st
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))


from workflow.graph import graph

st.set_page_config(
    page_title="Security Officer Portal",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------
# Header
# --------------------------

st.title("🛡️ Security Officer Portal")
st.caption("DRDO Intelligent Safety Guard")

st.markdown("---")

uploaded_file = st.file_uploader(
    "📄 Upload Incident Report",
    type=["json", "txt"]
)

# --------------------------
# Load Incident
# --------------------------

if uploaded_file:

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

        if isinstance(data, list):

            options = [
                f"{item.get('doc_id','UNKNOWN')} - {item.get('title', item.get('event','No Title'))}"
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

    if st.button("🚀 Analyze Incident", use_container_width=True):

        with st.spinner("Analyzing..."):

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

        st.balloons()

        st.markdown("---")

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

        st.markdown("---")

        st.subheader("📋 Incident Summary")

        threat = result.get("threat_report", {})

        summary = threat.get(
            "summary",
            result["report"]
        )

        st.info(summary)

        st.markdown("---")

        st.subheader("🚨 Recommended Actions")

        recommendations = result["recommendations"]

        for action in recommendations.get(
            "immediate_actions",
            []
        ):

            if isinstance(action, dict):

                st.success(
                    f"✔ {action.get('action')}"
                )

            else:

                st.success(
                    f"✔ {action}"
                )

        st.markdown("---")

        st.download_button(

            label="📥 Download Intelligence Report",

            data=json.dumps(
                result,
                indent=4
            ),

            file_name="Threat_Report.json",

            mime="application/json",

            use_container_width=True

        )