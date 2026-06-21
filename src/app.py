import streamlit as st
import json
from workflow.graph import graph

st.set_page_config(
    page_title="DRDO Intelligent Safety Guard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ DRDO Intelligent Safety Guard")
st.subheader("Multi-Agent Threat Intelligence System")

uploaded_file = st.file_uploader(
    "Upload Incident Report",
    type=["txt", "json"]
)

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

    st.write("### Incident Preview")

    st.json(incident)

    if st.button("Run Multi-Agent Pipeline"):

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

        with tab1:

            st.subheader("Extracted Entities")

            st.json(result["entities"])

        with tab2:

            st.subheader("Retrieved Evidence")

            for item in result["evidence"]:

                st.write(
                    f"**{item.get('doc_id')}** | "
                    f"{item.get('title')}"
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

            st.metric(
                "Threat Score",
                result["threat_score"]
            )

            st.metric(
                "Severity",
                result["severity_level"]
            )

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
                        f"• {action.get('action')}"
                    )

                else:

                    st.write(f"• {action}")

            st.write("### Monitoring Tasks")

            for task in recommendations.get(
                "monitoring_tasks",
                []
            ):

                if isinstance(task, dict):

                    st.write(
                        f"• {task.get('task')}"
                    )

                else:

                    st.write(f"• {task}")

            st.write("### Escalation")

            st.json(
                recommendations.get(
                    "escalation",
                    {}
                )
            )

            st.write("### Risk Mitigation")

            for item in recommendations.get(
                "risk_mitigation",
                []
            ):

                if isinstance(item, dict):

                    st.write(
                        f"• {item.get('mitigation')}"
                    )

                else:

                    st.write(f"• {item}")

        with tab6:

            st.subheader("Final Report")

            st.text(result["report"])