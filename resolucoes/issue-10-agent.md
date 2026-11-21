Automatizado via Orquestrador.

Plano:
**Análise da Issue**
A issue apresentada é relacionada à criação de uma função `calcular_total_com_juros(valor, parcelas)` que calcula o valor total de uma compra parcelada com juros simples. A função deve aplicar 2% de juros simples ao mês para compras parceladas de 4 a 12 vezes.
**Critérios de Aceitação**
Para atender aos critérios de aceitação, a função `calcular_total_com_juros(valor, parcelas)` deve ser capaz de calcular o valor total com juros simples para as seguintes combinações de entrada:
1. `valor = 100.0` e `parcelas = 5`
2. `valor = 100.0` e `parcelas = 10`
**Plano de Ação**
1. **Defina a função `calcular_total_com_juros(valor, parcelas)`**:
* A função deve receber dois parâmetros: `valor` e `parcelas`.
* A função deve calcular o valor total com juros simples usando a fórmula `valor * (1 + 0.02 * parcelas)`.
* A função deve retornar o valor total com juros simples.
2. **Verifique os critérios de aceitação**:
* Teste a função com os critérios de aceitação fornecidos (valor = 100.0 e parcelas = 5, valor = 100.0 e parcelas = 10).
* Verifique se a função retorna os valores esperados para os critérios de aceitação.
3. **Tratamento de casos especiais**:
* Verifique se a função deve tratar casos especiais, como:
+ `parcelas < 4`: deve retornar sem juros ou aplicar outra taxa?
+ `parcelas > 12`: deve retornar sem juros ou bloquear com erro?
* Se necessário, adicione lógica para tratar esses casos especiais.
**Código de Implementação**
```python
def calcular_total_com_juros(valor, parcelas):
if parcelas < 4 or parcelas > 12:
raise ValueError("Parcelas inválidas. Por favor, informe entre 4 e 12 parcelas.")
juros = valor * 0.02 * parcelas
total = valor + juros
return total
```
**Testes**
```python
import pytest
def test_calcular_total_com_juros():
valor = 100.0
parcelas = 5
assert calcular_total_com_juros(valor, parcelas) == 110.0
def test_calcular_total_com_juros():
valor = 100.0
parcelas = 10
assert calcular_total_com_juros(valor, parcelas) == 120.0
```
**Observação**
Se a equipe comercial não fornecer informações claras sobre como o sistema deve tratar casos especiais, é necessário solicitar esclarecimentos antes de prosseguir com a implementação.