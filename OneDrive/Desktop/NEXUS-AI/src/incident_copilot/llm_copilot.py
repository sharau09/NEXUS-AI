from ollama import chat

from src.incident_copilot.copilot_engine import (
    search_incidents
)

from src.incident_copilot.history_manager import (
    save_investigation
)


def investigate_incident(question):

    # Retrieve relevant incident evidence
    results = search_incidents(
        question,
        top_k=5
    )

    # Build evidence text
    evidence = ""

    for i, result in enumerate(
        results,
        start=1
    ):

        evidence += (
            f"\n\n--- Evidence {i} ---\n"
            f"{result['document']}\n"
        )

    # Handle case where no evidence is found
    if not evidence.strip():

        return {
            "question": question,
            "answer": (
                "## ⚠️ Insufficient Evidence\n\n"
                "NEXUS AI could not find relevant "
                "incident evidence for this question."
            ),
            "evidence": []
        }

    # Create AI investigation prompt
    prompt = f"""
You are NEXUS AI, an expert Autonomous AI Operations Engineer.

Your job is to investigate system incidents.

IMPORTANT:
You must analyze the incident using ONLY the
provided incident evidence.

USER QUESTION:
{question}

INCIDENT EVIDENCE:
{evidence}

Return your answer using EXACTLY the following format:

## 🚨 INCIDENT SUMMARY

Briefly explain what happened.

## 🎯 LIKELY ROOT CAUSE

Explain the most likely root cause based on the evidence.

## 📊 CONFIDENCE SCORE

Provide a confidence percentage between 0% and 100%.

## 🔍 EVIDENCE

List the important evidence supporting your conclusion.

## 💥 SYSTEM IMPACT

Explain the possible impact on users,
services, APIs, or system performance.

## ⚠️ RISK LEVEL

Choose exactly one:

LOW
MEDIUM
HIGH
CRITICAL

## 🛠️ RECOMMENDED ACTIONS

Provide practical steps engineers should take
to investigate or fix the incident.

IMPORTANT RULES:

- Use ONLY the provided evidence.
- Do NOT invent incidents.
- Do NOT invent metrics.
- Do NOT invent root causes.
- If evidence is insufficient, clearly say:
  "Insufficient evidence".
- Be concise and professional.
"""

    try:

        # Ask local Ollama model
        response = chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response["message"]["content"]

    except Exception as e:

        answer = (
            "## ❌ AI Investigation Error\n\n"
            "Unable to contact the local Ollama model.\n\n"
            f"Error: `{str(e)}`"
        )

    # Save investigation history
    investigation_record = save_investigation(
        question=question,
        answer=answer,
        evidence=results
    )

    # Return investigation result
    return {
        "question": question,
        "answer": answer,
        "evidence": results,
        "history": investigation_record
    }


if __name__ == "__main__":

    question = (
        "What is causing the critical incidents?"
    )

    result = investigate_incident(
        question
    )

    print("\n" + "=" * 60)
    print("QUESTION:")
    print(result["question"])

    print("\n" + "=" * 60)
    print("AI INVESTIGATION:")
    print(result["answer"])

    print("\n" + "=" * 60)
    print("EVIDENCE USED:")

    for i, evidence_item in enumerate(
        result["evidence"],
        start=1
    ):

        print(f"\nEvidence {i}:")
        print(
            evidence_item["document"]
        )

    print("\n" + "=" * 60)
    print("INVESTIGATION SAVED:")
    print(
        result["history"]["timestamp"]
    )