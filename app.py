import json
import os
from urllib.request import Request, urlopen

from flask import Flask, render_template, request
from dotenv import load_dotenv

from prompt_builder import build_prompt

load_dotenv()

app = Flask(__name__)


def generate_study_help(topic: str, mode: str) -> str:
    prompt = build_prompt(topic, mode)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    payload = json.dumps(
        {
            "model": "gpt-4o-mini",
            "input": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic},
            ],
        }
    ).encode("utf-8")
    request = Request(
        "https://api.openai.com/v1/responses",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request) as response:
        data = json.load(response)

    return "".join(
        content.get("text", "")
        for output in data.get("output", [])
        if output.get("type") == "message"
        for content in output.get("content", [])
        if content.get("type") == "output_text"
    )


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
            result = generate_study_help(topic, mode)

    return render_template(
        "index.html",
        topic=topic,
        mode=mode,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
