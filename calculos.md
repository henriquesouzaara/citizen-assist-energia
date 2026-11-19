# Cálculos e comparação das alternativas

Dados, origens e premissas: `dados/parametros.json`. Referências: `docs/referencias.md`.

## Necessidade e período de referência comum
Banho quente de uma família de 4 pessoas, 1 banho por pessoa por dia, durante 30 dias (1 mês).

## Fórmulas
- Energia (kWh) = potência (kW) x tempo (h)
- Consumo mensal do chuveiro = (potência em W / 1000) x (minutos / 60) x pessoas x banhos por dia x 30
- Custo mensal (R$) = kWh x tarifa (R$/kWh)
- CO2 (kg) = kWh x fator de emissão (0,0385 kg/kWh)
- Retorno (meses) = investimento / economia mensal em R$ (simples, sem juros)

## Cenário-base (estimativas identificadas)
Potência 5.500 W, banho de 10 min, tarifa R$ 0,78938/kWh (Enel SP, sem impostos), 4 pessoas.

| Alternativa | Consumo (kWh/mês) | Custo (R$/mês) | CO2 (kg/mês) | Investimento |
|---|---|---|---|---|
| 1. Chuveiro elétrico (base) | 110 | 86,83 | 4,24 | nenhum |
| 2. Banho de 7 min (economia por hábito) | 77 | 60,78 | 2,96 | nenhum |
| 3. Aquecedor solar com apoio elétrico (fração solar de 70%) | 33 | 26,05 | 1,27 | R$ 7.000 a R$ 20.000 |

Cálculo da base: 5,5 kW x (10/60 h) x 4 x 30 = 110 kWh. Banho de 7 min: 5,5 x (7/60) x 4 x 30 = 77 kWh. Solar: 110 x (1 - 0,70) = 33 kWh.

## Economia em relação à base
| Alternativa | Economia (kWh/mês) | Economia (R$/mês) | Economia (R$/ano) | CO2 evitado (kg/ano) |
|---|---|---|---|---|
| Banho de 7 min | 33 | 26,05 | 312,59 | 15,2 |
| Aquecedor solar | 77 | 60,78 | 729,39 | 35,6 |

**Retorno do aquecedor solar (simples):** R$ 7.000 / R$ 60,78 = 115 meses (9,6 anos). R$ 20.000 / R$ 60,78 = 329 meses (27,4 anos).

## Sensibilidade (para mostrar como os resultados mudam)
| Situação | Retorno do aquecedor solar |
|---|---|
| Cenário-base (10 min, tarifa sem impostos) | 9,6 a 27,4 anos |
| Banhos de 15 min (consumo-base de 165 kWh, economia solar de R$ 91,17/mês) | 6,4 a 18,3 anos |
| Tarifa com impostos de R$ 1,10/kWh (valor hipotético, para ilustrar) | 6,9 a 19,7 anos |

Quanto maior o uso de água quente e a tarifa efetiva, mais rápido o retorno.

## Justificativa das recomendações
**Custos**
- Banho mais curto: custo zero e economia imediata (R$ 26,05/mês no cenário-base).
- Aquecedor solar: economia maior por mês (R$ 60,78), mas exige investimento alto e retorno de longo prazo.

**Viabilidade**
- O hábito depende só da família, mas exige mudança de comportamento e pode não se manter.
- O aquecedor solar exige casa própria (ou autorização), telhado adequado, instalação e manutenção. Em imóvel alugado costuma não compensar.

**Impactos ambientais**
- Os dois reduzem o uso de eletricidade. O ganho em CO2 é pequeno (15 a 36 kg por ano) porque o fator de emissão da eletricidade brasileira é baixo.
- Estudo citado nas referências aponta também redução da demanda de pico, benefício para a rede elétrica.
- Não foram considerados o impacto da fabricação e do descarte dos equipamentos.

**Conclusão usada pelo assistente**
1. Comece pelo hábito (custo zero).
2. Considere o aquecedor solar apenas se a casa for própria e o retorno estimado compensar para a família.

## Limites da análise
Estimativas, não garantias. Payback simples, sem juros, inflação, manutenção ou vida útil. Dados com fonte jornalística ou de estudos específicos podem diferir da realidade de cada casa.
