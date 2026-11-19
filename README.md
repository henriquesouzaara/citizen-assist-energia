# Citizen Assist AI: módulo de Energia (banho quente em casa de família)

Global Solution 2026.2 · FIAP · 1º ano de Ciência da Computação · Soluções em Energias Renováveis e Sustentáveis

## Integrantes
- Leonardo Scotti Tobias (RM 573305)
- Henrique de Souza Aragão (RM 570529)
- Natan Silva da Costa (RM 573100)

## Contribuição desta disciplina ao Citizen Assist AI
Este repositório contém a **contribuição de Soluções em Energias Renováveis e Sustentáveis** ao desafio Citizen Assist AI: um módulo do assistente digital que orienta famílias sobre o uso consciente de energia no **banho quente**. O módulo é independente e pode ser testado separadamente.

## Público e problema
- **Público:** famílias que usam chuveiro elétrico (exemplo-base: 4 pessoas, casa na capital de São Paulo).
- **Necessidade energética:** o chuveiro elétrico tem potência alta e uso diário, e costuma pesar na conta de luz. A família precisa saber quanto gasta e se vale a pena mudar o hábito ou investir em uma fonte renovável.
- **Como o assistente ajuda:** responde com custo, economia, retorno do investimento e impacto ambiental, sempre com referências e avisos de limitação.

## Funcionalidades de energia
| Opção do menu | O que responde | Onde está o cálculo |
|---|---|---|
| 1 | Quanto custa o banho da minha casa | `energia.consumo_mensal_kwh`, `custo_reais`, `co2_kg` |
| 2 | Quanto economizo com banho mais curto | `energia.comparar` (alternativa de economia) |
| 3 | Vale a pena um aquecedor solar de água | `energia.comparar` (alternativa renovável) e `recomendar` |
| 4 | Comparação das três alternativas | `energia.comparar` |
| 5 | Pergunta digitada (reconhece palavras-chave) | `assistente.responder_pergunta` |
| 6 | Dados, premissas, fontes e limitações | `dados/parametros.json` |
| 7 | Informar outros dados da casa | `assistente.coletar_dados` |
| 8 | Entender os termos (kWh, tarifa, apoio elétrico) | `assistente.explicar_termos` |

As três alternativas são comparadas para a **mesma necessidade** (banho quente de uma família) e o **mesmo período** (1 mês): chuveiro elétrico (base), banho mais curto (economia por hábito) e aquecedor solar de água com apoio elétrico (fonte renovável).

## Como executar
Requisitos: Python 3.8 ou mais recente (sem bibliotecas externas).

```bash
python assistente.py        # assistente interativo
python testes_calculos.py   # testes automáticos dos cálculos
```

No assistente, pressione Enter para usar os valores sugeridos, ou digite os dados da sua casa (pessoas, minutos de banho, potência do chuveiro e preço do kWh da sua conta).

## Estrutura do repositório
```
assistente.py              assistente de linha de comando (menu, perguntas, tratamento de entradas inválidas)
energia.py                 cálculos de consumo, custo, CO2, retorno e recomendações
dados/parametros.json      dados e premissas, cada um com origem, tipo (oficial ou estimativa) e data
docs/calculos.md           cálculos, comparação das alternativas e justificativas
docs/referencias.md        referências com data de consulta
docs/testes_usuarios.md    roteiro e registro dos testes com usuários
testes_calculos.py         testes automáticos
```

## Como a análise sustenta as respostas do assistente
Todos os números exibidos pelo assistente vêm de `dados/parametros.json` e das fórmulas de `energia.py`, descritas em `docs/calculos.md`. As respostas de recomendação (hábito primeiro, solar só se a casa for própria e o retorno compensar) seguem diretamente dos resultados dessa comparação.

## Limitações
- O assistente **não é canal oficial** e **não garante** economia, geração ou custo. Os valores são estimativas.
- A tarifa padrão é a da Enel SP **sem impostos**; a conta real é maior. O usuário pode informar a tarifa da própria conta.
- O retorno do investimento é um cálculo simples, sem juros, inflação, manutenção ou vida útil.
- Preços do aquecedor solar vêm de fonte jornalística e variam; peça orçamentos reais.
- A fração solar (70%) vem de um estudo e depende de clima, instalação e uso do apoio elétrico.
- O ganho de CO2 é pequeno porque a eletricidade brasileira já é, em média, de baixa emissão.
- Nenhum dado pessoal é coletado ou gravado.
