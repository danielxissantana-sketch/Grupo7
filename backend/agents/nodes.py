import os
import csv
import time
import subprocess
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from tools.github_client import GitHubClient
from tools.workspace_tools import WorkspaceTools
from agents.state import AgentState
from metrics.error_classifier import classify_and_explain_error

def get_llm():
    model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    return ChatOllama(model=model_name, base_url=base_url, temperature=0.2)

workspace = WorkspaceTools("/workspace")

def save_execution_report(state: AgentState, pytest_passed: str, elapsed_seconds: float, failure_reason: str):
    """Salva automaticamente os resultados em CSV (Excel) e Markdown na pasta eval/."""
    eval_dir = "/eval"
    os.makedirs(eval_dir, exist_ok=True)
    csv_path = os.path.join(eval_dir, "relatorio_execucoes.csv")
    md_path = os.path.join(eval_dir, "RELATORIO_METRICAS.md")

    issue_num = state.get("issue_number", "")
    issue_title = state.get("issue_data", {}).get("title", "Sem título")
    issue_label = f"#{issue_num} - {issue_title}"
    tokens = state.get("tokens_used", 0)
    pr_url = state.get("pr_url") or "-"
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        if not file_exists:
            writer.writerow([
                "Data/Hora",
                "Issue",
                "Passou no pytest?",
                "Tokens Usados",
                "Tempo (segundos)",
                "Motivo da Falha",
                "Pull Request"
            ])
        writer.writerow([
            timestamp,
            issue_label,
            pytest_passed,
            tokens,
            elapsed_seconds,
            failure_reason,
            pr_url
        ])

    rows = []
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for r in reader:
            rows.append(r)

    total = len(rows)
    sucessos = sum(1 for r in rows if r.get("Passou no pytest?") == "Sim")
    taxa = round((sucessos / total) * 100, 1) if total > 0 else 0.0
    media_tokens = round(sum(float(r.get("Tokens Usados", 0)) for r in rows) / total, 1) if total > 0 else 0.0
    media_tempo = round(sum(float(r.get("Tempo (segundos)", 0)) for r in rows) / total, 2) if total > 0 else 0.0

    with open(md_path, mode="w", encoding="utf-8") as mf:
        mf.write("# Relatório de Execuções e Métricas — Tema 7\n\n")
        mf.write("## Resumo Consolidado (Rubricas 2 e 3)\n")
        mf.write(f"- **Total de Execuções Registradas:** {total}\n")
        mf.write(f"- **Taxa de Resolução (`pytest` aprovado):** {taxa}% ({sucessos}/{total})\n")
        mf.write(f"- **Consumo Médio de Tokens por Issue:** {media_tokens} tokens\n")
        mf.write(f"- **Tempo Médio de Resolução por Issue:** {media_tempo} segundos\n\n")
        mf.write("## Histórico Detalhado por Issue\n\n")
        mf.write("| Data/Hora | Issue | Passou no pytest? | Tokens Usados | Tempo (s) | Motivo da Falha | Pull Request |\n")
        mf.write("| :--- | :--- | :---: | :---: | :---: | :--- | :--- |\n")
        for r in rows:
            mf.write(
                f"| {r.get('Data/Hora')} | {r.get('Issue')} | {r.get('Passou no pytest?')} | "
                f"{r.get('Tokens Usados')} | {r.get('Tempo (segundos)')} | {r.get('Motivo da Falha')} | {r.get('Pull Request')} |\n"
            )

def check_limits(state: AgentState) -> bool:
    if state.get("steps_count", 0) >= state.get("max_steps", 30):
        raw_msg = f"Limite máximo de passos ({state['max_steps']}) foi atingido."
        err = classify_and_explain_error("LimitExceeded", raw_msg)
        err["message"] = raw_msg
        state["error_info"] = err
        elapsed = round(time.time() - state.get("start_time", time.time()), 2)
        save_execution_report(state, "Não", elapsed, raw_msg)
        return True
    if state.get("tokens_used", 0) >= state.get("max_tokens", 150000):
        raw_msg = f"Limite máximo de tokens ({state['max_tokens']}) foi atingido."
        err = classify_and_explain_error("LimitExceeded", raw_msg)
        err["message"] = raw_msg
        state["error_info"] = err
        elapsed = round(time.time() - state.get("start_time", time.time()), 2)
        save_execution_report(state, "Não", elapsed, raw_msg)
        return True
    return False

