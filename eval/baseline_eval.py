"""
baseline_eval.py — Baseline de chamada única (Tema 7)
Busca as issues direto da API do GitHub.

Uso:
    export GITHUB_TOKEN=ghp_xxx
    export GITHUB_REPO=usuario/repositorio
    python baseline_eval.py
    python baseline_eval.py --issues 1 7 10
    python baseline_eval.py --limite 30

Saída:
    eval/baseline_execucoes.csv
    eval/baseline_logs/issue_NN.json
"""

import os
import csv
import json
import time
import argparse
import subprocess
from datetime import datetime

import requests

# ---------------------------------------------------------------- CONFIG
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "")   # ex.: "danielxissantana-sketch/Grupo7"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"
REPO_DIR = os.environ.get("REPO_DIR", "./repo_teste")
CSV_PATH = "eval/baseline_execucoes.csv"
LOG_DIR = "eval/baseline_logs"
MAX_TOKENS = 4096
TIMEOUT_S = 1800
LIMITE_ISSUES = 30

CABECALHO = [
    "Data/Hora", "Issue", "Passou no pytest?",
    "Tokens Usados", "Tempo (segundos)", "Motivo da Falha", "Pull Request",
]

PROMPT_SISTEMA = """Você é um engenheiro de software. Receba uma issue e o
contexto do repositório e produza o diff completo que resolve a issue.

Regras:
- Responda APENAS com um bloco de diff unificado válido (formato git diff).
- Não inclua explicações antes ou depois do diff.
- Não altere arquivos fora do escopo da issue.
- Se não for possível resolver, responda exatamente: NAO_RESOLVIDO
"""


# ---------------------------------------------------------------- GITHUB
def listar_issues(limite: int, filtro: list | None = None) -> list[dict]:
    """Busca issues abertas/fechadas do repositório, em ordem crescente."""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        raise SystemExit("Defina GITHUB_TOKEN e GITHUB_REPO no ambiente.")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    params = {"state": "all", "per_page": 100, "sort": "created", "direction": "asc"}

    issues, pagina = [], 1
    while len(issues) < limite:
        params["page"] = pagina
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        lote = r.json()
        if not lote:
            break
        for item in lote:
            if "pull_request" in item:      # ignora PRs
                continue
            if filtro and item["number"] not in filtro:
                continue
            issues.append({
                "numero": item["number"],
                "titulo": item["title"],
                "texto": f"# {item['title']}\n\n{item.get('body') or ''}",
            })
            if len(issues) >= limite:
                break
        pagina += 1

    if not issues:
        raise SystemExit("Nenhuma issue encontrada com os filtros informados.")
    return issues


# ---------------------------------------------------------------- OLLAMA
def chamar_modelo(prompt: str) -> dict:
    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": MAX_TOKENS, "temperature": 0.2},
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT_S)
    r.raise_for_status()
    d = r.json()
    return {
        "texto": d.get("response", ""),
        "tokens_prompt": d.get("prompt_eval_count", 0),
        "tokens_gerados": d.get("eval_count", 0),
    }


def montar_prompt(issue_texto: str, contexto: str) -> str:
    return f"""{PROMPT_SISTEMA}

=== ISSUE ===
{issue_texto}

=== CONTEXTO DO REPOSITÓRIO ===
{contexto}

=== DIFF ===
"""


# ---------------------------------------------------------------- REPO
def contexto_repositorio() -> str:
    partes = []
    for raiz, _, arquivos in os.walk(REPO_DIR):
        if ".git" in raiz or "__pycache__" in raiz:
            continue
        for nome in sorted(arquivos):
            if not nome.endswith(".py"):
                continue
            caminho = os.path.join(raiz, nome)
            rel = os.path.relpath(caminho, REPO_DIR)
            try:
                with open(caminho, encoding="utf-8") as f:
                    partes.append(f"--- {rel} ---\n{f.read()}")
            except Exception:
                continue
    return "\n\n".join(partes)


def restaurar_repo() -> None:
    subprocess.run(["git", "checkout", "--", "."], cwd=REPO_DIR, check=False)
    subprocess.run(["git", "clean", "-fd"], cwd=REPO_DIR, check=False)


def aplicar_diff(diff: str) -> bool:
    if not diff.strip() or "NAO_RESOLVIDO" in diff:
        return False
    p = subprocess.run(
        ["git", "apply", "--whitespace=nowarn", "-"],
        input=diff, text=True, cwd=REPO_DIR, capture_output=True,
    )
    return p.returncode == 0


def rodar_pytest() -> bool:
    p = subprocess.run(
        ["python", "-m", "pytest", "-q", "--tb=no"],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    return p.returncode == 0


# ---------------------------------------------------------------- MAIN
def executar_issue(issue: dict, contexto: str) -> dict:
    restaurar_repo()
    inicio = time.time()
    ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    reg = {
        "Data/Hora": ts,
        "Issue": f"#{issue['numero']} - {issue['titulo'][:80]}",
        "Passou no pytest?": "Não",
        "Tokens Usados": 0,
        "Tempo (segundos)": 0.0,
        "Motivo da Falha": "",
        "Pull Request": "-",
    }
    log = {"issue": issue["numero"], "timestamp": ts, "etapas": []}

    try:
        resp = chamar_modelo(montar_prompt(issue["texto"], contexto))
        reg["Tokens Usados"] = resp["tokens_prompt"] + resp["tokens_gerados"]
        log["etapas"].append({
            "etapa": "chamada_unica",
            "tokens_prompt": resp["tokens_prompt"],
            "tokens_gerados": resp["tokens_gerados"],
        })

        if not aplicar_diff(resp["texto"]):
            reg["Motivo da Falha"] = "Diff inválido ou não aplicável"
            log["etapas"].append({"etapa": "aplicar_diff", "ok": False})
        else:
            log["etapas"].append({"etapa": "aplicar_diff", "ok": True})
            if rodar_pytest():
                reg["Passou no pytest?"] = "Sim"
                reg["Motivo da Falha"] = "Nenhuma falha (Concluído com sucesso)"
            else:
                reg["Motivo da Falha"] = "Quebrou outro teste"

    except requests.exceptions.Timeout:
        reg["Motivo da Falha"] = "Timeout na chamada ao modelo"
    except Exception as e:
        reg["Motivo da Falha"] = f"Infraestrutura: {type(e).__name__}"

    reg["Tempo (segundos)"] = round(time.time() - inicio, 2)
    log["resultado"] = reg

    os.makedirs(LOG_DIR, exist_ok=True)
    with open(f"{LOG_DIR}/issue_{issue['numero']:02d}.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    return reg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--issues", nargs="*", type=int, default=None)
    ap.add_argument("--limite", type=int, default=LIMITE_ISSUES)
    args = ap.parse_args()

    issues = listar_issues(args.limite, args.issues)
    print(f"{len(issues)} issues carregadas do GitHub.")

    contexto = contexto_repositorio()
    os.makedirs("eval", exist_ok=True)

    novo = not os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CABECALHO, delimiter=";")
        if novo:
            w.writeheader()
        for i, issue in enumerate(issues, 1):
            print(f"[{i}/{len(issues)}] issue #{issue['numero']}")
            w.writerow(executar_issue(issue, contexto))
            f.flush()

    print(f"\nConcluído. Resultados em {CSV_PATH}")


if __name__ == "__main__":
    main()