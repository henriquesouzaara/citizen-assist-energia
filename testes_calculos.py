# -*- coding: utf-8 -*-
"""Testes automáticos dos cálculos (rode: python testes_calculos.py)."""

import energia

PAR = energia.carregar_parametros()


def aprox(a, b, tol=0.01):
    return abs(a - b) <= tol


def teste_consumo_base():
    # 5,5 kW x (10/60 h) x 4 pessoas x 30 dias = 110 kWh
    assert aprox(energia.consumo_mensal_kwh(4, 10, 5500), 110.0)


def teste_banho_curto():
    assert aprox(energia.consumo_mensal_kwh(4, 7, 5500), 77.0)


def teste_comparacao_cenario_base():
    c = energia.comparar(4, 10, 5500, PAR["tarifa_kwh"]["valor"], PAR)
    assert aprox(c["base"]["reais"], 86.83)
    assert aprox(c["curto"]["reais"], 60.78)
    assert aprox(c["solar"]["kwh"], 33.0)
    assert aprox(c["eco_solar"]["reais"], 60.78)
    assert aprox(c["retorno_min_anos"], 9.6, 0.05)
    assert aprox(c["retorno_max_anos"], 27.4, 0.05)
    assert aprox(c["base"]["co2"], 4.235, 0.005)


def teste_sem_economia():
    assert energia.retorno_meses(7000, 0) is None


def teste_banho_ja_curto():
    c = energia.comparar(4, 5, 5500, 0.78938, PAR)
    assert c["eco_curto"]["kwh"] == 0  # banho de 5 min já é menor que o alvo de 7


def teste_recomendacao_alugado():
    c = energia.comparar(4, 10, 5500, 0.78938, PAR)
    texto = " ".join(energia.recomendar(c, casa_propria=False))
    assert "alugado" in texto


if __name__ == "__main__":
    testes = [v for k, v in sorted(globals().items()) if k.startswith("teste_")]
    for t in testes:
        t()
        print("OK  ", t.__name__)
    print("\n%d testes passaram." % len(testes))
