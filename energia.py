# -*- coding: utf-8 -*-
"""
Cálculos do módulo de Energia do Citizen Assist AI (GS 2026.2 - Soluções em Energias
Renováveis e Sustentáveis).

Necessidade energética: banho quente em casa de família.
Alternativas comparadas para a MESMA necessidade e o MESMO período (1 mês):
  1) Base: chuveiro elétrico
  2) Economia: banho mais curto (hábito)
  3) Renovável: aquecedor solar de água com apoio elétrico

Fórmula básica: E (kWh) = P (kW) x t (h)
"""

import json
import os

PASTA = os.path.dirname(os.path.abspath(__file__))


def carregar_parametros(caminho=None):
    """Lê os parâmetros (valores, origem e premissas) do arquivo JSON."""
    caminho = caminho or os.path.join(PASTA, "dados", "parametros.json")
    with open(caminho, encoding="utf-8") as arq:
        return json.load(arq)


def consumo_mensal_kwh(pessoas, minutos, potencia_w, banhos_dia=1, dias=30):
    """Energia do chuveiro em um mês: potência (kW) x horas totais de uso."""
    horas = (minutos / 60) * pessoas * banhos_dia * dias
    return (potencia_w / 1000) * horas


def custo_reais(kwh, tarifa):
    return kwh * tarifa


def co2_kg(kwh, fator_kg_por_kwh):
    return kwh * fator_kg_por_kwh


def retorno_meses(investimento, economia_mensal_reais):
    """Payback simples (sem juros e sem manutenção). None se não houver economia."""
    if economia_mensal_reais <= 0:
        return None
    return investimento / economia_mensal_reais


def comparar(pessoas, minutos, potencia_w, tarifa, par):
    """Compara as três alternativas e devolve um dicionário com os resultados."""
    banhos = par["banhos_por_pessoa_dia"]["valor"]
    dias = par["dias_mes"]["valor"]
    fator = par["fator_emissao_kg_kwh"]["valor"]
    fracao = par["fracao_solar"]["valor"]
    inv_min = par["custo_aquecedor_solar_min"]["valor"]
    inv_max = par["custo_aquecedor_solar_max"]["valor"]
    minutos_curto = min(par["minutos_banho_curto"]["valor"], minutos)

    kwh_base = consumo_mensal_kwh(pessoas, minutos, potencia_w, banhos, dias)
    kwh_curto = consumo_mensal_kwh(pessoas, minutos_curto, potencia_w, banhos, dias)
    kwh_solar = kwh_base * (1 - fracao)

    def linha(kwh):
        return {"kwh": kwh, "reais": custo_reais(kwh, tarifa), "co2": co2_kg(kwh, fator)}

    base, curto, solar = linha(kwh_base), linha(kwh_curto), linha(kwh_solar)
    eco_curto = {k: base[k] - curto[k] for k in base}
    eco_solar = {k: base[k] - solar[k] for k in base}
    meses_min = retorno_meses(inv_min, eco_solar["reais"])
    meses_max = retorno_meses(inv_max, eco_solar["reais"])
    return {
        "minutos_curto": minutos_curto,
        "base": base,
        "curto": curto,
        "solar": solar,
        "eco_curto": eco_curto,
        "eco_solar": eco_solar,
        "inv_min": inv_min,
        "inv_max": inv_max,
        "retorno_min_anos": None if meses_min is None else meses_min / 12,
        "retorno_max_anos": None if meses_max is None else meses_max / 12,
    }


def _v(valor):
    """Número com 1 casa decimal e vírgula."""
    return ("%.1f" % valor).replace(".", ",")


def recomendar(c, casa_propria):
    """Regras simples que ligam os resultados da análise às orientações do assistente."""
    linhas = []
    if c["eco_curto"]["kwh"] > 0:
        linhas.append(
            "1) Comece pelo hábito: com banhos de %d min você economizaria cerca de "
            "%.0f kWh por mês, sem gastar nada." % (c["minutos_curto"], c["eco_curto"]["kwh"])
        )
    else:
        linhas.append("1) Seus banhos já são curtos. Reduzir mais o tempo traz pouca economia.")

    anos_min = c["retorno_min_anos"]
    anos_max = c["retorno_max_anos"]
    if anos_min is None:
        linhas.append("2) Com esses dados o aquecedor solar não gera economia calculável.")
    elif not casa_propria:
        linhas.append(
            "2) Aquecedor solar exige instalação no telhado e retorno de longo prazo. "
            "Em imóvel alugado costuma não compensar."
        )
    elif anos_min <= 8:
        linhas.append(
            "2) O aquecedor solar pode compensar: retorno estimado de %s a %s anos, "
            "conforme o preço do kit. Peça orçamentos." % (_v(anos_min), _v(anos_max))
        )
    elif anos_min <= 15:
        linhas.append(
            "2) O aquecedor solar tem retorno longo: %s a %s anos. Só vale a pena se "
            "a casa é sua e você pretende ficar muitos anos nela." % (_v(anos_min), _v(anos_max))
        )
    else:
        linhas.append(
            "2) O retorno financeiro do aquecedor solar seria muito longo (%s a %s "
            "anos) só pela economia do chuveiro. Priorize o hábito." % (_v(anos_min), _v(anos_max))
        )
    return linhas