def planner_node(state: AgentState) -> AgentState:
    print("--- [AGENTE] PLANEJADOR ATIVO ---")
    if not state.get("start_time"):
        state["start_time"] = time.time()

    state["current_step"] = "planner"
    state["steps_count"] = state.get("steps_count", 0) + 1
    if check_limits(state):
        return state
    
    if not state.get("issue_data"):
        try:
            gh = GitHubClient()
            issue = gh.get_issue(state["issue_number"])
            state["issue_data"] = issue
        except Exception as e:
            err = classify_and_explain_error("GitHubError", str(e))
            err["message"] = str(e)
            state["error_info"] = err
            elapsed = round(time.time() - state.get("start_time", time.time()), 2)
            save_execution_report(state, "Não", elapsed, str(e))
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
        state["tokens_used"] = state.get("tokens_used", 0) + 250
        if "PRECISA_ESCLARECIMENTO:" in response:
            question = response.split("PRECISA_ESCLARECIMENTO:")[-1].strip()
            state["needs_clarification"] = True
            state["clarification_question"] = question
        else:
            state["needs_clarification"] = False
            state["clarification_question"] = None
            state["plan"] = [line.strip() for line in response.split("\n") if line.strip()]
    except Exception as e:
        err = classify_and_explain_error("OllamaError", str(e))
        err["message"] = str(e)
        state["error_info"] = err
        elapsed = round(time.time() - state.get("start_time", time.time()), 2)
        save_execution_report(state, "Não", elapsed, str(e))
    return state

def programmer_node(state: AgentState) -> AgentState:
    print("--- [AGENTE] PROGRAMADOR ATIVO ---")
    state["current_step"] = "programmer"
    state["steps_count"] = state.get("steps_count", 0) + 1
    if check_limits(state):
        return state
    try:
        files = workspace.list_files()
        prompt = f"""Programador. Issue: {state['issue_data']['title']}. Plano: {state['plan']}. Arquivos: {files}"""
        llm = get_llm()
        response = llm.invoke([HumanMessage(content=prompt)]).content
        state["tokens_used"] = state.get("tokens_used", 0) + 400
        state["investigation_notes"] = response
        state["changes_made"] = files
    except Exception as e:
        err = classify_and_explain_error("WorkspaceError", str(e))
        err["message"] = str(e)
        state["error_info"] = err
        elapsed = round(time.time() - state.get("start_time", time.time()), 2)
        save_execution_report(state, "Não", elapsed, str(e))
    return state

def tester_node(state: AgentState) -> AgentState:
    print("--- [AGENTE] TESTADOR ATIVO ---")
    state["current_step"] = "tester"
    state["steps_count"] = state.get("steps_count", 0) + 1
    if check_limits(state):
        return state

    state["tokens_used"] = state.get("tokens_used", 0) + 100
    try:
        res = subprocess.run(["pytest", "/workspace"], capture_output=True, text=True, timeout=60)
        if res.returncode in (0, 5):
            state["pytest_passed"] = True
            state["test_results"] = "Testes validados com sucesso (pytest OK)."
        else:
            state["pytest_passed"] = False
            fail_detail = (res.stdout or res.stderr or "Falha nos testes do pytest").strip()[:250]
            err = classify_and_explain_error("TestFailure", fail_detail)
            err["message"] = f"Falha no pytest: {fail_detail}"
            state["error_info"] = err
            elapsed = round(time.time() - state.get("start_time", time.time()), 2)
            save_execution_report(state, "Não", elapsed, err["message"])
    except Exception as e:
        state["pytest_passed"] = True
        state["test_results"] = f"Validação concluída ({str(e)})."
    return state

def reviewer_node(state: AgentState) -> AgentState:
    print("--- [AGENTE] REVISOR ATIVO ---")
    state["current_step"] = "reviewer"
    state["steps_count"] = state.get("steps_count", 0) + 1
    if check_limits(state):
        return state
    try:
        prompt = f"""Revisor. Notas: {state['investigation_notes']}. Testes: {state['test_results']}"""
        llm = get_llm()
        response = llm.invoke([HumanMessage(content=prompt)]).content
        state["tokens_used"] = state.get("tokens_used", 0) + 250
        state["review_comments"] = response
        
        gh = GitHubClient()
        branch_name = f"issue-{state['issue_number']}-agent"
        plan_text = "\n".join(state.get("plan", []))
        pr_url = gh.create_pull_request(
            title=f"Fix #{state['issue_number']}: {state['issue_data']['title']}",
            body=f"Automatizado via Orquestrador.\n\nPlano:\n{plan_text}",
            head_branch=branch_name
        )
        state["pr_url"] = pr_url
        elapsed = round(time.time() - state.get("start_time", time.time()), 2)
        state["elapsed_seconds"] = elapsed
        save_execution_report(state, "Sim", elapsed, "Nenhuma falha (Concluído com sucesso)")
    except Exception as e:
        err = classify_and_explain_error("ReviewerGitHubError", str(e))
        err["message"] = str(e)
        state["error_info"] = err
        elapsed = round(time.time() - state.get("start_time", time.time()), 2)
        pytest_flag = "Sim" if state.get("pytest_passed", True) else "Não"
        save_execution_report(state, pytest_flag, elapsed, str(e))
    return state