from typing import TypedDict
class ThreatState(TypedDict):

    incident: dict

    entities: dict

    evidence: list

    verified_claims: dict

    confidence_score: float

    threat_score: float
    recommendations: dict

    severity_level: str

    threat_report: dict

    report: str