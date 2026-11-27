# Índice de Evidências — Tema 7 (Orquestrador Multi-Agente)

Este índice conecta os requisitos do projeto e as afirmações do trabalho de pesquisa às suas respectivas evidências auditáveis neste repositório.

## 1. Vídeo de Demonstração (Tela Inteira)
- **Arquivo:** `evidencias/demo_orquestrador_grupo7.mp4`
- **O que demonstra:** Inicialização do ambiente via `docker-compose up`, abertura do painel web, execução dos agentes (Planejador, Programador, Testador e Revisor), pausa e retomada *Human-in-the-Loop* e geração automática de Pull Request no GitHub.

## 2. Integração Contínua (GitHub Actions — Tag `v1.0`)
- **Link da Execução Verde:** `https://github.com/danielxissantana-sketch/Grupo7/actions` *(atualizar com o link direto da execução da tag `v1.0`)*
- **Captura de Tela:** `evidencias/05_github_actions_v1.png`

## 3. Tabela de Rastreabilidade (Afirmação x Evidência)

| # | Afirmação / Requisito Comprovado | Arquivo de Prova | Como Conferir |
| :-: | :--- | :--- | :--- |
| 1 | O sistema sobe localmente a custo zero com FastAPI, LangGraph e Ollama (`llama3.2`) | `evidencias/01_painel_online.png` | Indicador verde *Sistema Online* no painel (`localhost:8000`) |
| 2 | O agente Planejador identifica ambiguidade na issue e solicita ajuda humana antes de codificar | `evidencias/02_pausa_human_in_the_loop.png` | Caixa amarela exibindo perguntas de esclarecimento ao operador |
| 3 | Após validação no `pytest`, o agente Revisor abre automaticamente o Pull Request no GitHub | `evidencias/03_fluxo_concluido_pr.png` | Painel exibindo `Passou no pytest?: Sim` e o link do PR gerado |
| 4 | O orquestrador impede loops infinitos e gasto excessivo bloqueando execuções ao atingir o teto | `evidencias/04_erro_limite_excedido.png` | Caixa vermelha (`LimitExceeded`) interrompendo o fluxo por limite |
| 5 | Todas as etapas e decisões dos 4 agentes são registradas cronologicamente | `evidencias/execucao_completa.log` | Logs completos do container com data, hora, entradas e saídas |
| 6 | Avaliação experimental com taxa de resolução, consumo médio de tokens, tempo e falhas | `eval/relatorio_execucoes.csv` e `eval/RELATORIO_METRICAS.md` | Executar `python eval/run_eval.py` para regenerar os dados |