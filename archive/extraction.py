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

try:
    with open('cyber_incidents.json', 'r') as f:
        incidents = json.load(f)
    
    extracted_database = []
    for incident in incidents:
        print(f" 🔄 Extracting Intel: {incident['doc_id']}...")
        response = extraction_chain.invoke({
            "doc_id": incident["doc_id"],
            "title": incident["title"],
            "content": incident["content"],
            "location": incident["location"]
        })
        extracted_database.append(json.loads(response.content))
        
    # Step 1 Ki File Save Karein
    with open('extracted_cyber_intel.json', 'w') as f_out:
        json.dump(extracted_database, f_out, indent=4)
    print("✅ Stage 1 Complete! Data saved to 'extracted_cyber_intel.json'")

# =====================================================================
# 3. STAGE 2: CORRELATION & TREND ANALYST AGENT (JSON OUTPUT ONLY)
# =====================================================================
    print("\n🕵️‍♂️ Stage 2: Running Trend Analyst Agent (Generating JSON Report)...")
    
    analyst_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a Senior Cyber Threat Intelligence Analyst. Your task is to analyze the provided "
            "JSON database of cyber incidents and generate a high-level analytics summary.\n\n"
            "You MUST respond with a valid JSON object matching this exact schema:\n"
            "{{\n"
            '  "executive_summary": "Overall evaluation of the threat landscape.",\n'
            '  "top_targeted_sectors": ["Ranked list of top 3 sectors targeted"],\n'
            '  "dominant_attack_vectors": ["Most common attack methodologies used"],\n'
            '  "critical_metrics": {{\n'
            '     "total_incidents": 50,\n'
            '     "actionable_threats_count": "number of incidents with actionable_indicator true",\n'
            '     "non_actionable_count": "number of incidents with actionable_indicator false"\n'
            '  }},\n'
            '  "strategic_recommendations": ["List of actionable recommendations for C-level executives"]\n'
            "}}"
        )),
        ("user", "Analyze patterns from this dataset:\n\n{structured_data}")
    ])
    
    analyst_chain = analyst_prompt | llm_json
    
    # Pure data pass karke final dashboard metrics report generate karna
    print(" 🔄 Aggregating metrics and corellating trends...")
    analysis_response = analyst_chain.invoke({
        "structured_data": json.dumps(extracted_database, indent=2)
    })
    
    # Step 2 Ki Final File Save Karein (JSON Format)
    final_report_json = json.loads(analysis_response.content)
    with open('threat_analysis_report.json', 'w') as f_rep:
        json.dump(final_report_json, f_rep, indent=4)
        
    print("="*50)
    print("🎯 Mission Accomplished! Dono steps ka output absolute JSON format me save ho gaya hai:")
    print("1. Extracted Data -> 'extracted_cyber_intel.json'")
    print("2. Final Analytics Report -> 'threat_analysis_report.json'")

except Exception as e:
    print(f"❌ Pipeline Error: {str(e)}")