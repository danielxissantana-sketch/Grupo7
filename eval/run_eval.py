import os
import csv
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "relatorio_execucoes.csv")
MD_PATH = os.path.join(BASE_DIR, "RELATORIO_METRICAS.md")

def gerar_relatorio():
    if not os.path.isfile(CSV_PATH):
        print("Arquivo relatorio_execucoes.csv não encontrado.")
        return

    with open(CSV_PATH, mode="r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f, delimiter=";"))

    total = len(rows)
    sucessos = sum(1 for r in rows if r.get("Passou no pytest?") == "Sim")
    falhas = total - sucessos
    taxa = round((sucessos / total) * 100, 1) if total > 0 else 0.0
    media_tokens = round(sum(float(r.get("Tokens Usados", 0)) for r in rows) / total, 1) if total > 0 else 0.0
    media_tempo = round(sum(float(r.get("Tempo (segundos)", 0)) for r in rows) / total, 2) if total > 0 else 0.0

    categorias_falha = Counter(
        r.get("Motivo da Falha", "Desconhecido")
        for r in rows
        if r.get("Passou no pytest?") != "Sim"
    )

    with open(MD_PATH, mode="w", encoding="utf-8") as mf:
        mf.write("# Relatório de Execuções e Métricas — Tema 7\n\n")
        mf.write("## Resumo Consolidado (Rubricas 2 e 3)\n")
        mf.write(f"- **Total de Execuções Registradas:** {total}\n")
        mf.write(f"- **Taxa de Resolução (`pytest` aprovado):** {taxa}% ({sucessos}/{total})\n")
        mf.write(f"- **Total de Falhas Registradas:** {falhas}\n")
        mf.write(f"- **Consumo Médio de Tokens por Issue:** {media_tokens} tokens\n")
        mf.write(f"- **Tempo Médio de Resolução por Issue:** {media_tempo} segundos\n\n")

        mf.write("## Análise de Falhas por Categoria\n\n")
        if categorias_falha:
            mf.write("| Categoria / Motivo da Falha | Ocorrências |\n")
            mf.write("| :--- | :---: |\n")
            for motivo, qtd in categorias_falha.items():
                mf.write(f"| {motivo} | {qtd} |\n")
        else:
            mf.write("Nenhuma falha registrada.\n")

        mf.write("\n## Histórico Detalhado por Issue\n\n")
        mf.write("| Data/Hora | Issue | Passou no pytest? | Tokens Usados | Tempo (s) | Motivo da Falha | Pull Request |\n")
        mf.write("| :--- | :--- | :---: | :---: | :---: | :--- | :--- |\n")
        for r in rows:
            mf.write(
                f"| {r.get('Data/Hora')} | {r.get('Issue')} | {r.get('Passou no pytest?')} | "
                f"{r.get('Tokens Usados')} | {r.get('Tempo (segundos)')} | {r.get('Motivo da Falha')} | {r.get('Pull Request')} |\n"
            )

    print(f"Relatório atualizado com sucesso! Total: {total} execuções | Taxa de resolução: {taxa}%")

if __name__ == "__main__":
    gerar_relatorio()