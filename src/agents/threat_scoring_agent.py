import json
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# =====================================================
# LLM SETUP
# =====================================================

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

llm_json = llm.bind(
    response_format={"type": "json_object"}
)

# =====================================================
# THREAT SCORING CONFIG
# =====================================================

SEVERITY_BANDS = [
    (0.0, 2.0, "Low"),
    (2.0, 5.0, "Medium"),
    (5.0, 8.0, "High"),
    (8.0, 10.01, "Critical"),
]

# =====================================================
# THREAT ANALYSIS PROMPT
# =====================================================

threat_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Senior Defence and Public Safety Threat Assessment Agent.

You MUST return ONLY a valid JSON object.

Output JSON format:

{{
  "threat_score": 0,
  "severity_level": "",
  "summary": "",
  "key_entities": [],
  "threat_indicators": [],
  "evidence": []
}}

Threat Score Guidelines:

0-2 = Low
3-5 = Medium
6-8 = High
9-10 = Critical

Assess the threat using:
- Incident details
- Extracted entities
- Verified claims
- Retrieved evidence

Do not return markdown.
Do not return explanations.
Return JSON only.
"""
    ),
    (
        "user",
        """
Analyze the following threat intelligence:

{document}
"""
    )
])

# =====================================================
# THREAT ANALYSIS FUNCTION
# =====================================================

def analyze_threat(document_text):

    response = (
        threat_prompt
        | llm_json
    ).invoke(
        {
            "document": document_text
        }
    )

    report = json.loads(
        response.content
    )

    score = _clamp_score(
        report.get("threat_score")
    )

    report["threat_score"] = score

    report["severity_level"] = (
        _severity_for_score(
            score,
            report.get("severity_level")
        )
    )

    report.setdefault("summary", "")
    report.setdefault("key_entities", [])
    report.setdefault("threat_indicators", [])
    report.setdefault("evidence", [])

    return report


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def _clamp_score(value):

    try:
        score = float(value)

    except (TypeError, ValueError):
        score = 0.0

    return round(
        max(0.0, min(10.0, score)),
        1
    )


def _severity_for_score(
    score,
    model_severity
):

    for low, high, label in SEVERITY_BANDS:

        if low <= score < high:
            return label

    if isinstance(model_severity, str) and model_severity:
        return model_severity

    return "Low"