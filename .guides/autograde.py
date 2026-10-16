from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    print(message)
    sys.exit(1)


def main() -> None:
    app_path = ROOT / "app.py"
    prompt_path = ROOT / "prompt_builder.py"
    template_path = ROOT / "templates" / "index.html"

    for path in (app_path, prompt_path, template_path):
      if not path.exists():
        fail(f"Missing required file: {path.relative_to(ROOT)}")

    app_text = app_path.read_text(encoding="utf-8")
    prompt_text = prompt_path.read_text(encoding="utf-8")
    template_text = template_path.read_text(encoding="utf-8")

    if "OpenAI" not in app_text:
        fail("OpenAI client usage was not detected in app.py")

    if "responses.create" not in app_text:
        fail("Expected a responses.create call in app.py")

    if "quiz" not in prompt_text or "summary" not in prompt_text or "plan" not in prompt_text:
        fail("Expected prompt_builder.py to support quiz, summary, and plan modes")

    if "result" not in template_text:
        fail("Expected the template to display the generated result")

    print("Autograde checks passed.")


if __name__ == "__main__":
    main()
