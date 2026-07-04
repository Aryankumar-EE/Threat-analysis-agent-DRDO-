# 🛡️ DRDO Intelligent Safety Guard

## AI-Powered Multi-Agent Threat Intelligence & Decision Support System

### Overview

DRDO Intelligent Safety Guard is an AI-driven Multi-Agent Threat Intelligence System designed to automate cyber threat analysis, verification, risk assessment, and recommendation generation.

The system uses LangGraph-based agent orchestration, FAISS vector search, Llama 3.1 LLM, and a Streamlit dashboard to provide real-time threat intelligence support.

---

## Features

### Extraction Agent

* Extracts threat actor
* Identifies attack vector
* Detects target sector
* Finds compromised assets

### Retrieval Agent

* Retrieves similar incidents using FAISS
* Provides supporting intelligence evidence

### Verification Agent

* Verifies extracted claims
* Generates confidence score

### Threat Scoring Agent

* Calculates threat score (0–10)
* Assigns severity level

### Recommendation Agent

* Generates actionable recommendations
* Provides escalation guidance
* Suggests risk mitigation measures

### Report Generation Agent

* Produces final intelligence report

---

## System Architecture

User Input
↓
Extraction Agent
↓
Retrieval Agent (FAISS)
↓
Verification Agent
↓
Threat Scoring Agent
↓
Recommendation Agent
↓
Report Generation Agent
↓
Streamlit Dashboard

---

## Technology Stack

* Python
* LangGraph
* LangChain
* Groq API
* Llama 3.1
* FAISS
* Sentence Transformers
* Streamlit
* JSON

---

## Dataset

The project uses a custom cyber incident dataset containing:

* Cyber fraud incidents
* Phishing attacks
* Ransomware attacks
* Insider threats
* Cloud security incidents
* Smart city security events
* Banking cyber attacks

Total Records: 80

---

## Installation

### Clone Repository

git clone <repository-link>

cd drdoaryan

### Install Dependencies

pip install -r requirements.txt

### Create .env File

GROQ_API_KEY=your_groq_api_key

### Run Main Pipeline

python src/main.py

### Run Dashboard

streamlit run src/app.py

---

## Sample Output

Threat Score: 7.0

Severity: High

Confidence: 80%

Recommended Actions:

* Block suspicious IPs
* Investigate incident
* Implement additional security controls

---

## Future Scope

* Real-time SOC Integration
* SIEM Integration
* Threat Feed Integration
* Crowd Intelligence Module
* CCTV Analytics
* Predictive Threat Modeling

---

## Project Team

<<<<<<< HEAD
Project Leader:
Aryan Kumar , Faculty of Technology(UoD)
Paresha SUdha , Faculty of Technology(UoD)
Kalpana , IGDTUW
Manisha , IGDTUW
=======
Project members:
Aryan Kumar
Paresha sudha
Manisha
kalpana 
>>>>>>> 8282a0f386dc7ff74412cd74ef3ff8a5756eb7a7


DRDO Internship Project
