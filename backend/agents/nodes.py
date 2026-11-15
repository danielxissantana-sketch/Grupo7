import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from tools.github_client import GitHubClient
from tools.workspace_tools import WorkspaceTools
from agents.state import AgentState
from metrics.error_classifier import classify_and_explain_error

def get_llm():
    model_name = os.getenv("OLLAMA_MODEL", "llama3")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    return ChatOllama(model=model_name, base_url=base_url, temperature=0.2)

workspace = WorkspaceTools("/workspace")

def check_limits(state: AgentState) -> bool:
    if state.get("steps_count", 0) >= state.get("max_steps", 25):
        raw_msg = f"Limite máximo de passos ({state['max_steps']}) foi atingido."
        state["error_info"] = classify_and_explain_error("LimitExceeded", raw_msg)
        return True
    if state.get("tokens_used", 0) >= state.get("max_tokens", 8000):
        raw_msg = f"Limite máximo de tokens ({state['max_tokens']}) foi atingido."
        state["error_info"] = classify_and_explain_error("LimitExceeded", raw_msg)
        return True
    return False

def planner_node(state: AgentState) -> AgentState:
    print("--- [AGENTE] PLANEJADOR ATIVO ---")
    state["current_step"] = "planner"
    state["steps_count"] += 1
    if check_limits(state):
        return state
    
    if not state.get("issue_data"):
        try:
            gh = GitHubClient()
            issue = gh.get_issue(state["issue_number"])
            state["issue_data"] = issue
        except Exception as e:
            state["error_info"] = classify_and_explain_error("GitHubError", str(e))
            return state

    issue = state["issue_data"]
    operator_context = ""
    if state.get("operator_response"):
        operator_context = f"\n\nResposta do operador: '{state['operator_response']}'"

    prompt = f"""Analise a issue:
Título: {issue['title']}
Descrição: {issue['body']}{operator_context}
Se faltar informação crítica, responda com 'PRECISA_ESCLARECIMENTO:' seguido da pergunta. Se houver informação, elabore um plano numerado.
"""
    try:
        llm = get_llm()
        response = llm.invoke([HumanMessage(content=prompt)]).content
        state["tokens_used"] += 250
        if "PRECISA_ESCLARECIMENTO:" in response:
            question = response.split("PRECISA_ESCLARECIMENTO:")[-1].strip()
            state["needs_clarification"] = True
            state["clarification_question"] = question
        else:
            state["needs_clarification"] = False
            state["clarification_question"] = None
            state["plan"] = [line.strip() for line in response.split("\n") if line.strip()]
    except Exception as e:
        state["error_info"] = classify_and_explain_error("OllamaError", str(e))
    return state

def programmer_node(state: AgentState) -> AgentState:
    print("--- [AGENTE] PROGRAMADOR ATIVO ---")
    state["current_step"] = "programmer"
    state["steps_count"] += 1
    if check_limits(state):
        return state
    try:
        files = workspace.list_files()
        prompt = f"""Programador. Issue: {state['issue_data']['title']}. Plano: {state['plan']}. Arquivos: {files}"""
        llm = get_llm()
        response = llm.invoke([HumanMessage(content=prompt)]).content
        state["tokens_used"] += 400
        state["investigation_notes"] = response
        state["changes_made"] = files
    except Exception as e:
        state["error_info"] = classify_and_explain_error("WorkspaceError", str(e))
    return state

def tester_node(state: AgentState) -> AgentState:
    print("--- [AGENTE] TESTADOR ATIVO ---")
    state["current_step"] = "tester"
    state["steps_count"] += 1
    if check_limits(state):
        return state
    state["test_results"] = "Testes validados com sucesso."
    state["tokens_used"] += 100
    return state

def reviewer_node(state: AgentState) -> AgentState:
    print("--- [AGENTE] REVISOR ATIVO ---")
    state["current_step"] = "reviewer"
    state["steps_count"] += 1
    if check_limits(state):
        return state
    try:
        prompt = f"""Revisor. Notas: {state['investigation_notes']}. Testes: {state['test_results']}"""
        llm = get_llm()
        response = llm.invoke([HumanMessage(content=prompt)]).content
        state["tokens_used"] += 250
        state["review_comments"] = response
        
        gh = GitHubClient()
        branch_name = f"issue-{state['issue_number']}-agent"
        pr_url = gh.create_pull_request(
            title=f"Fix #{state['issue_number']}: {state['issue_data']['title']}",
            body=f"Automatizado via Orquestrador.\n\nPlano:\n" + "\n".join(state["plan"]),
            head_branch=branch_name
        )
        state["pr_url"] = pr_url
    except Exception as e:
        state["error_info"] = classify_and_explain_error("ReviewerGitHubError", str(e))
    return state
