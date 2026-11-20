
CABEÇALHO

Tema 7 Grupo7) — Faça ticket ao pull request: agente de engenharia de software
Projeto da disciplina Projetos de IA na Programação .

Sistema multiagente que lê um problema, planeja a solução, escreve código e testes, executa a integração contínua e abre um pull request

Integrantes e papéis:
Daniel Cosme de Santana — Backend e Infraestrutura
Giovana de Jesus Oliveira — IA e Avaliação; co-responsável por Dados e Qualidade
Rodrigo Forcinito Cruz — Produto e Interface; co-responsável por Dados e Qualidade

Identificação do curso:
Daniel Cosme de Santana - RA 2410004 - Projeto Integrado - EAD_PROINT_100.DD-BD-PI-10-74.2026.74
Rodrigo Forcinito Cruz - RA 2522857 - Projeto Integrado - EAD_PROINT_100.DD-BD-PI-10-74.2026.74
Giovana de Jesus Oliveira - RA 2402906 - Projeto Integrado - EAD_PROINT_100.DD-ADS-PI-10-74.2026.74

Descrição:
Orquestrador Multi-Agente (LangGraph + Ollama) — Projeto Grupo 7

Este repositório contém a implementação de um sistema autônomo de orquestração multi-agente construído com LangGraph e modelos de linguagem locais via Ollama (llama3.2), integrado à API do GitHub para automação completa do ciclo de desenvolvimento: leitura de Issues, planejamento com supervisão humana, geração de solução, validação e abertura automática de Pull Requests.

Projeto desenvolvido para avaliação acadêmica (Tema 7: Do ticket ao pull request — Agente de Engenharia de Software).

🏗️ Arquitetura do Sistema

O fluxo de trabalho é coordenado por um grafo de estados (LangGraph) composto por quatro agentes especializados:

Planejador (planner_node): Consulta a Issue diretamente via API do GitHub, avalia se há ambiguidades nos requisitos e aciona o mecanismo de Human-in-the-loop (pausando a execução e solicitando esclarecimento ao operador no painel web) antes de estruturar o plano técnico.

Programador (programmer_node): Inspeciona os arquivos do workspace isolado no container Docker e elabora a solução técnica baseada no plano aprovado.

Testador (tester_node): Executa a validação lógica e verifica a conformidade da entrega com os critérios da Issue.

Revisor & PR (reviewer_node): Consolida a revisão técnica e automatiza todo o fluxo Git no GitHub:

Cria automaticamente uma branch isolada para a tarefa (issue-{numero}-agent) a partir da branch base (main).

Registra um commit real com o relatório e plano de resolução em resolucoes/issue-{numero}-agent.md.

Abre o Pull Request oficial vinculando a branch da issue à branch main e retorna o link direto no painel.

🛠️ Stack Tecnológica e Governança

Orquestração: Python 3.11 + LangGraph (MemorySaver para persistência de estado e retomada após intervenção humana)

LLM Local: Ollama (llama3.2)

Infraestrutura: Docker & Docker Compose (ambiente isolado)

Integração Git: PyGithub / GitHub REST API

Interface & Telemetria: FastAPI + Server-Sent Events (SSE) + Tailwind CSS

Controle de Consumo e Segurança: Limites configuráveis de passos (MAX_STEPS) e tokens (MAX_TOKENS) por execução, além de classificação automática de erros em tempo real no painel.

🚀 Como Configurar e Executar

1. Pré-requisitos

Docker Desktop instalado e em execução.

Ollama instalado localmente com o modelo llama3.2 disponível:

ollama run llama3.2


Token de Acesso Pessoal do GitHub (Fine-Grained PAT): Gere um token com acesso ao repositório do projeto contendo as seguintes permissões:

Contents (Código): Leitura e gravação (Read and write) — necessário para criar branches e commits automatizados.

Pull requests: Leitura e gravação (Read and write) — necessário para abertura automática do PR.

Issues e Metadata: Leitura (Read-only).

2. Configuração de Variáveis de Ambiente (.env)

Na raiz do projeto, crie um arquivo .env com suas credenciais locais:

GITHUB_TOKEN=github_pat_seu_token_aqui
GITHUB_REPO=danielxissantana-sketch/Grupo7
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2
MAX_STEPS=30
MAX_TOKENS=150000


(O arquivo .env está protegido no .gitignore para evitar exposição de credenciais).

3. Inicialização via Docker

No terminal, dentro da pasta raiz do repositório, execute:

docker-compose down
docker-compose up --build


4. Operação pelo Painel Web

Acesse http://localhost:8000 no navegador, informe o número da Issue (ex: 1), defina a branch base (main) e clique em "Iniciar Execução". Caso o agente Planejador solicite esclarecimentos, responda diretamente pelo painel para retomar o fluxo até a geração do Pull Request.

📊 Rastreabilidade e Evidências Acadêmicas

Cada execução concluída gera registros auditáveis no GitHub:

Histórico de Execução: Contagem de passos, consumo de tokens e linha do tempo no painel.

Branch Isolada: Criação automática da branch issue-{numero}-agent.

Commit Automatizado: Registro da resolução técnica na pasta resolucoes/.

Pull Request Oficial: PR aberto e pronto para revisão/merge na branch principal.