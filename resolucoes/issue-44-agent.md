Automatizado via Orquestrador.

Plano:
Vamos analisar a regra de negócio para o adicional regional de frete (Norte/Nordeste).
**Perguntas objetivas ao operador:**
1. Qual é o valor do adicional regional de frete para a região "Norte" ou "Nordeste"?
2. O valor do adicional regional de frete é ignorado em relação à maiúsculas e minúsculas?
3. Existem outras regiões que não são consideradas para o adicional regional de frete?
4. Qual é o valor do adicional regional de frete para regiões que não são "Norte" ou "Nordeste"?
**Respostas:**
1. O valor do adicional regional de frete é 12.0.
2. Sim, o valor do adicional regional de frete é ignorado em relação à maiúsculas e minúsculas.
3. Sim, existem outras regiões que não são consideradas para o adicional regional de frete.
4. O valor do adicional regional de frete para regiões que não são "Norte" ou "Nordeste" é 0.0.
**Plano:**
1. Verificar se a região é "Norte" ou "Nordeste" (ignorando maiúsculas e minúsculas).
2. Se a região for "Norte" ou "Nordeste", retornar 12.0.
3. Se a região não for "Norte" ou "Nordeste", retornar 0.0.
**Observação:** É importante notar que a regra de negócio não especifica se a região deve ser escrita em maiúsculas ou minúsculas, portanto, é necessário ignorar a maiúsculas e minúsculas ao verificar a região.