# Orquestrador Multi-Agente (LangGraph + Ollama) - Projeto Grupo 7

Rodrigo Forcinito Cruz — RA
Giovana de Jesus Oliveira — RA
Daniel Cosme de Santana — RA 2410004

Este repositório contém a implementação de um sistema de orquestração multi-agente utilizando **LangGraph** e modelos de linguagem locais via **Ollama** (`llama3.2`), integrado ao ecossistema do GitHub para automação de tarefas em Issues e criação de Pull Requests.

O projeto faz parte de um trabalho acadêmico em grupo focado em Engenharia de Software e Inteligência Artificial Aplicada.

---

## 🏗️ Arquitetura do Sistema

O sistema é dividido em quatro agentes autônomos sequenciais:
1. **Planejador:** Analisa a Issue designada do GitHub, decompõe o problema e formula um plano técnico de implementação (com suporte a *Human-in-the-loop* para esclarecimentos).
2. **Programador:** Escreve ou modifica o código-fonte necessário para atender aos requisitos da Issue no workspace local.
3. **Testador:** Executa validações e verifica a integridade das alterações propostas.
4. **Revisor & PR:** Realiza a revisão final do código e automatiza a abertura do Pull Request correspondente na branch de trabalho do repositório.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11** (Backend e LangGraph)
- **Ollama** (Modelo local `llama3.2`)
- **Docker & Docker Compose** (Isolamento e execução do ambiente)
- **GitHub API** (Leitura de Issues e abertura de Pull Requests)
- **Tailwind CSS** (Interface web em tempo real para monitoramento)

---

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e rodar o orquestrador no seu ambiente de desenvolvimento:

### 1. Pré-requisitos
- **Docker Desktop** instalado e rodando.
- **Ollama** instalado localmente com o modelo baixado:
  ```bash
  ollama run llama3.2
  ```

### 2. Configuração do Ambiente (`.env`)
Na raiz do projeto, crie um arquivo chamado `.env` contendo as suas credenciais de integração:
```env
GITHUB_TOKEN=seu_token_pessoal_do_github_com_escopo_repo
GITHUB_REPO=nome_da_organizacao_ou_usuario/Grupo7
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2
MAX_STEPS=30
MAX_TOKENS=150000
```
*(Nota: O arquivo `.env` contém credenciais sensíveis e está listado no `.gitignore` para não ser enviado publicamente).*

### 3. Subindo o Ambiente com Docker
Abra o terminal na pasta raiz do projeto e execute os comandos:
```bash
docker-compose down
docker-compose up --build
```

### 4. Acessando o Painel Web
Com o container em execução, abra o seu navegador e acesse:
```text
http://localhost:8000
```
No painel, insira o número da Issue do GitHub que deseja automatizar (ex: `#1`), confirme a branch base de trabalho e clique em **"Iniciar Execução"**.

---

## 📊 Evidências e Avaliação Acadêmica
Todas as interações realizadas pelos agentes de IA geram rastreabilidade direta no GitHub do grupo, incluindo:
- Histórico de comentários e alinhamentos nas **Issues**.
- Commits organizados na branch específica do desenvolvedor.
- **Pull Requests** automatizados contendo o relatório de modificações e validações do sistema.