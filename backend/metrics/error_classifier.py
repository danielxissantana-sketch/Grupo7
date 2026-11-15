def classify_and_explain_error(error_category: str, raw_message: str) -> dict:
    category_mapping = {
        "GitHubError": {
            "title": "Erro de Integração com o GitHub",
            "explanation": "O orquestrador encontrou falhas ao interagir com a API do GitHub.",
            "remediation": "Verifique se o token do GitHub (GITHUB_TOKEN) está válido e se o repositório configurado está correto."
        },
        "OllamaError": {
            "title": "Erro de Comunicação com o Ollama / LLM",
            "explanation": "O modelo local no Ollama falhou ao responder ou recusou/timeout durante a geração.",
            "remediation": "Certifique-se de que o Ollama está rodando e o modelo configurado está disponível."
        },
        "WorkspaceError": {
            "title": "Erro no Workspace Local",
            "explanation": "Falha ao ler ou gravar arquivos no diretório de trabalho do projeto.",
            "remediation": "Verifique as permissões do diretório de workspace mapeado no Docker."
        },
        "ReviewerGitHubError": {
            "title": "Erro ao Criar Pull Request",
            "explanation": "A abertura automática do Pull Request falhou.",
            "remediation": "Pode haver conflito de branch ou permissões insuficientes no token."
        },
        "LimitExceeded": {
            "title": "Limite de Consumo Excedido",
            "explanation": "A execução atingiu o teto máximo parametrizado de passos ou tokens.",
            "remediation": "Aumente os limites de passos ou tokens na configuração."
        }
    }
    details = category_mapping.get(error_category, {
        "title": "Erro Desconhecido",
        "explanation": f"Ocorreu uma exceção inesperada: {raw_message}",
        "remediation": "Inspecione os logs do container Docker."
    })
    return {
        "category": error_category,
        "title": details["title"],
        "explanation": details["explanation"],
        "remediation": details["remediation"],
        "raw_message": raw_message
    }
