import json
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

llm_json = llm.bind(
    response_format={"type": "json_object"}
)

verification_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an Elite Fact Verification Agent.

You MUST return a valid JSON object.

Verify extracted entities against evidence.

Return ONLY JSON.

Output JSON format:

{{
  "verified_claims": {{
    "threat_actor_verified": "",
    "attack_vector_verified": "",
    "target_sector_verified": ""
  }},
  "confidence_score": 0.0
}}
"""
    ),
    (
        "user",
        """
Return ONLY JSON.

Entities:
{entities}

Evidence:
{evidence}
"""
    )
])

verification_chain = (
    verification_prompt
    | llm_json
)


def verify_claims(
    doc_id,
    entities,
    evidence
):

    response = verification_chain.invoke(
        {
            "entities": json.dumps(
                entities,
                indent=2
            ),
            "evidence": json.dumps(
                evidence,
                indent=2
            )
        }
    )

    return json.loads(
        response.content
    )