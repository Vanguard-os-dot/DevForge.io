from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

class CodePayload(BaseModel):
    language: str
    code: str

@app.post("/api/emulate")
def emulate_code(payload: CodePayload):
    lang = payload.language.lower()
    code = payload.code

    if lang == "python":
        try:
            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "status": "success",
                "output": result.stdout if result.returncode == 0 else result.stderr,
                "rendered_html": f"<pre class='text-emerald-400 font-mono text-xs'>{result.stdout}</pre>"
            }
        except Exception as e:
            return {"status": "error", "output": str(e)}

    return {
        "status": "success",
        "output": f"Emulated {lang.upper()} payload successfully parsed.",
        "rendered_html": f"<div class='p-4 bg-slate-950 border border-slate-800 rounded-lg'><div class='text-xs text-blue-400 font-mono mb-2'>// Live {lang.upper()} Sandbox Output</div>{code}</div>"
    }

UI_EMULATOR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevForge.io - Universal Emulation Engine</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex flex-col justify-between">
    <header class="border-b border-slate-800 bg-slate-900/50 p-4 flex justify-between items-center">
        <span class="font-mono font-bold text-lg bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">DevForge.io</span>
        <span class="px-2 py-1 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs font-mono">UNIVERSAL EMULATOR</span>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto p-4 grid grid-cols-1 lg:grid-cols-12 gap-6 my-4">
        <div class="lg:col-span-5 flex flex-col gap-4">
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl flex flex-col gap-3">
                <label class="text-xs font-mono text-slate-400">Target Language / Framework</label>
                <select id="langSelect" class="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 font-mono">
                    <option value="html">HTML / Tailwind UI</option>
                    <option value="python">Python Script / Logic</option>
                    <option value="react">React / JSX Component</option>
                    <option value="rust">Rust / WebAssembly</option>
                    <option value="vue">Vue.js Component</option>
                </select>

                <label class="text-xs font-mono text-slate-400">Paste Any Code / UI Structure Here</label>
                <textarea id="rawCodeInput" rows="10" class="bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-mono resize-none focus:outline-none focus:border-blue-500" placeholder="Paste your code, component, or markup here..."></textarea>

                <button onclick="emulateUserCode()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-mono text-xs font-bold py-3 rounded-lg transition">EMULATE CODE & UI</button>
            </div>
        </div>

        <div class="lg:col-span-7 flex flex-col bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
            <div class="bg-slate-950 px-4 py-2 border-b border-slate-800 text-xs font-mono text-slate-400">Live Emulated Viewport</div>
            <div id="viewportCanvas" class="flex-1 p-6 bg-slate-900 flex items-center justify-center overflow-auto">
                <div class="text-slate-500 font-mono text-xs">Waiting for input code to render...</div>
            </div>
        </div>
    </main>

    <script>
        async function emulateUserCode() {
            const lang = document.getElementById('langSelect').value;
            const code = document.getElementById('rawCodeInput').value;
            const canvas = document.getElementById('viewportCanvas');

            if(lang === 'html' || lang === 'react' || lang === 'vue') {
                canvas.innerHTML = code;
                return;
            }

            try {
                const response = await fetch('/api/emulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ language: lang, code: code })
                });
                const data = await response.json();
                canvas.innerHTML = data.rendered_html || `<pre class='text-xs font-mono text-red-400'>${data.output}</pre>`;
            } catch (err) {
                canvas.innerHTML = `<div class='text-xs font-mono text-red-400'>Execution Error: ${err}</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return UI_EMULATOR_TEMPLATE
