from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import os
import asyncio
import json
from sse_starlette.sse import EventSourceResponse
from langgraph.checkpoint.memory import MemorySaver
from tools.github_client import GitHubClient
from tools.workspace_tools import WorkspaceTools
from agents.graph import build_orchestrator_graph

app = FastAPI(title="LangGraph Multi-Agent Orchestrator", version="9.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workspace = WorkspaceTools("/workspace")
memory_saver = MemorySaver()
orchestrator_graph = build_orchestrator_graph(checkpointer=memory_saver)

class OperatorInput(BaseModel):
    response: str

class RunConfigInput(BaseModel):
    max_steps: int = Field(default=int(os.getenv("MAX_STEPS", 25)))
    max_tokens: int = Field(default=int(os.getenv("MAX_TOKENS", 8000)))

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = "/frontend/index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Painel HTML não encontrado na pasta frontend!</h1>"

@app.get("/health")
def health_check():
    return {"health": "ok"}

@app.get("/metrics/{issue_number}")
def get_orchestrator_metrics(issue_number: int):
    thread_config = {"configurable": {"thread_id": f"issue-{issue_number}"}}
    existing_state = orchestrator_graph.get_state(thread_config)
    if not existing_state or not existing_state.values:
        raise HTTPException(status_code=404, detail="Nenhuma métrica encontrada.")
    state = existing_state.values
    return {
        "success": True,
        "issue_number": state.get("issue_number"),
        "current_step": state.get("current_step"),
        "steps_count": state.get("steps_count", 0),
        "max_steps": state.get("max_steps", 25),
        "tokens_used": state.get("tokens_used", 0),
        "max_tokens": state.get("max_tokens", 8000),
        "paused": state.get("needs_clarification", False),
        "error_info": state.get("error_info"),
        "pr_url": state.get("pr_url")
    }

@app.get("/stream/{issue_number}")
async def stream_orchestrator_events(issue_number: int):
    thread_config = {"configurable": {"thread_id": f"issue-{issue_number}"}}
    async def event_generator():
        while True:
            existing_state = orchestrator_graph.get_state(thread_config)
            if existing_state and existing_state.values:
                state = existing_state.values
                current_step = state.get("current_step", "start")
                yield {
                    "event": "agent_update",
                    "data": json.dumps({
                        "current_step": current_step,
                        "steps_count": state.get("steps_count", 0),
                        "tokens_used": state.get("tokens_used", 0),
                        "paused": state.get("needs_clarification", False),
                        "question": state.get("clarification_question"),
                        "error_info": state.get("error_info"),
                        "pr_url": state.get("pr_url")
                    })
                }
                if state.get("needs_clarification") or state.get("error_info") or current_step == "reviewer":
                    await asyncio.sleep(1)
                    yield {"event": "finish", "data": json.dumps({"message": "Finalizado ou Pausado."})}
                    break
            await asyncio.sleep(1.5)
    return EventSourceResponse(event_generator())

@app.post("/run/{issue_number}")
def run_orchestrator(issue_number: int, config_input: RunConfigInput = None):
    thread_config = {"configurable": {"thread_id": f"issue-{issue_number}"}}
    max_steps = config_input.max_steps if config_input else int(os.getenv("MAX_STEPS", 25))
    max_tokens = config_input.max_tokens if config_input else int(os.getenv("MAX_TOKENS", 8000))

    existing_state = orchestrator_graph.get_state(thread_config)
    if existing_state and existing_state.values and existing_state.values.get("needs_clarification"):
        return {"success": False, "paused": True, "question": existing_state.values.get("clarification_question"), "state": existing_state.values}

    initial_state = {
        "issue_number": issue_number, "issue_data": {}, "plan": [],
        "needs_clarification": False, "clarification_question": None, "operator_response": None,
        "investigation_notes": "", "changes_made": [], "test_results": "", "review_comments": "",
        "pr_url": None, "current_step": "start", "error_info": None,
        "steps_count": 0, "tokens_used": 0, "max_steps": max_steps, "max_tokens": max_tokens, "messages": []
    }
    try:
        final_state = orchestrator_graph.invoke(initial_state, config=thread_config)
        if final_state.get("error_info"):
            return {"success": False, "error": True, "error_info": final_state["error_info"], "state": final_state}
        if final_state.get("needs_clarification"):
            return {"success": True, "paused": True, "question": final_state.get("clarification_question"), "state": final_state}
        return {"success": True, "paused": False, "state": final_state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resume/{issue_number}")
def resume_orchestrator(issue_number: int, data: OperatorInput):
    thread_config = {"configurable": {"thread_id": f"issue-{issue_number}"}}
    existing_state = orchestrator_graph.get_state(thread_config)
    if not existing_state or not existing_state.values:
        raise HTTPException(status_code=404, detail="Nenhum estado pausado encontrado.")
    current_values = existing_state.values
    current_values["operator_response"] = data.response
    current_values["needs_clarification"] = False
    current_values["clarification_question"] = None
    try:
        orchestrator_graph.update_state(thread_config, current_values)
        final_state = orchestrator_graph.invoke(None, config=thread_config)
        if final_state.get("error_info"):
            return {"success": False, "error": True, "error_info": final_state["error_info"], "state": final_state}
        return {"success": True, "paused": False, "state": final_state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))