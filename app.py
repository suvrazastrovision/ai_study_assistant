import os

from dotenv import load_dotenv
from flask import Flask, render_template_string, request
from openai import OpenAI, OpenAIError

load_dotenv()

app = Flask(__name__)

MODE_INSTRUCTIONS = {
    "quiz": (
        "Create exactly 5 numbered practice questions: include recall and "
        "application questions. Put concise answers in a separate Answer Key "
        "after the questions; do not show answers beside the questions."
    ),
    "summary": (
        "Explain the topic in a concise summary of about 150-200 words. Use "
        "the headings Key Ideas, Important Terms, and Quick Review. Focus on "
        "understanding rather than asking questions or listing study tasks."
    ),
    "plan": (
        "Create a practical 4-step study plan for about 30 minutes total. "
        "Give every step a time estimate and a concrete activity. Finish with "
        "a short self-check; do not write a general topic summary."
    ),
}

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Study Assistant</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <main class="page-shell">
      <section class="card hero-card">
        <h1>Study Assistant</h1>
        <p class="intro">Choose a topic and a study mode to create focused materials for your next study session.</p>
      </section>
      <section class="grid">
        <section class="card form-card">
          <h2>Build a study session</h2>
          <form method="post" class="study-form">
            <label for="topic">Topic</label>
            <input id="topic" name="topic" type="text" value="{{ topic }}" placeholder="Try a focused topic, like SQL joins" required>
            <label for="mode">Study mode</label>
            <select id="mode" name="mode">
              <option value="quiz" {% if mode == "quiz" %}selected{% endif %}>Quiz questions</option>
              <option value="summary" {% if mode == "summary" %}selected{% endif %}>Summary</option>
              <option value="plan" {% if mode == "plan" %}selected{% endif %}>Study plan</option>
            </select>
            <button type="submit">Create study material</button>
          </form>
          {% if error %}<div class="message error" role="alert">{{ error }}</div>{% endif %}
        </section>
        <section class="card result-card" aria-live="polite">
          <h2>Your study material</h2>
          {% if result %}
          <pre class="result-output" tabindex="0">{{ result }}</pre>
          {% else %}
          <p class="empty-state">Your questions, summary, or study steps will appear here after you submit a topic.</p>
          {% endif %}
        </section>
      </section>
    </main>
  </body>
</html>
"""


def build_prompt(topic: str, mode: str) -> str:
    """Build a focused prompt with a distinct structure for each study mode."""
    if mode not in MODE_INSTRUCTIONS:
        raise ValueError("Choose quiz, summary, or study plan mode.")

    return f"""You are an accurate, beginner-friendly study assistant.

The student's topic is: {topic}

Create {mode} study material:
{MODE_INSTRUCTIONS[mode]}

Keep the response focused, useful, concise, and easy to scan. Do not invent
unsupported facts. If the topic is too unclear to answer reliably, ask one
brief clarifying question instead of guessing. If it is broad, focus on the
most important general ideas. Return only the study material."""


def generate_study_help(topic: str, mode: str) -> str:
    prompt = build_prompt(topic, mode)
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI()
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic},
            ],
        )
    except OpenAIError as exc:
        raise RuntimeError("The AI service request failed. Please try again.") from exc

    result = (response.output_text or "").strip()
    if not result:
        raise RuntimeError("The AI service returned an empty response.")
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    topic = ""
    mode = "quiz"
    result = ""
    error = ""

    if request.method == "POST":
        topic = (request.form.get("topic") or "").strip()
        mode = (request.form.get("mode") or "quiz").strip()

        if not topic:
            error = "Please enter a topic before asking the study assistant for help."
        else:
            try:
                result = generate_study_help(topic, mode)
            except (RuntimeError, ValueError) as exc:
                error = str(exc)

    return render_template_string(
        INDEX_TEMPLATE,
        topic=topic,
        mode=mode,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
