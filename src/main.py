#testing paresha
import from workflow.graph import graph
import json
from pathlib import Path


# =====================================================
# LOAD DATASET
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "cyber_incidents.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    incidents = json.load(f)


# =====================================================
# RUN PIPELINE
# =====================================================

def run_pipeline(incident):
    initial_state = {
        "incident": incident,

        "entities": {},
        "evidence": [],

        "verified_claims": {},
        "confidence_score": 0.0,

        "threat_score": 0.0,
        "severity_level": "",

        "threat_report": {},

        "recommendations": {},

        "report": ""
    }

    result = graph.invoke(initial_state)

    return result


# =====================================================
# MAIN
# =====================================================

def main():

    print("\n" + "=" * 70)
    print("DRDO INTELLIGENT SAFETY GUARD SYSTEM")
    print("MULTI-AGENT THREAT INTELLIGENCE PIPELINE")
    print("=" * 70)

    try:

        print(f"\nLoaded {len(incidents)} incidents")

        print("\nAVAILABLE INCIDENTS")
        print("-" * 70)

        for i, incident in enumerate(incidents):

            print(
                f"{i+1}. "
                f"{incident['doc_id']} - "
                f"{incident.get('title', incident.get('event', 'No Title'))}"
            )

        choice = int(input("\nSelect Incident Number: "))

        if choice < 1 or choice > len(incidents):
            print("Invalid selection.")
            return

        incident = incidents[choice - 1]

        print("\nRunning Multi-Agent Pipeline...")
        print("-" * 70)

        result = run_pipeline(incident)

        # =====================================================
        # EXTRACTED ENTITIES
        # =====================================================

        print("\n[1] EXTRACTED ENTITIES")
        print("-" * 40)

        print(
            json.dumps(
                result["entities"],
                indent=4
            )
        )

        # =====================================================
        # EVIDENCE
        # =====================================================

        print("\n[2] RETRIEVED EVIDENCE")
        print("-" * 40)

        for evidence in result["evidence"]:

            print(
                f"{evidence.get('doc_id')} | "
                f"{evidence.get('title')}"
            )

        # =====================================================
        # VERIFICATION
        # =====================================================

        print("\n[3] VERIFIED CLAIMS")
        print("-" * 40)

        print(
            json.dumps(
                result["verified_claims"],
                indent=4
            )
        )

        print("\nVerification Confidence")
        print(
            result.get(
                "confidence_score",
                0
            )
        )

        # =====================================================
        # THREAT SCORE
        # =====================================================

        print("\n[4] THREAT SCORE")
        print("-" * 40)

        print(result["threat_score"])

        print(
            f"Severity: "
            f"{result.get('severity_level', '')}"
        )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        print("\n[5] RECOMMENDATIONS")
        print("-" * 40)

        recommend = result["recommendations"]

        print("\nImmediate Actions:")

        for action in recommend.get(
            "immediate_actions",
            []
        ):

            if isinstance(action, dict):

                print(
                    f"• {action.get('action')}"
                )

                print(
                    f"  Urgency: {action.get('urgency')}"
                )

                print(
                    f"  Owner: {action.get('responsible')}"
                )

            else:
                print(f"• {action}")

        print("\nMonitoring Tasks:")

        for task in recommend.get(
            "monitoring_tasks",
            []
        ):

            if isinstance(task, dict):

                print(
                    f"• {task.get('task')}"
                )

                print(
                    f"  Urgency: {task.get('urgency')}"
                )

                print(
                    f"  Owner: {task.get('responsible')}"
                )

            else:
                print(f"• {task}")

        print("\nEscalation:")

        esc = recommend.get(
            "escalation",
            {}
        )

        print(
            f"Should Escalate : "
            f"{esc.get('should_escalate')}"
        )

        print(
            f"Escalate To     : "
            f"{esc.get('escalate_to')}"
        )

        print(
            f"Urgency         : "
            f"{esc.get('urgency')}"
        )

        print(
            f"Reason          : "
            f"{esc.get('reason')}"
        )

        print("\nRisk Mitigation:")

        for item in recommend.get(
            "risk_mitigation",
            []
        ):

            if isinstance(item, dict):

                print(
                    f"• {item.get('mitigation')}"
                )

                print(
                    f"  Urgency: {item.get('urgency')}"
                )

                print(
                    f"  Owner: {item.get('responsible')}"
                )

            else:
                print(f"• {item}")

        # =====================================================
        # FINAL REPORT
        # =====================================================

        print("\n[6] FINAL REPORT")
        print("-" * 40)

        print(result["report"])

        # =====================================================
        # SAVE OUTPUT
        # =====================================================

        report_path = (
            BASE_DIR /
            "final_intelligence_report.json"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as outfile:

            json.dump(
                result,
                outfile,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        print(
            f"\nReport saved to:\n{report_path}"
        )

    except Exception as e:

        print(
            f"\nPipeline Error: {e}"
        )


if __name__ == "__main__":
    main()
