import pandas

# Base de Dados utilizado = 
df = pandas.read_excel("baseDados01.xlsx")# Organiza em ordem numérica.
# Coloca base de dados na variável df

# ----------------------------------- #

# VARIÁVEL QUANTITATIVA DISCRETA --> WAITING TIME

freq_discreta = df['waiting_time'].value_counts().sort_index() # Conta os valores e organiza em ordem numérica.

print("TABELA DE FREQUÊNCIA - WAITING TIME")
print(freq_discreta)

# Insight 1: A maioria dos tempos de espera ficou entre 8 e 14, mostrando que existe certa demora com frequência.
# Insight 2: Isso mostra que um sistema automático pode ajudar a organizar melhor o carregamento.

# ----------------------------------- #

# VARIÁVEL QUANTITATIVA CONTÍNUA --> ELECTRICITY PRICE

df['electricity_price'] = pandas.to_numeric(df['electricity_price'], errors='coerce') # Faz com que os valores obtidos sejam transformados em números

classes = pandas.cut(df['electricity_price'], bins=8) # Agrupa os valores e divide o intervalo total em 8 pedaços

freq_continua = classes.value_counts().sort_index()

print()
print("TABELA DE FREQUÊNCIA - ELECTRICITY PRICE")
print(freq_continua)

# Insight 1: Os preços ficaram mais concentrados em algumas faixas específicas.
# Insight 2: Isso pode ajudar a pensar em formas melhores de cobrança dependendo da demanda.
