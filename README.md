# Tema 7 — Faça Ticket ao Pull Request: Orquestrador Multi-Agente de Engenharia de Software

Projeto desenvolvido para a disciplina **Projetos de IA na Programação**, com o objetivo de automatizar o ciclo de resolução de *issues* do GitHub até a abertura de *Pull Requests* validados por testes, utilizando arquitetura multi-agente com limites explícitos de execução e intervenção humana (*Human-in-the-Loop*).

---

## Integrantes — Grupo 7

* **Daniel Cosme de Santana** - RA 2410004 - Projeto integrador - EAD_PROINT_100.DD-BD-PI-10-74.2026.74 (Backend e Infraestrutura)
* **Giovana de Jesus Oliveira** - RA 2402906 - Projeto integrador - EAD_PROINT_100.DD-ADS-PI-10-74.2026.74 (IA e Avaliação; co-responsável por Dados e Qualidade)
* **Rodrigo Forcinito Cruz** - RA 2522857 - Projeto integrador - EAD_PROINT_100.DD-BD-PI-10-74.2026.74 (Produto e Interface; co-responsável por Dados e Qualidade)

---

## Problema e Objetivo

Agentes autônomos de engenharia de software frequentemente falham por três motivos principais: não sabem quando parar para pedir esclarecimentos humanos, entram em loops infinitos de correção consumindo excesso de tokens e abrem *Pull Requests* sem validação real de testes.

**Solução implementada:** Um grafo multi-agente orquestrado via **LangGraph** integrado a modelos locais (**Ollama / `llama3.2`**), com:
* Orçamento explícito de execução (**Max Passos** e **Max Tokens**).
* Pausa automática para esclarecimento humano quando a *issue* possui ambiguidade ou falta de especificações.
* Execução automatizada de testes com `pytest` antes da abertura do *Pull Request*.
* Painel web em tempo real e exportação automática de métricas para avaliação das rubricas.

---

## Arquitetura e Fluxo Multi-Agente

O sistema é executado em ambiente containerizado (**Docker**) e coordena quatro agentes especializados conectados por estado persistente (`MemorySaver`):

1. **Agente Planejador (`planner_node`):** Lê o título e a descrição da *issue* diretamente via API do GitHub. Se identificar ausência de informação crítica, pausa o fluxo (`PRECISA_ESCLARECIMENTO:`) e solicita resposta do operador no painel; caso contrário, estrutura o plano técnico de ação.
2. **Agente Programador (`programmer_node`):** Inspeciona os arquivos no diretório `/workspace`, analisa o plano aprovado e prepara as alterações necessárias para atender aos requisitos da *issue*.
3. **Agente Testador (`tester_node`):** Executa a suíte de testes (`pytest`) sobre o `/workspace`, validando se a solução atende aos critérios de aceitação sem quebrar funcionalidades existentes.
4. **Agente Revisor & PR (`reviewer_node`):** Consolida as notas técnicas e os resultados dos testes, cria ou sincroniza a branch dedicada da *issue* (`issue-<numero>-agent`), registra o commit da solução em `resolucoes/` e abre automaticamente o **Pull Request** na branch `main`.

---

## Funcionalidades Implementadas

* **Painel Web em Tempo Real (`http://localhost:8000`):**
  * Acompanhamento ao vivo da ativação de cada agente via *Server-Sent Events* (SSE).
  * Configuração dinâmica de limites (`Max Passos` e `Max Tokens`) e escolha da branch base.
  * Interface interativa **Human-in-the-Loop** para responder dúvidas do Planejador e retomar o fluxo exatamente do ponto de pausa (`/resume/{issue_number}`).
* **Quadro Consolidado de Resultado Final (Rubrica & Relatório):**
  * Confirmação automática do número e título da *issue* em execução.
  * Indicador visual direto de aprovação nos testes (**Passou no pytest?: Sim / Não**).
  * Contabilização de **Tokens Usados** e cronômetro de **Tempo (segundos)** de resolução.
  * Diagnóstico categorizado de falhas (`GitHubError`, `OllamaError`, `TestFailure`, `LimitExceeded`, `ReviewerGitHubError`).
* **Relatórios Automáticos de Evidências (`eval/`):**
  * Ao final de cada execução (sucesso ou falha), o sistema grava e atualiza automaticamente:
    * `eval/relatorio_execucoes.csv`: planilha estruturada compatível com Excel.
    * `eval/RELATORIO_METRICAS.md`: relatório consolidado com taxa de resolução (`%`), consumo médio de tokens e tempo médio por *issue*.

---

## Estrutura do Repositório

```text
Grupo7/
├── backend/
│   ├── agents/
│   │   ├── graph.py              # Definição do grafo LangGraph e transições condicionais
│   │   ├── nodes.py              # Lógica dos 4 agentes e gerador automático de relatórios
│   │   └── state.py              # Tipagem do estado compartilhado (AgentState)
│   ├── metrics/
│   │   └── error_classifier.py   # Classificação e diagnóstico amigável de falhas
│   ├── tools/
│   │   ├── github_client.py      # Integração com GitHub API (issues, branches, commits e PRs)
│   │   └── workspace_tools.py    # Leitura e manipulação segura de arquivos no workspace
│   ├── main.py                   # API FastAPI, endpoints /run, /resume, /metrics e /stream
│   └── requirements.txt          # Dependências Python do backend
├── frontend/
│   └── index.html                # Interface web do painel de controle e monitoramento
├── eval/
│   ├── relatorio_execucoes.csv   # Registro tabular automático das execuções
│   ├── RELATORIO_METRICAS.md     # Resumo consolidado de métricas para avaliação
│   └── run_eval.py               # Script auxiliar de avaliação
├── resolucoes/                   # Documentação das soluções geradas por issue/PR
├── src/                          # Código-fonte da aplicação alvo e testes
├── .env.example                  # Modelo de variáveis de ambiente necessárias
├── .gitignore                    # Proteção contra versionamento de segredos (.env) e cache
├── Dockerfile                    # Imagem Python 3.11 com Git e dependências do orquestrador
└── docker-compose.yml            # Orquestração do container e volumes locais
```

---

## Como Executar Localmente

### Pré-requisitos
* **Docker Desktop** instalado e em execução.
* **Ollama** instalado localmente com o modelo `llama3.2` baixado (`ollama pull llama3.2`).
* **Personal Access Token (PAT)** do GitHub com permissão de leitura e escrita em *Contents*, *Issues* e *Pull requests*.

### Passo a Passo
1. Na raiz do projeto, crie um arquivo `.env` baseado no `.env.example` contendo suas credenciais locais (este arquivo é ignorado pelo Git):
   ```env
   GITHUB_TOKEN=seu_token_do_github_aqui
   GITHUB_REPO=danielxissantana-sketch/Grupo7
   OLLAMA_BASE_URL=[http://host.docker.internal:11434](http://host.docker.internal:11434)
   OLLAMA_MODEL=llama3.2
   MAX_STEPS=30
   MAX_TOKENS=150000
   ```
2. No terminal (PowerShell), dentro da pasta do repositório, inicie o container:
   ```bash
   docker-compose up --build
   ```
3. Acesse o painel de controle no navegador em **`http://localhost:8000`**, informe o número da *issue* aberta no GitHub, defina a branch base (`main`) e clique em **Iniciar Execução**.
4. Após a criação do *Pull Request*, revise e confirme o *merge* no GitHub e consulte os indicadores atualizados em `eval/RELATORIO_METRICAS.md`.