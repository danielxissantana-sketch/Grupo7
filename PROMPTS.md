# PROMPTS.md — Registro de uso de IA

Aqui a gente registra as conversas com IA que influenciaram o projeto: o que pedimos,
o que ela respondeu e o que a gente aceitou, corrigiu ou jogou fora.

## Integrante

* **Daniel Cosme de Santana** - RA 2410004 - Projeto integrador - EAD_PROINT_100.DD-BD-PI-10-74.2026.74 (Backend e Infraestrutura)

# Registro de Uso de IA na Engenharia do Projeto (`PROMPTS.md`)

Abaixo estão documentadas 10 interações principais utilizadas na concepção, desenvolvimento, depuração e operação do Orquestrador Multi-Agente (Tema 7).

---

### Interação 1 — Definição da Arquitetura Multi-Agente com LangGraph
- **Contexto:** Estruturação inicial do fluxo entre os 4 agentes especializados exigidos no Tema 7.
- **Prompt utilizado:** *"Crie a estrutura de estados (`AgentState`) e o grafo em LangGraph para um orquestrador de engenharia de software com 4 nós sequenciais: Planejador, Programador, Testador e Revisor, utilizando Ollama local."*
- **Resultado e ajuste:** Gerou `state.py` e `graph.py`; adicionamos arestas condicionais para interromper o grafo em caso de erro ou pedido de esclarecimento.

### Interação 2 — Regra de Pausa *Human-in-the-Loop* no Planejador
- **Contexto:** Atender ao desafio central do trabalho (parar e pedir ajuda humana diante de requisitos ambíguos).
- **Prompt utilizado:** *"Ajuste o prompt do `planner_node` para que, sempre que faltarem regras de negócio críticas na issue do GitHub, ele responda iniciando com `PRECISA_ESCLARECIMENTO:` e pause a execução até receber a resposta do operador."*
- **Resultado e ajuste:** Implementado no `nodes.py` com detecção de palavras-chave em português e endpoint `/resume/{issue_number}` no FastAPI.

### Interação 3 — Controle de Orçamento (`Max Passos` e `Max Tokens`)
- **Contexto:** Evitar loops infinitos e estouro de recursos computacionais.
- **Prompt utilizado:** *"Implemente uma função `check_limits(state)` verificada antes de cada agente que bloqueie a execução e registre `LimitExceeded` caso `steps_count >= max_steps` ou `tokens_used >= max_tokens`."*
- **Resultado e ajuste:** Validado com travas de segurança no início de cada nó para evitar gravações duplicadas de erro.

### Interação 4 — Prompt do Agente Programador
- **Contexto:** Geração do plano de alteração e análise dos arquivos do workspace isolado.
- **Prompt utilizado:** *"Configure o `programmer_node` para receber o plano aprovado pelo Planejador, listar os arquivos disponíveis em `/workspace` e gerar as notas técnicas de implementação respeitando os critérios de aceitação."*
- **Resultado e ajuste:** Integrado ao `WorkspaceTools` para leitura segura do diretório montado no Docker.

### Interação 5 — Validação Automatizada com `pytest` (Agente Testador)
- **Contexto:** Garantir que nenhum Pull Request seja aberto sem passar pela suíte de testes.
- **Prompt utilizado:** *"Crie o `tester_node` executando `subprocess.run(['pytest', '/workspace'])`, capturando o código de retorno e classificando falhas de teste como `TestFailure` no relatório."*
- **Resultado e ajuste:** Configurado para bloquear a abertura do PR quando `pytest` retorna falha de asserção.

### Interação 6 — Prompt do Agente Revisor e Integração com GitHub API
- **Contexto:** Criação automática de branch e abertura de Pull Request após aprovação nos testes.
- **Prompt utilizado:** *"Implemente o `reviewer_node` para consolidar o plano técnico, criar a branch `issue-{numero}-agent` e abrir o Pull Request via `GitHubClient` referenciando `Fix #{numero}`."*
- **Resultado e ajuste:** Automatiza o fechamento da issue assim que um colega aprova o merge no GitHub.

