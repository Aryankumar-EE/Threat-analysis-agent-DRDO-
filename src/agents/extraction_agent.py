import json
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file"
    )
from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# =====================================================================


# Groq LLM setup with forced JSON mode
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
llm_json = llm.bind(response_format={"type": "json_object"})

print("\n🔄 Stage 1: Running Cyber Intelligence Extraction Agent...")

# =====================================================================
# 2. STAGE 1: EXTRACTION AGENT PROMPT & EXECUTION
# =====================================================================
extract_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an Elite Cyber Intelligence Extraction Agent. Analyze raw operational logs "
        "and extract specific intelligence fields into a structured JSON object matching this schema:\n"
        "{{\n"
        '  "doc_id": "string",\n'
        '  "primary_threat_actor": "string",\n'
        '  "attack_vector": "string",\n'
        '  "target_sector": "string",\n'
        '  "compromised_assets": ["array of strings"],\n'
        '  "actionable_indicator": true/false\n'
        "}}\n"
        "Set 'actionable_indicator' to true ONLY if the threat is active/ongoing or a severe breach."
    )),
    ("user", "Analyze:\nTitle: {title}\nContent: {content}\nLocation: {location}\nDoc ID: {doc_id}")
])

extraction_chain = extract_prompt | llm_json


def extract_intelligence(incident):

    response = extraction_chain.invoke({
        "doc_id": incident["doc_id"],
        "title": incident["title"],
        "content": incident["content"],
        "location": incident["location"]
    })

    return json.loads(response.content)


incident = {
    "doc_id": "CI001",
    "title": "Ransomware Attack",
    "content": "Multiple servers were encrypted by attackers.",
    "location": "Delhi"
}

result = extract_intelligence(incident)

print(result)