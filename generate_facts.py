import os
import json
import urllib.request
from datetime import datetime

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

PROMPT = """Generate 5 fascinating, true, and verifiable facts from science, history, or nature.
Return ONLY valid JSON in this exact format, nothing else:
[
  {"fact": "short catchy title", "explanation": "1-2 sentence explanation"},
  ...
]"""

def get_facts():
    payload = {
        "contents": [{"parts": [{"text": PROMPT}]}]
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    text = text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)

def build_html(facts):
    today = datetime.now().strftime("%B %d, %Y")
    items = "\n".join(
        f'<div class="fact"><h2>{f["fact"]}</h2><p>{f["explanation"]}</p></div>'
        for f in facts
    )
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Daily Fascinating Facts</title>
<style>
body {{ font-family: Georgia, serif; max-width: 700px; margin: 40px auto; padding: 0 20px; background: #fdfdfd; color: #222; }}
h1 {{ text-align: center; }}
.date {{ text-align: center; color: #888; margin-bottom: 40px; }}
.fact {{ margin-bottom: 30px; padding: 20px; border-left: 4px solid #6c63ff; background: #f7f7ff; }}
.fact h2 {{ margin: 0 0 10px; font-size: 1.2em; }}
.fact p {{ margin: 0; line-height: 1.5; }}
</style>
</head>
<body>
<h1>🌟 Daily Fascinating Facts</h1>
<div class="date">{today}</div>
{items}
</body>
</html>"""

if __name__ == "__main__":
    facts = get_facts()
    html = build_html(facts)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated index.html successfully")
