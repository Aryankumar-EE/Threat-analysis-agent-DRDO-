import json
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY
)

llm_json = llm.bind(
    response_format={"type": "json_object"}
)

recommendation_prompt = ChatPromptTemplate.from_messages([
(
"system",
"""
You are a Cyber Incident Response Advisor.

Return ONLY JSON.

Output format:

{{
  "immediate_actions": [],
  "monitoring_tasks": [],
  "escalation": {{
      "should_escalate": false,
      "escalate_to": "",
      "urgency": "",
      "reason": ""
  }},
  "risk_mitigation": []
}}
"""
),
(
"user",
"""
Generate recommendations for:

{threat_report}
"""
)
])

recommendation_chain = (
    recommendation_prompt
    | llm_json
)


def generate_recommendations(
    threat_report
):

    response = (
        recommendation_chain
    ).invoke(
        {
            "threat_report":
            json.dumps(
                threat_report,
                indent=2
            )
        }
    )

    return json.loads(
        response.content
    )