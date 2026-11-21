Automatizado via Orquestrador.

Plano:
**Análise da Issue**
A issue apresentada é uma função `calcular_desconto_pix(valor, metodo)` que deve aplicar um desconto de 10% quando o método de pagamento for "PIX". A função deve funcionar tanto para "PIX" em maiúsculo quanto para "pix" em minúsculo.
**Critérios de Aceitação**
Para atender aos critérios de aceitação, precisamos garantir que a função seja testada com os seguintes cenários:
1. `valor = 100.0` e `metodo = "PIX"` (ou `"PIX"` em maiúsculo)
2. `valor = 100.0` e `metodo = "CARTAO"`
3. `valor = 100.0` e `metodo = "pix"` (ou `"PIX"` em minúsculo)
**Plano de Ação**
Aqui está um plano de ação para resolver a issue:
1. **Defina a função `calcular_desconto_pix(valor, metodo)`**:
```python
def calcular_desconto_pix(valor, metodo):
# Verifique se o método é "PIX" (ou "PIX" em maiúsculo)
if metodo.lower() == "pix":
# Aplicar desconto de 10%
desconto = valor * 0.10
valor_desconto = valor - desconto
return valor_desconto
# Se o método for "CARTAO", não aplicar desconto
elif metodo.upper() == "CARTAO":
return valor
# Se o método for qualquer outro valor, retornar erro
else:
return "Erro: Método inválido"
```
2. **Teste a função com os critérios de aceitação**:
```python
import pytest
def test_calcular_desconto_pix():
# Teste 1: Valor = 100.0 e método = "PIX" (ou "PIX" em maiúsculo)
assert calcular_desconto_pix(100.0, "PIX") == 90.0
assert calcular_desconto_pix(100.0, "PIX") == 90.0  # Teste com "PIX" em maiúsculo
# Teste 2: Valor = 100.0 e método = "CARTAO"
assert calcular_desconto_pix(100.0, "CARTAO") == 100.0
# Teste 3: Valor = 100.0 e método = "pix" (ou "PIX" em maiúsculo)
assert calcular_desconto_pix(100.0, "pix") == 90.0
assert calcular_desconto_pix(100.0, "PIX") == 90.0  # Teste com "PIX" em maiúsculo
def test_calcular_desconto_pix_error():
# Teste: Valor = 100.0 e método = qualquer outro valor
assert calcular_desconto_pix(100.0, "OUTRO") == "Erro: Método inválido"
```
3. **Executar os testes**:
```python
pytest test_calcular_desconto_pix.py
```
Com esses passos, podemos garantir que a função `calcular_desconto_pix(valor, metodo)` seja testada com os critérios de aceitação e que ela funcione corretamente para os diferentes cenários.