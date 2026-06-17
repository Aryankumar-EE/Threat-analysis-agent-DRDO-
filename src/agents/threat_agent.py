from agents.threat_scoring_agent import analyze_threat


def calculate_threat(state):

    context = f"""
Incident:
{state['incident']}

Entities:
{state['entities']}

Verified Claims:
{state['verified_claims']}

Confidence Score:
{state.get('confidence_score', 0)}

Evidence:
{state['evidence']}
"""

    return analyze_threat(context)