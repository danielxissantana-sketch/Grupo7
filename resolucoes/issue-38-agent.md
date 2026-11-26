Automatizado via Orquestrador.

Plano:
**Análise da Issue**
A issue apresenta um problema de validação de formato de CPF (Cadastro de Pessoas Físicas) no Brasil. A função `validar_cpf_formato(cpf)` deve verificar se o CPF fornecido é válido de acordo com a regra estabelecida pela Receita Federal do Brasil.
**Regra de Negócio**
A regra de negócio para validação de CPF é a seguinte:
* O CPF deve ter exatamente 11 dígitos.
* Os 9 primeiros dígitos devem ser numéricos.
* O último dígito deve ser calculado com base nos 9 primeiros dígitos.
* O CPF pode conter pontos e traços (-) como separadores, mas eles não são necessários para a validação.
**Perguntas ao Operador**
Antes de criar o plano de solução, gostaria de saber:
1. Qual é a fonte de dados para o CPF? (Ex: banco de dados, API, etc.)
2. Existem regras adicionais para validação de CPF, como a necessidade de verificar se o CPF é válido para um determinado estado ou região?
3. Qual é o comportamento para CPFs inválidos? (Ex: retornar um erro, ignorar, etc.)
4. Existem requisitos específicos para a formatação do CPF, como a necessidade de usar pontos e traços (-) como separadores?
**Plano de Solução**
Se todas as regras estiverem claras, o plano de solução é o seguinte:
1. Crie uma função `validar_cpf_formato(cpf)` que receba um CPF como parâmetro.
2. Remova todos os caracteres não numéricos do CPF (pontos e traços -).
3. Verifique se o CPF tem exatamente 11 dígitos.
4. Verifique se os 9 primeiros dígitos são numéricos.
5. Se os passos 3 e 4 forem verdadeiros, calcule o último dígito com base nos 9 primeiros dígitos.
6. Verifique se o último dígito calculado é igual ao último dígito do CPF original.
7. Se os passos 5 e 6 forem verdadeiros, retorne `True` indicando que o CPF é válido. Caso contrário, retorne `False`.
**Código de Exemplo**
```python
def validar_cpf_formato(cpf):
# Remova todos os caracteres não numéricos do CPF
cpf_numerico = ''.join(c para c in cpf if c.isdigit())
# Verifique se o CPF tem exatamente 11 dígitos
if len(cpf_numerico) != 11:
return False
# Verifique se os 9 primeiros dígitos são numéricos
if not cpf_numerico[:9].isdigit():
return False
# Calcule o último dígito com base nos 9 primeiros dígitos
dígito_calculado = 0
for i in range(9):
dígito_calculado += int(cpf_numerico[i]) * (10 - i)
# Verifique se o último dígito calculado é igual ao último dígito do CPF original
if dígito_calculado != int(cpf_numerico[9]):
return False
return True
```
Espero que isso ajude! Se tiver alguma dúvida ou precisar de mais informações, não hesite em perguntar.