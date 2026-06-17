from graph import graph

initial_state = {

    "incident": {
        "doc_id": "CI001",
        "title": "Ransomware Attack",
        "content": "Multiple servers were encrypted by attackers.",
        "location": "Delhi"
    },

    "entities": {},
    "evidence": [],
    "verified_claims": [],
    "threat_score": 0,
    "report": ""
}

result = graph.invoke(initial_state)

print("\nENTITIES\n")
print(result["entities"])

print("\nEVIDENCE COUNT\n")
print(len(result["evidence"]))

print("\nTHREAT SCORE\n")
print(result["threat_score"])

print("\nREPORT\n")
print(result["report"])