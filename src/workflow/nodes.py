from agents.extraction_agent import extract_intelligence
from agents.retrieval_agent import retrieve_evidence


def extraction_node(state):

    state["entities"] = extract_intelligence(
        state["incident"]
    )

    return state


def retrieval_node(state):

    attack_vector = state["entities"]["attack_vector"]

    state["evidence"] = retrieve_evidence(
        attack_vector
    )

    return state


from agents.verification_agent import verify_claims

def verification_node(state):

    print(
        "Verification Agent Running"
    )

    result = verify_claims(
        doc_id=
        state["entities"]["doc_id"],

        entities=
        state["entities"],

        evidence=
        state["evidence"]
    )

    state["verified_claims"] = (
        result["verified_claims"]
    )

    state["confidence_score"] = (
        result["confidence_score"]
    )

    return state


from agents.threat_agent import calculate_threat


def threat_node(state):

    print("Threat Agent Running")

    report = calculate_threat(
        state
    )

    state["threat_score"] = (
        report["threat_score"]
    )

    state["severity_level"] = (
        report["severity_level"]
    )

    state["threat_report"] = (
        report
    )

    return state

def report_node(state):

    print("Report Agent Running")

    report = state["threat_report"]

    state["report"] = f"""
THREAT ASSESSMENT REPORT

Threat Score:
{report['threat_score']}/10

Severity:
{report['severity_level']}

Summary:
{report['summary']}
"""

    return state

from agents.recommendation_agent import (
    generate_recommendations
)

def recommendation_node(state):

    print(
        "Recommendation Agent Running"
    )

    state["recommendations"] = (
        generate_recommendations(
            state["threat_report"]
        )
    )

    return state