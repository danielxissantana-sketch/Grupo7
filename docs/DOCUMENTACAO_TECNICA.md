# Documentação Técnica — Orquestrador Multi-Agente (Tema 7)

## 1. Visão Geral e Arquitetura

O sistema automatiza o ciclo de resolução de *issues* do GitHub até a abertura de *Pull Requests* validados por testes, utilizando uma arquitetura multiagente com limites de execução e intervenção humana (*Human-in-the-Loop*).

```mermaid
flowchart TD
    A[Usuário / Painel Web] -->|Issue # + Limites| B[FastAPI Backend]
    B --> C[1. Agente Planejador - Llama 3.2]
    C -->|Falta informação?| D{Precisa de Ajuda?}
    D -->|Sim| E[Pausa: Caixa Amarela no Painel]
    E -->|Resposta Humana| C
    D -->|Não| F[2. Agente Programador]
    F --> G[3. Agente Testador - pytest]
    G -->|Passou?| H{Testes OK?}
    H -->|Não| I[Registra Falha em eval/]
    H -->|Sim| J[4. Agente Revisor]
    J --> K[Abre Pull Request no GitHub]
    K --> L[Salva Métricas CSV/MD]