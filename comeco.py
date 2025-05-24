# Crie um programa que:
# 1. Pergunte seu nome
# 2. Pergunte sua idade
# 3. Calcule em que ano você nasceu
# 4. Mostre uma mensagem personalizada

from datetime import datetime

nome = input("Qual seu nome? ")

idade = int(input("Qual sua idade? "))

mes_nasc = int(input("Em que mês você nasceu? (1-12) "))

ano_atual = datetime.now().year
mes_atual = datetime.now().month

if mes_atual >= mes_nasc:
    ano_nascimento = ano_atual - idade
else:
    ano_nascimento = ano_atual - idade - 1