VALID_MODES = {"quiz", "summary", "study_plan"}


def build_prompt(topic: str, mode: str) -> str:
    """
    Build the study assistant prompt based on the selected mode.

    Args:
        topic: The topic the student wants to study.
        mode: The selected study mode.

    Returns:
        A formatted prompt ready to send to the AI model.

    Raises:
        ValueError: If an unsupported mode is supplied.
    """
    if mode not in VALID_MODES:
        raise ValueError("Invalid study mode selected.")

    if mode == "quiz":
        mode_instruction = (
            "Create 5 short quiz questions with brief answers. "
            "Use numbered items and keep the language student-friendly."
        )

    elif mode == "summary":
        mode_instruction = (
            "Write a concise study summary with the following sections:\n"
            "1. Key Ideas\n"
            "2. Important Terms\n"
            "3. Quick Reminder\n"
            "Keep each section brief and easy to revise from."
        )

    else:  # study_plan
        mode_instruction = (
            "Create a 4-step study plan. "
            "Each step should include a practical action. "
            "Finish with a short self-check activity."
        )

    return f"""
You are a helpful study assistant for beginner learners.

The student wants help with the topic:

{topic}

Task:
{mode_instruction}

Requirements:
- Use clear and simple language.
- Be accurate and educational.
- Avoid unnecessary filler.
- Keep the content easy to scan.
- If the topic is broad, still provide practical study help.
- Concise

Return only the study content.
""".strip()