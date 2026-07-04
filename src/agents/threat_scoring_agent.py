import json
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
<<<<<<< HEAD

=======
>>>>>>> 8282a0f386dc7ff74412cd74ef3ff8a5756eb7a7
# =====================================================
# LLM SETUP
# =====================================================

llm = ChatGroq(
    model="llama-3.1-8b-instant",
<<<<<<< HEAD
    temperature=0,
    api_key=GROQ_API_KEY
)
=======
    temperature=0,api_key= GROQ_API_KEY)
>>>>>>> 8282a0f386dc7ff74412cd74ef3ff8a5756eb7a7

llm_json = llm.bind(
    response_format={"type": "json_object"}
)

# =====================================================
# THREAT SCORING CONFIG
# =====================================================

SEVERITY_BANDS = [
    (0.0, 2.0,  "Low"),
    (2.0, 5.0,  "Medium"),
    (5.0, 8.0,  "High"),
    (8.0, 10.01,"Critical"),
]

# =====================================================
# THREAT ANALYSIS PROMPT  (rewritten)
# =====================================================

threat_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Senior Defence and Public Safety Threat Assessment Agent.
Return ONLY a valid JSON object — no markdown, no explanation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCORING SCALE  (threat_score: 0.0 – 10.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

0.0 – 1.9  │ LOW
  • Routine, fully lawful activity with no risk indicators.
  • Examples: speed checks, parking tickets, noise complaints,
    routine border crossings, administrative database queries,
    policy research, general public-safety drills.
  • No weapons, no targets, no threat language, no prior history.

2.0 – 4.9  │ MEDIUM
  • Minor or ambiguous indicators that warrant monitoring
    but no immediate action.
  • Examples: low-level antisocial behaviour with a pattern,
    minor possession offence, mildly suspicious surveillance of
    a public building with no confirmed intent, vague online
    threat with no operational detail, petty theft.

5.0 – 7.9  │ HIGH
  • Credible threat with specific targets, timing, or methods,
    OR organised criminal activity posing risk to individuals.
  • Examples: confirmed gang violence with named targets,
    credible bomb threat with partial operational detail,
    smuggling of restricted goods, serious stalking with
    explicit intent, cyber-attack on critical infrastructure
    with evidence of capability.

8.0 – 10.0 │ CRITICAL
  • Imminent or active threat of mass casualties, national
    security breach, or catastrophic harm.
  • Examples: active shooter, confirmed CBRN weapon attempt,
    active terrorist plot with resources and target confirmed,
    live hostage situation, infrastructure attack in progress.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCORING RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Default to LOW (0-1.9) unless there is explicit evidence
   of harmful intent, capability, or outcome. Do NOT score
   higher simply because a topic sounds sensitive.

2. Raise the score only when TWO OR MORE of these factors
   are present and evidenced in the document:
     a) Specific identifiable target (person, place, system)
     b) Credible capability or method described
     c) Stated or strongly implied harmful intent
     d) Timeline or imminent action signals
     e) Prior related incidents or escalating pattern

3. If only ONE factor is present → stay in Low or low-Medium.

4. Hypotheticals, simulations, research, or training exercises
   must be scored ≤ 2.0 unless the document itself contains
   independent threat indicators.

5. Score precision: use one decimal place (e.g. 3.4, 7.1).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT (strict)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{{
  "threat_score": 0.0,
  "severity_level": "",
  "scoring_rationale": "",
  "factors_present": [],
  "summary": "",
  "key_entities": [],
  "threat_indicators": [],
  "evidence": []
}}

Field notes:
- scoring_rationale : 1-2 sentences explaining why that exact
  score was chosen, referencing which factors above were met.
- factors_present   : list from [target, capability, intent,
  timeline, pattern] that are confirmed in the document.
- threat_indicators : specific phrases/facts from the document
  that raised (or kept low) the score.
- evidence          : supporting facts or citations from the text.
"""
    ),
    (
        "user",
        """
Analyze the following document and return the JSON assessment:

{document}
"""
    )
])

# =====================================================
# THREAT ANALYSIS FUNCTION
# =====================================================

def analyze_threat(document_text: str) -> dict:
    """
    Analyze a document for threat indicators and return a
    structured report with a calibrated threat score.
    """
    response = (threat_prompt | llm_json).invoke(
        {"document": document_text}
    )

    report = json.loads(response.content)

    # -- Normalise & clamp score -----------------------
    score = _clamp_score(report.get("threat_score"))
    report["threat_score"] = score

    # -- Authoritative severity from score bands -------
    # (model's own label is ignored; bands are the source of truth)
    report["severity_level"] = _severity_for_score(score)

    # -- Ensure all expected fields exist --------------
    for field, default in [
        ("scoring_rationale", ""),
        ("factors_present",   []),
        ("summary",           ""),
        ("key_entities",      []),
        ("threat_indicators", []),
        ("evidence",          []),
    ]:
        report.setdefault(field, default)

    return report


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def _clamp_score(value) -> float:
    """Coerce value to a float clamped to [0.0, 10.0]."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 0.0
    return round(max(0.0, min(10.0, score)), 1)


def _severity_for_score(score: float) -> str:
    """Map a numeric score to a severity label via SEVERITY_BANDS."""
    for low, high, label in SEVERITY_BANDS:
        if low <= score < high:
            return label
    return "Low"   # fallback (score == 10.0 is caught by last band)


# =====================================================
# QUICK SMOKE-TEST  (remove before production)
# =====================================================

if __name__ == "__main__":

    test_cases = [
        # Should be LOW
        ("Routine patrol",
         "Officer conducted a routine speed check on Highway 9. "
         "No violations detected. All vehicles cleared."),

        # Should be MEDIUM
        ("Suspicious loitering",
         "A man was observed circling the downtown courthouse "
         "three times over two hours, photographing entrances. "
         "No weapons visible. No prior record found."),

        # Should be HIGH
        ("Credible threat with target",
         "Intercepted message: 'We will hit the central railway "
         "station on Friday morning. Package is ready and team "
         "is in place.' Sender identity partially confirmed."),

        # Should be CRITICAL
        ("Active incident",
         "Active shooter reported inside Terminal 2, "
         "International Airport. Multiple casualties confirmed. "
         "Subject armed with automatic rifle, still at large."),
    ]

    for label, doc in test_cases:
        result = analyze_threat(doc)
        print(
            f"[{label}]\n"
            f"  Score    : {result['threat_score']}\n"
            f"  Severity : {result['severity_level']}\n"
            f"  Rationale: {result['scoring_rationale']}\n"
            f"  Factors  : {result['factors_present']}\n"
        )