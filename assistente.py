#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Citizen Assist AI - Módulo de Energia (banho quente em casa de família)
Global Solution 2026.2 - FIAP - Soluções em Energias Renováveis e Sustentáveis

Assistente de linha de comando que orienta famílias sobre o gasto de energia do chuveiro
elétrico e compara três alternativas: chuveiro elétrico (base), banho mais curto e
aquecedor solar de água (fonte renovável).

AVISO: protótipo educacional. NÃO é canal oficial de nenhuma distribuidora ou órgão
público. Os valores são estimativas, e não garantias de economia. O programa não coleta
nem grava dados pessoais: usa apenas números digitados na hora, mantidos só na memória.
"""

import sys
import unicodedata

import energia

PAR = energia.carregar_parametros()


# ---------------------------------------------------------------------------
# Formatação
# ---------------------------------------------------------------------------
def brl(valor):
    texto = "{:,.2f}".format(valor)
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def dec(valor, casas=1):
    """Número com vírgula decimal (padrão brasileiro)."""
    return ("%.*f" % (casas, valor)).replace(".", ",")


def anos(valor):
    return dec(valor) + " anos"


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------------------
# Entrada de dados com tratamento de entradas inválidas
# ---------------------------------------------------------------------------
def ler_numero(pergunta, minimo, maximo, padrao, inteiro=False):
    """Lê um número no intervalo [minimo, maximo]. Enter usa o valor padrão."""
    while True:
        bruto = input("%s [Enter = %s]: " % (pergunta, padrao)).strip().replace(",", ".")
        if bruto == "":
            return padrao
        try:
            valor = int(bruto) if inteiro else float(bruto)
        except ValueError:
            print("  Entrada inválida. Digite apenas números (exemplo: 10).\n")
            continue
        if not (minimo <= valor <= maximo):
            print("  Valor fora do intervalo aceito (%s a %s).\n" % (minimo, maximo))
            continue
        return valor


def ler_sim_nao(pergunta):
    while True:
        resposta = normalizar(input(pergunta + " [s/n]: "))
        if resposta in ("s", "sim", "1"):
            return True
        if resposta in ("n", "nao", "0"):
            return False
        print("  Resposta inválida. Digite 's' para sim ou 'n' para não.\n")


def ler_opcao(validas):
    while True:
        escolha = normalizar(input("Escolha uma opção: "))
        if escolha in validas:
            return escolha
        print("Opção inválida. Escolha entre: " + ", ".join(sorted(validas)) + ".\n")


# ---------------------------------------------------------------------------
# Telas
# ---------------------------------------------------------------------------
def aviso_inicial():
    print("=" * 68)
    print(" CITIZEN ASSIST AI - Energia: banho quente em casa de família")
    print("=" * 68)
    print(" AVISO: protótipo educacional. NÃO é canal oficial e NÃO garante")
    print(" economia: os valores são estimativas. Não coletamos dados pessoais.")
    print(" Dados e fontes consultados em " + PAR["consulta"] + ".")
    print("=" * 68)


def rodape():
    print("\nLimitações: estimativas com base nas premissas acima. Tarifa sem impostos")
    print("(a conta real é maior). Resultados dependem de clima, instalação e hábitos.")
    print("Fontes: veja a opção 6.\n")


def explicar_termos():
    print("\nENTENDENDO OS TERMOS")
    print("- kWh (quilowatt-hora): quantidade de energia usada. É o que o medidor da sua")
    print("  casa mede. Um chuveiro de 5,5 kW ligado por 1 hora gasta 5,5 kWh.")
    print("- Tarifa (R$ por kWh): preço de cada kWh. Custo em reais = kWh x tarifa.")
    print("- Apoio elétrico: resistência elétrica que completa o aquecimento da água quando")
    print("  o sol não basta (dia nublado ou muito uso).")
    print("- Retorno do investimento: tempo que a economia leva para pagar a compra e a")
    print("  instalação. Retorno = investimento dividido pela economia por mês.")
    print("- Estimativa: valor aproximado, com base em premissas. Não é garantia.\n")


def coletar_dados():
    print("\nVamos conhecer a sua casa (só números, nada é gravado).")
    print("Se não souber a resposta, aperte Enter: usamos um valor sugerido.\n")
    pessoas = ler_numero("Quantas pessoas tomam banho quente por dia?", 1, 12,
                         PAR["pessoas"]["valor"], inteiro=True)
    minutos = ler_numero("Quantos minutos dura cada banho?", 1, 60,
                         PAR["minutos_banho"]["valor"])
    potencia = ler_numero("Potência do chuveiro em watts (está na etiqueta)?", 1500, 8000,
                          PAR["potencia_chuveiro_w"]["valor"], inteiro=True)
    print("\nTarifa: preço do kWh na sua conta de luz. O valor sugerido é o da Enel SP")
    print("(capital) SEM impostos. Se informar o da sua conta, a análise fica mais real.")
    tarifa = ler_numero("Preço do kWh em R$?", 0.30, 3.00, PAR["tarifa_kwh"]["valor"])
    return {"pessoas": pessoas, "minutos": minutos, "potencia": potencia, "tarifa": tarifa}


def calcular(dados):
    return energia.comparar(dados["pessoas"], dados["minutos"], dados["potencia"],
                            dados["tarifa"], PAR)


def mostrar_custo(dados):
    c = calcular(dados)
    b = c["base"]
    print("\nSEU BANHO HOJE (chuveiro elétrico)")
    print("  %d pessoa(s) x %s min x %d W, por 30 dias" %
          (dados["pessoas"], dados["minutos"], dados["potencia"]))
    print("  Consumo: %.0f kWh por mês" % b["kwh"])
    print("  Custo estimado: %s por mês (%s por ano)" % (brl(b["reais"]), brl(b["reais"] * 12)))
    print("  Emissão de CO2 da eletricidade usada: %s kg por mês" % dec(b["co2"]))
    print("\n  Como calculamos:")
    print("   1) Energia (kWh) = potência (kW) x horas de banho no mês = %.0f kWh" % b["kwh"])
    print("   2) Custo (R$) = kWh x preço do kWh = %.0f x %s = %s" %
          (b["kwh"], dec(dados["tarifa"], 5), brl(b["reais"])))
    print("  Origem da tarifa sugerida: Enel SP, sem impostos (ANEEL). Veja a opção 6.")
    rodape()


def mostrar_banho_curto(dados):
    c = calcular(dados)
    print("\nECONOMIA COM BANHO MAIS CURTO (%d min)" % c["minutos_curto"])
    if c["eco_curto"]["kwh"] <= 0:
        print("  Seus banhos já têm %s min ou menos. Não há economia calculável." % dados["minutos"])
    else:
        e = c["eco_curto"]
        print("  Consumo: de %.0f para %.0f kWh por mês" % (c["base"]["kwh"], c["curto"]["kwh"]))
        print("  Economia: %.0f kWh = %s por mês (%s por ano)" %
              (e["kwh"], brl(e["reais"]), brl(e["reais"] * 12)))
        print("  Custo de implantação: nenhum (depende de mudar o hábito).")
    rodape()


def mostrar_solar(dados):
    c = calcular(dados)
    casa_propria = ler_sim_nao("\nA casa é própria (ou você pode instalar equipamento no telhado)?")
    e = c["eco_solar"]
    print("\nAQUECEDOR SOLAR DE ÁGUA (fonte renovável, com apoio elétrico)")
    print("  Premissa: o sol fornece %d%% da energia do banho (estimativa de estudo)." %
          round(PAR["fracao_solar"]["valor"] * 100))
    print("  Consumo: de %.0f para %.0f kWh por mês" % (c["base"]["kwh"], c["solar"]["kwh"]))
    print("  Economia: %s por mês (%s por ano) e %s kg de CO2 por mês" %
          (brl(e["reais"]), brl(e["reais"] * 12), dec(e["co2"])))
    print("  Investimento estimado: %s a %s" % (brl(c["inv_min"]), brl(c["inv_max"])))
    if c["retorno_min_anos"] is not None:
        print("  Retorno estimado: %s a %s (sem juros e sem manutenção)" %
              (anos(c["retorno_min_anos"]), anos(c["retorno_max_anos"])))
    print("\n  Como o retorno é calculado: investimento / economia por mês. O investimento")
    print("  NÃO é calculado pelo programa: é uma faixa de preços de mercado (estimativa).")
    print("  Em dias nublados a produção solar cai e o apoio elétrico completa o")
    print("  aquecimento. Por isso usamos uma média de 70% de energia solar, e não 100%.")
    print("\nORIENTAÇÃO")
    for linha in energia.recomendar(c, casa_propria):
        print("  " + linha)
    print("\n  Obs.: o ganho em CO2 é pequeno porque a eletricidade brasileira já é, em")
    print("  média, de baixa emissão. Peça orçamentos e confirme com o fabricante.")
    rodape()


def mostrar_comparacao(dados):
    c = calcular(dados)
    casa_propria = ler_sim_nao("\nA casa é própria (ou você pode instalar equipamento no telhado)?")
    print("\nCOMPARAÇÃO PARA A MESMA NECESSIDADE (banho quente, 1 mês)")
    print("-" * 68)
    print("%-30s %9s %12s %10s" % ("Alternativa", "kWh/mês", "Custo/mês", "CO2 kg"))
    nomes = (("Chuveiro elétrico (base)", c["base"]),
             ("Banho de %d min" % c["minutos_curto"], c["curto"]),
             ("Aquecedor solar", c["solar"]))
    for nome, v in nomes:
        print("%-30s %9.0f %12s %10s" % (nome, v["kwh"], brl(v["reais"]), dec(v["co2"])))
    print("-" * 68)
    print("\nGráfico do custo por mês (cada bloco = cerca de R$ 3):")
    maior = max(v["reais"] for _, v in nomes) or 1
    for nome, v in nomes:
        blocos = max(1, round(v["reais"] / maior * 28))
        print("  %-26s %s %s" % (nome, "█" * blocos, brl(v["reais"])))
    print()
    print("Investimento: banho curto = nenhum | aquecedor solar = %s a %s" %
          (brl(c["inv_min"]), brl(c["inv_max"])))
    if c["retorno_min_anos"] is not None:
        print("Retorno do aquecedor solar: %s a %s" %
              (anos(c["retorno_min_anos"]), anos(c["retorno_max_anos"])))
    print("\nORIENTAÇÃO")
    for linha in energia.recomendar(c, casa_propria):
        print("  " + linha)
    rodape()


def mostrar_referencias():
    print("\nDADOS, PREMISSAS E FONTES (consultados em " + PAR["consulta"] + ")")
    for chave, item in PAR.items():
        if chave == "consulta":
            continue
        print("\n- %s = %s %s  [%s]" % (chave, item["valor"], item["unidade"], item["tipo"]))
        print("  Origem: " + item["origem"])
        print("  Premissa: " + item["premissa"])
    print("\nLIMITAÇÕES")
    print("- Este assistente NÃO é canal oficial e NÃO garante economia, geração ou custo.")
    print("- Estimativas dependem de clima, instalação, preço de mercado e hábitos.")
    print("- Retorno calculado de forma simples (sem juros, inflação, manutenção ou vida útil).")
    print("- Tarifa sem impostos: a conta real costuma ser maior.")
    print("- Nenhum dado pessoal é coletado ou armazenado.\n")


def responder_pergunta(dados_fn):
    """Roteador simples por palavras-chave para perguntas digitadas."""
    texto = normalizar(input("\nDigite sua pergunta (ex.: 'vale a pena aquecedor solar?'): "))
    if not texto:
        print("  Pergunta vazia. Tente escrever uma frase curta.\n")
        return
    if any(p in texto for p in ("solar", "aquecedor", "renov")):
        mostrar_solar(dados_fn())
    elif any(p in texto for p in ("economi", "reduz", "curto", "menos", "diminu")):
        mostrar_banho_curto(dados_fn())
    elif any(p in texto for p in ("custa", "custo", "quanto", "gasto", "conta")):
        mostrar_custo(dados_fn())
    elif any(p in texto for p in ("fonte", "referenc", "dado", "origem")):
        mostrar_referencias()
    elif any(p in texto for p in ("limit", "garant", "certeza")):
        mostrar_referencias()
    else:
        print("  Não entendi a pergunta. Eu respondo sobre: custo do banho, economia com")
        print("  banho curto, aquecedor solar, fontes e limitações. Use o menu ou reformule.\n")


def menu():
    aviso_inicial()
    sessao = {"dados": None}

    def obter_dados():
        if sessao["dados"] is None:
            sessao["dados"] = coletar_dados()
        return sessao["dados"]

    while True:
        print("MENU")
        print("  1 - Quanto custa o banho da minha casa?")
        print("  2 - Quanto economizo com banho mais curto?")
        print("  3 - Vale a pena um aquecedor solar de água?")
        print("  4 - Comparar as três alternativas")
        print("  5 - Fazer uma pergunta")
        print("  6 - Ver dados, fontes e limitações")
        print("  7 - Informar outros dados da minha casa")
        print("  8 - Entender os termos (kWh, tarifa, apoio elétrico...)")
        print("  0 - Sair")
        print("Digite o NÚMERO da opção e aperte Enter.")
        opcao = ler_opcao({"0", "1", "2", "3", "4", "5", "6", "7", "8"})
        if opcao == "1":
            mostrar_custo(obter_dados())
        elif opcao == "2":
            mostrar_banho_curto(obter_dados())
        elif opcao == "3":
            mostrar_solar(obter_dados())
        elif opcao == "4":
            mostrar_comparacao(obter_dados())
        elif opcao == "5":
            responder_pergunta(obter_dados)
        elif opcao == "6":
            mostrar_referencias()
        elif opcao == "7":
            sessao["dados"] = coletar_dados()
        elif opcao == "8":
            explicar_termos()
        else:
            print("Até logo!")
            return


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    try:
        menu()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrado.")


if __name__ == "__main__":
    main()
