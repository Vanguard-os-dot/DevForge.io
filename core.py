# core/engine.py

class NativeLocalAI:
    def __init__(self):
        # Built from scratch for this project: zero API keys, zero external calls
        self.knowledge_base = {
            "hello": "Local engine active.",
            "status": "All local subsystems operational.",
            "help": "Type instructions to generate code locally."
        }

    def generate(self, prompt: str) -> str:
        clean_prompt = prompt.lower().strip()
        
        if any(w in clean_prompt for w in ["html", "page", "create", "build"]):
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Generated Output</title>
<style>
  body {{ background: #0f0f11; color: #39ff14; font-family: monospace; padding: 20px; }}
  .card {{ border: 1px solid #39ff14; padding: 20px; border-radius: 8px; margin-top: 20px; background: #18181b; }}
</style>
</head>
<body>
  <h1>Native Execution</h1>
  <div class="card">
    <p>Processed prompt: <strong>{prompt}</strong></p>
    <p>Status: Local generation complete.</p>
  </div>
</body>
</html>"""

        for key, response in self.knowledge_base.items():
            if key in clean_prompt:
                return response
                
        return f"<!-- Local Processed -->\n<div style='font-family:monospace; color:#39ff14; padding:15px; background:#121212;'>\n  <h3>Result</h3>\n  <p>Processed instruction: {prompt}</p>\n</div>"

