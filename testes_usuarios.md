# Testes com usuários

Objetivo: verificar se as pessoas entendem e acham útil as orientações do assistente de Energia (banho quente). Os participantes são identificados apenas por código (P1 a P5), sem nomes ou outros dados pessoais.

## Situações testadas
Cada participante usou o assistente (`python assistente.py`) com os valores sugeridos (família de 4 pessoas, banho de 10 min, chuveiro de 5.500 W, tarifa Enel SP sem impostos) e realizou três tarefas:
1. Descobrir quanto custa por mês o banho da família (esperado: cerca de R$ 86,83, opção 1). O tempo foi cronometrado.
2. Dizer qual alternativa economiza sem investimento (esperado: banho mais curto, opção 4).
3. Dizer se o assistente garante a economia (esperado: não, são estimativas).

## Registro dos testes
| Participante | Perfil | Tarefa 1: acertou? tempo | Tarefa 2: acertou? | Tarefa 3: acertou? | Facilidade (1 a 5) | O que não ficou claro | O que mudaria |
|---|---|---|---|---|---|---|---|
| P1 | Jovem adulto, 19 anos, familiaridade intermediária com tecnologia | Sim, 35 s | Sim | Sim | 5 | A diferença entre kWh e reais | Colocaria uma explicação simples sobre o consumo de energia |
| P2 | Adulto, 35 anos, usa computador e celular diariamente | Sim, 48 s | Sim | Sim | 4 | Como o programa calcula o investimento do aquecedor solar | Adicionaria uma comparação visual entre as alternativas |
| P3 | Adulto, 52 anos, pouca familiaridade com programas de computador | Sim, 85 s | Sim | Sim | 3 | Algumas informações e termos técnicos | Deixaria as opções mais simples e as instruções mais explicativas |
| P4 | Estudante universitário, 21 anos, familiaridade avançada com tecnologia | Sim, 25 s | Sim | Sim | 5 | A origem de alguns valores usados nos cálculos | Criaria gráficos para facilitar a visualização dos resultados |
| P5 | Adulto, 43 anos, familiaridade básica com tecnologia | Sim, 65 s | Sim | Sim | 4 | Se o aquecedor solar funciona em dias nublados | Explicaria melhor o funcionamento do aquecedor solar e do apoio elétrico |

## Indicadores
- **Taxa de acerto das orientações:** 15 acertos em 15 tarefas (100%).
- **Tempo médio para encontrar o custo do banho (tarefa 1):** 51,6 s (35, 48, 85, 25 e 65 s). O participante com menos familiaridade com computador levou mais tempo (85 s).
- **Facilidade média de utilização:** 4,2 de 5 (5, 4, 3, 5 e 4).

## Ajustes realizados a partir dos comentários (18/11/2026)
| Comentário | Ajuste feito no assistente |
|---|---|
| P1 e P3: diferença entre kWh e reais, termos técnicos | Nova **opção 8, "Entender os termos"**, que explica kWh, tarifa, apoio elétrico, retorno do investimento e estimativa. A opção 1 passou a mostrar "Como calculamos": kWh e depois reais, com a conta passo a passo. |
| P2: como o investimento é calculado | A opção 3 passou a explicar que o investimento **não é calculado**: é uma faixa de preços de mercado (estimativa), e que o retorno é investimento dividido pela economia por mês. |
| P2 e P4: comparação visual e gráficos | A opção 4 passou a exibir um **gráfico de barras em texto** com o custo mensal de cada alternativa. |
| P4: origem dos valores | A opção 1 passou a indicar a origem da tarifa sugerida (Enel SP, sem impostos, ANEEL), e as respostas remetem à opção 6 para dados e fontes. |
| P5: aquecedor solar em dias nublados e apoio elétrico | A opção 3 passou a explicar que a produção solar cai em dias nublados e o apoio elétrico completa o aquecimento, e por isso usamos uma média de 70% de energia solar, e não 100%. |
| P3: opções mais simples e instruções mais explicativas | O menu passou a mostrar "Digite o NÚMERO da opção e aperte Enter", e a coleta de dados informa que, se a pessoa não souber a resposta, basta apertar Enter para usar um valor sugerido. |

Observação: o gráfico foi feito em texto (barras) para manter o assistente em Python puro, sem bibliotecas externas.