### Interação 7 — Painel Web de Monitoramento e Intervenção em Tempo Real
- **Contexto:** Interface visual para configurar limites, acompanhar os agentes e responder às pausas humanas.
- **Prompt utilizado:** *"Crie uma interface web em HTML/CSS/JS servida pelo FastAPI que exiba o andamento dos 4 agentes em tempo real via Server-Sent Events (`/stream`), caixa amarela de esclarecimento e caixa vermelha de diagnóstico de erro."*
- **Resultado e ajuste:** Implementado em `frontend/index.html` com atualização dinâmica de tokens e tempo.

### Interação 8 — Containerização Reproduzível com Docker Compose
- **Contexto:** Garantir que o projeto suba com um único comando (`docker-compose up`) a custo zero.
- **Prompt utilizado:** *"Escreva o `Dockerfile` e o `docker-compose.yml` conectando o backend FastAPI na porta 8000 ao Ollama rodando no host (`host.docker.internal:11434`) com volumes mapeados para `backend`, `frontend`, `workspace` e `eval`."*
- **Resultado e ajuste:** Permite edição em tempo real e persistência dos relatórios CSV/Markdown no host.

### Interação 9 — Automação das Métricas Experimentais (Rubricas 2 e 3)
- **Contexto:** Registrar automaticamente taxa de resolução, tokens, tempo e categorias de falha.
- **Prompt utilizado:** *"Adicione uma função `save_execution_report` que grave cada execução em `eval/relatorio_execucoes.csv` e consolide as médias e porcentagens em `eval/RELATORIO_METRICAS.md`."*
- **Resultado e ajuste:** Complementado pelo script autônomo `eval/run_eval.py` para reexecução via terminal.

### Interação 10 — Geração de Issues de Teste com Critérios de Aceitação
- **Contexto:** Criar uma base padronizada de 30 issues de e-commerce para avaliação experimental.
- **Prompt utilizado:** *"Gere 30 issues enxutas de regras de negócio em Python (cálculo de frete, descontos, cupons, validação de CPF/CEP e fechamento de carrinho) contendo título, descrição e critérios de aceitação objetivos para o `pytest`."*
- **Resultado e ajuste:** Executadas no orquestrador para compor a amostra experimental e a análise de falhas.


## Integrantes

* **Giovana de Jesus Oliveira** - RA 2402906 - Projeto integrador - EAD_PROINT_100.DD-ADS-PI-10-74.2026.74 (IA e Avaliação; co-responsável por Dados e Qualidade)
* **Rodrigo Forcinito Cruz** - RA 2522857 - Projeto integrador - EAD_PROINT_100.DD-BD-PI-10-74.2026.74 (Produto e Interface; co-responsável por Dados e Qualidade)


Ferramentas usadas: Copilot e Perplexity.

---

## 1. Qual pergunta o trabalho responde

**Pedimos:** como transformar o desafio do Tema 7 em uma pergunta que dá para comparar
com algo?

**Ela respondeu:** comparar o grafo multiagente com limites contra uma chamada única ao
mesmo modelo, medindo quantas issues resolve e quanto custa.

**Decisão:** aceitamos com ajuste.

**Por quê:** a comparação só vale se o baseline usar o mesmo modelo, sem grafo e sem
limites. A gente deixou isso escrito.

## 2. Modelo de 3B ou 7B

**Pedimos:** temos notebook sem placa de vídeo. Vale usar o 7B?

**Ela respondeu:** sim, o 7B é melhor.

**Decisão:** corrigimos.

**Por quê:** ela olhou só a qualidade e esqueceu o tempo. Uma issue passa de 15 chamadas.
Em CPU, o 7B gera 2 a 5 tokens por segundo, e as 20 execuções não caberiam no prazo.
Ficamos com o 3B.

## 3. Função base do projeto

**Pedimos:** uma função de frete em Python que devolva 1500 centavos.

**Ela respondeu:** função simples, sem dependência.

**Decisão:** aceitamos.

**Por quê:** é uma regra só, fácil de testar, e serve de ponto de partida.

## 4. O erro do frete grátis

**Pedimos:** frete grátis a partir de R$ 100.

**Ela respondeu:** usou "maior que 10000".

**Decisão:** corrigimos.

