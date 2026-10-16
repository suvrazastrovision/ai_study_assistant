from flask import Flask, render_template, request
from openai import OpenAI, OpenAIError

from prompt_builder import build_prompt

app = Flask(__name__)
client = OpenAI()

VALID_MODES = {"quiz", "summary", "study_plan"}


def generate_study_help(topic: str, mode: str) -> str:
    """
    Generate AI-powered study help for a topic.

    Args:
        topic: The study topic entered by the user.
        mode: The selected study mode.

    Returns:
        The AI-generated study content.

    Raises:
        ValueError: If the topic or mode is invalid.
        RuntimeError: If the AI request fails.
    """
    if not topic:
        raise ValueError("Please enter a topic before asking for study help.")

    if mode not in VALID_MODES:
        raise ValueError("Invalid study mode selected.")

    prompt = build_prompt(topic, mode)

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic},
            ],
        )
    except OpenAIError as exc:
        raise RuntimeError(
            "Something went wrong while contacting the AI service. Please try again."
        ) from exc

    output_text = (response.output_text or "").strip()

    if not output_text:
        raise RuntimeError(
            "The AI service returned an empty response. Please try again."
        )

    return output_text


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Display the study assistant and process form submissions.
    """
    topic = ""
    mode = "quiz"
    result = ""
    error = ""

    if request.method == "POST":
        topic = (request.form.get("topic") or "").strip()
        mode = (request.form.get("mode") or "quiz").strip()

        try:
            result = generate_study_help(topic, mode)
        except (ValueError, RuntimeError) as exc:
            error = str(exc)
        except Exception:
            error = "An unexpected error occurred. Please try again."

    return render_template(
        "index.html",
        topic=topic,
        mode=mode,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)