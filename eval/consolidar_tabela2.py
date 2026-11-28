"""
consolidar_tabela2.py — Gera a Tabela 2 do trabalho ABNT

Lê os dois CSVs (multiagente e baseline) e produz:
    eval/tabela2.md    (tabela em Markdown)
    eval/tabela2.csv   (dados brutos consolidados)

Uso:
    python consolidar_tabela2.py
    python consolidar_tabela2.py --multi eval/relatorio_execucoes.csv \
                                 --baseline eval/baseline_execucoes.csv
"""

import csv
import argparse
from collections import defaultdict

MULTI = "eval/relatorio_execucoes.csv"
BASE = "eval/baseline_execucoes.csv"


def ler(caminho: str) -> list[dict]:
    with open(caminho, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def numero_issue(texto: str) -> str:
    """Extrai '#17' de '#17 - Cupom de desconto'."""
    return texto.split(" - ")[0].strip()


def resumir(linhas: list[dict], nome: str) -> dict:
    total_exec = len(linhas)
    sucessos = sum(1 for r in linhas if r.get("Passou no pytest?") == "Sim")

    por_issue = defaultdict(list)
    for r in linhas:
        por_issue[numero_issue(r["Issue"])].append(r.get("Passou no pytest?") == "Sim")

    issues_distintas = len(por_issue)
    issues_resolvidas = sum(1 for v in por_issue.values() if any(v))

    tokens = [float(r.get("Tokens Usados") or 0) for r in linhas]
    tempos = [float(r.get("Tempo (segundos)") or 0) for r in linhas]

    return {
        "sistema": nome,
        "execucoes": total_exec,
        "sucessos_execucao": sucessos,
        "taxa_execucao": round(100 * sucessos / total_exec, 2) if total_exec else 0.0,
        "issues_distintas": issues_distintas,
        "issues_resolvidas": issues_resolvidas,
        "taxa_issue": round(100 * issues_resolvidas / issues_distintas, 2) if issues_distintas else 0.0,
        "tokens_media": round(sum(tokens) / total_exec, 2) if total_exec else 0.0,
        "tempo_media": round(sum(tempos) / total_exec, 2) if total_exec else 0.0,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--multi", default=MULTI)
    ap.add_argument("--baseline", default=BASE)
    args = ap.parse_args()

    multi = resumir(ler(args.multi), "Sistema multiagente")

    try:
        base = resumir(ler(args.baseline), "Baseline (chamada única)")
    except FileNotFoundError:
        base = None
        print(f"Aviso: {args.baseline} não encontrado. Tabela 2 ficará parcial.")

    linhas = [base, multi] if base else [multi]

    # ---------------- Markdown
    md = ["Tabela 2 – Comparação entre o sistema multiagente e o baseline de chamada única\n"]
    md.append("| Sistema | Issues resolvidas | Taxa de resolução | Tokens médios por issue | Tempo médio por issue |")
    md.append("| :--- | :---: | :---: | :---: | :---: |")
    for r in linhas:
        md.append(
            f"| {r['sistema']} | {r['issues_resolvidas']} de {r['issues_distintas']} "
            f"| {r['taxa_issue']}% | {r['tokens_media']} | {r['tempo_media']} s |"
        )
    md.append("\nFonte: elaborado pelos autores (2026).")

    with open("eval/tabela2.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    # ---------------- CSV
    campos = ["sistema", "execucoes", "sucessos_execucao", "taxa_execucao",
              "issues_distintas", "issues_resolvidas", "taxa_issue",
              "tokens_media", "tempo_media"]
    with open("eval/tabela2.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        w.writeheader()
        w.writerows(linhas)

    print("\n".join(md))
    print("\nGerados: eval/tabela2.md e eval/tabela2.csv")


if __name__ == "__main__":
    main()