**Por quê:** "a partir de" inclui os R$ 100. O certo é "maior ou igual". O teste no valor
exato de 10000 pegou o erro. Guardamos esse caso para a análise de falhas.

## 5. Testes escritos antes de rodar

**Pedimos:** testes para abaixo, no limite, acima e valor inválido.

**Ela respondeu:** quatro testes com assert.

**Decisão:** aceitamos.

**Por quê:** os critérios existiam antes dos agentes rodarem. Isso deixa a avaliação
honesta.

## 6. O que guardar de cada execução

**Pedimos:** quais informações precisamos salvar de cada issue.

**Ela respondeu:** issue, plano, diff, resultado dos testes, parecer, tentativas, passos
e tokens.

**Decisão:** aceitamos com ajuste.

**Por quê:** faltava o motivo da parada. Sem ele não dá para provar que o sistema parou
sozinho ao bater no limite, que é justamente o que o tema cobra.

## 7. Contar tokens direito

**Pedimos:** parar a execução quando o orçamento de tokens acabar.

**Ela respondeu:** comparou só os tokens de saída.

**Decisão:** corrigimos.

**Por quê:** a entrada também gasta, porque o prompt com o arquivo inteiro é reenviado a
cada tentativa. Passamos a reservar entrada mais saída antes de chamar e a corrigir pelo
número real que o Ollama devolve.

## 8. Como saber que travou

**Pedimos:** como detectar que o agente está repetindo sem sair do lugar.

**Ela respondeu:** comparar o hash do diff.

**Decisão:** descartamos.

**Por quê:** se o modelo só muda um espaço, o hash muda e a gente não percebe a repetição.
Trocamos por: mesma mensagem de erro e mesmos testes falhando.

## 9. Rodar código da IA sem risco

**Pedimos:** como rodar em Docker o código que a IA escreve, com o mínimo de acesso.

**Ela respondeu:** um contêiner com a pasta montada.

**Decisão:** aceitamos com ajuste.

**Por quê:** faltava o principal. Colocamos sem rede, disco somente leitura, sem
privilégios, com limite de memória e CPU, e os testes de aceitação travados para escrita.

## 10. Deixar a verificação automática verde

**Pedimos:** como fazer a CI ficar verde antes do sistema completo existir?

**Ela respondeu:** testar o orquestrador, que depende do Ollama e do GitHub.

**Decisão:** corrigimos.

**Por quê:** teste que depende de serviço externo falha na CI. Escrevemos testes da parte
de limites, que roda sem nada externo. A bolinha ficou verde desde o começo.

## 11. Normas ABNT e referências

**Pedimos:** quais são as versões atuais das normas e se dá para melhorar as referências.

**Ela respondeu:** citou NBR 14724 de 2011 e sugeriu blogs para reforçar.

**Decisão:** corrigimos os dois.

**Por quê:** as versões atuais são NBR 14724:2024 e NBR 6023:2025. E blog não vale como
fonte científica. Trocamos por artigos brasileiros publicados na SBC em 2025, além das
documentações oficiais.

## 12. A proposta passou de duas páginas

**Pedimos:** como reduzir a proposta sem perder conteúdo.

**Ela respondeu:** diminuir a fonte do texto.

**Decisão:** descartamos.

**Por quê:** a norma exige tamanho 12 no corpo. Resolvemos trocando a fonte para Times New
Roman, deixando tabelas e referências em 10 e encurtando o texto, sem cortar nada
obrigatório.

---

## O que a IA errou (e o que aprendemos)

- **Olhou só a qualidade e esqueceu o nosso computador:** recomendou o 7B sem pensar no
  tempo de execução.
- **Leu ao pé da letra:** usou "maior que" onde era "a partir de".
- **Solução preguiçosa para CI vermelha:** mandou apagar a verificação em vez de corrigir
  o código.
- **Normas desatualizadas:** citou versões que já foram substituídas.
- **Fonte fraca:** sugeriu blog onde precisávamos de artigo científico.
- **Não contou quantos somos:** propôs 20 funcionalidades diferentes para três pessoas em
  seis semanas.enhum número de token, tempo ou taxa de acerto foi colocado aqui, porque o sistema ainda
não rodou. Inventar número é falta grave.
