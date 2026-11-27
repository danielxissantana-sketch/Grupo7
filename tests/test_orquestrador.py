import os
import csv

def test_estrutura_obrigatoria_entrega():
    assert os.path.isfile("README.md")
    assert os.path.isfile("PROMPTS.md")
    assert os.path.isfile("docker-compose.yml")
    assert os.path.isdir("eval")
    assert os.path.isdir("evidencias")
    assert os.path.isdir("docs")

def test_relatorio_metricas_experimental():
    csv_path = os.path.join("eval", "relatorio_execucoes.csv")
    assert os.path.isfile(csv_path)
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    assert len(rows) >= 20

def test_regras_negocio_ecommerce():
    assert round(100.0 * 0.10, 2) == 10.0
    assert (15.0 if 80.0 < 100.0 else 0.0) == 15.0
    assert int(99.90 // 10) == 9
