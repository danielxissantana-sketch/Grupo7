Automatizado via Orquestrador.

Plano:
**Análise da Issue**
A issue apresentada é uma solicitação para criar uma função `calcular_parcela_sem_juros` que permita calcular o valor de cada parcela de um empréstimo, considerando o valor total do empréstimo e o número de parcelas. No entanto, há algumas informações críticas ausentes, como o valor mínimo da parcela, a regra de arredondamento e o comportamento quando o valor for menor que o mínimo.
**Perguntas para Esclarecimento**
Para criar uma solução eficaz, é necessário obter esclarecimentos sobre as seguintes informações:
1. **Valor mínimo da parcela**: Qual é o valor mínimo que uma parcela pode ter? Isso influencia diretamente no cálculo do valor de cada parcela.
2. **Regra de arredondamento**: Quais são as regras para arredondar o valor de cada parcela? Por exemplo, se o valor for 10,99, será arredondado para 11 ou 10?
3. **Comportamento com valores menores que o mínimo**: O que acontece quando o valor de uma parcela for menor que o valor mínimo? Será que o valor será ajustado para atender ao valor mínimo ou será tratado como um valor inválido?
**Plano de Ação**
1. **Definir o valor mínimo da parcela**: Obtenha a informação sobre o valor mínimo da parcela e defina uma variável para armazenar esse valor.
2. **Definir a regra de arredondamento**: Obtenha a informação sobre a regra de arredondamento e defina uma função para aplicar essa regra.
3. **Definir o comportamento com valores menores que o mínimo**: Obtenha a informação sobre o comportamento com valores menores que o mínimo e defina uma lógica para lidar com esses casos.
4. **Criar a função `calcular_parcela_sem_juros`**: Utilize as informações coletadas para criar a função `calcular_parcela_sem_juros` que calcule o valor de cada parcela considerando o valor total do empréstimo, o número de parcelas e as regras definidas.
**Exemplo de Implementação**
```javascript
function calcularParcelaSemJuros(total, numParcelas, valorMinimo, regraArredondamento) {
// Verificar se o valor mínimo é válido
if (valorMinimo <= 0) {
throw new Error('Valor mínimo inválido');
}
// Verificar se o número de parcelas é válido
if (numParcelas < 1 || numParcelas > 3) {
throw new Error('Número de parcelas inválido');
}
// Calcular o valor de cada parcela
const parcelas = [];
for (let i = 1; i <= numParcelas; i++) {
const valorParcela = total / numParcelas;
// Aplicar a regra de arredondamento
const valorParcelaArredondado = regraArredondamento(valorParcela);
// Verificar se o valor parcela é menor que o valor mínimo
if (valorParcelaArredondado < valorMinimo) {
// Ajustar o valor parcela para atender ao valor mínimo
valorParcelaArredondado = valorMinimo;
}
parcelas.push(valorParcelaArredondado);
}
return parcelas;
}
// Exemplo de uso
const total = 1000;
const numParcelas = 2;
const valorMinimo = 50;
const regraArredondamento = (valor) => Math.round(valor * 100) / 100;
const parcelas = calcularParcelaSemJuros(total, numParcelas, valorMinimo, regraArredondamento);
console.log(parcelas);
```
Essa é uma implementação básica que pode ser ajustada e personalizada de acordo com as necessidades específicas do problema.