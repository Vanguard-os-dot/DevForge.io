# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os
import json
from core.engine import NativeLocalAI

app = FastAPI()
ai_engine = NativeLocalAI()

workspace_state = {
    "projects": ["Default Project"],
    "snippets": ["HTML Boilerplate"],
    "terminal_logs": ["[INFO] System initialized.", "[INFO] Local AI core loaded."],
    "current_code": ""
}

@app.get("/", response_class=HTMLResponse)
async def get_root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(json.dumps({"type": "INIT", "data": workspace_state}))
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action")
            
            if action == "AI_PROMPT":
                prompt = message.get("prompt", "")
                workspace_state["terminal_logs"].append(f"[AI] Processing local prompt: {prompt}")
                
                generated_code = ai_engine.generate(prompt)
                workspace_state["current_code"] = generated_code
                workspace_state["terminal_logs"].append("[AI] Generated payload locally.")
                
                await websocket.send_text(json.dumps({
                    "type": "AI_RESPONSE",
                    "code": generated_code,
                    "logs": workspace_state["terminal_logs"]
                }))
                
            elif action == "SAVE_CODE":
                workspace_state["current_code"] = message.get("code", "")
                workspace_state["terminal_logs"].append("[INFO] Workspace code synchronized.")
                await websocket.send_text(json.dumps({
                    "type": "SYNC_ACK",
                    "logs": workspace_state["terminal_logs"]
                }))
                
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

