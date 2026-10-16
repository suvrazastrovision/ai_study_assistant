MODE_INSTRUCTIONS = {
    "quiz": (
        "Create exactly 5 numbered questions, mixing recall and application. "
        "After the questions, add an 'Answer Key' with a concise answer for "
        "each number. Do not reveal answers alongside the questions."
    ),
    "summary": (
        "Write a concise summary of about 150-200 words. Use the headings "
        "'Key Ideas', 'Important Terms', and 'Quick Review'. Explain the main "
        "ideas in your own words and define only terms relevant to the topic."
    ),
    "plan": (
        "Create a practical 4-step study plan for a beginner, for about "
        "30 minutes total. Give each step a time estimate and a concrete "
        "activity, such as reviewing, practicing, or self-testing. End with "
        "a short self-check."
    ),
}


def build_prompt(topic: str, mode: str) -> str:
    mode_instruction = MODE_INSTRUCTIONS.get(
        mode,
        "Give concise, structured study help that explains the key ideas and "
        "includes one useful way to check understanding.",
    )
    return f"""
You are a clear, accurate study assistant for beginner learners.

The student's topic is:
{topic}

For this request:
{mode_instruction}

Requirements:
- Use student-friendly language and keep the response focused and easy to scan.
- Be accurate. Do not invent details, definitions, or facts to fill gaps.
- If the topic is unclear or ambiguous, ask one brief clarifying question
  instead of guessing.
- If the topic is broad, focus on the most important general ideas without
  pretending to cover every detail.
- Return only the study content.
""".strip()
