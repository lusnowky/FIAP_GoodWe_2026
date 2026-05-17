import pandas

# Carregar base
df = pandas.read_excel("chargegrid.xlsx")

# ----------------------------------- #

# VARIÁVEL QUANTITATIVA DISCRETA --> WAITING TIME

freq_discreta = df['waiting_time'].value_counts().sort_index()

print("TABELA DE FREQUÊNCIA - WAITING TIME")
print(freq_discreta)

# Insight 1: A maioria dos tempos de espera ficou entre 8 e 14, mostrando que existe certa demora com frequência.
# Insight 2: Isso mostra que um sistema automático pode ajudar a organizar melhor o carregamento.

# ----------------------------------- #

# VARIÁVEL QUANTITATIVA CONTÍNUA --> ELECTRICITY PRICE

df['electricity_price'] = pandas.to_numeric(df['electricity_price'], errors='coerce')

classes = pandas.cut(df['electricity_price'], bins=8)

freq_continua = classes.value_counts().sort_index()

print()
print("TABELA DE FREQUÊNCIA - ELECTRICITY PRICE")
print(freq_continua)

# Insight 1: Os preços ficaram mais concentrados em algumas faixas específicas.
# Insight 2: Isso pode ajudar a pensar em formas melhores de cobrança dependendo da demanda.