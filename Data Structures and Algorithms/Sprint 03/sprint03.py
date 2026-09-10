sessoes = []
comandosDisponiveis = [0, 1, 2, 3, 4, 5, 6]

preco_kWh = 1.97
tarifa = 0.89
potencia = 7

# ================================================================================

class Sessao:
    def __init__(self, id, energia, tempo, custo):
        self.id = id
        self.energia = energia
        self.tempo = tempo
        self.custo = custo

    def __repr__(self):
        return (f"\nId   Sessão = {self.id}\n"
                f"Energia Carregada = {self.energia} kWh\n"
                f"Tempo de Carregamento = {self.tempo:.2f} horas\n"
                f"Custo total = R$ {self.custo:.2f}\n")

# ================================================================================

def inserirLinha():
    print("=" * 53)

def msgBemVindo():
    inserirLinha()
    print("      Bem-vindo à Estação de Recarga ChargeVolt")
    inserirLinha()
    print("\nComandos disponiveis:")

def msgComandos():
    print(f"""
[ 0 ] Sair
[ 1 ] Nova sessão de recarga
[ 2 ] Listar sessões
[ 3 ] Buscar sesão
[ 4 ] Ordernar sessões
[ 5 ] Estatísticas
[ 6 ] Encerrar
""")

# ================================================================================

def novaEntrada():
    comandoAtual = None

    if comandoAtual is None:
        msgBemVindo()
        msgComandos()
        comandoAtual = int(input("Insira o comando desejado: "))

        while comandoAtual not in comandosDisponiveis:
            comandoAtual = int(input("Comando Inválido! Tente novamente: "))
        inserirLinha()

    return comandoAtual

def notNovaEntrada():
    input("Pressione ENTER para continuar...")
    inserirLinha()

    print("\nSelecione um novo comando")
    msgComandos()

    comandoAtual = int(input("Insira o comando desejado: "))

    while comandoAtual not in comandosDisponiveis:
        comandoAtual = int(input("Comando Inválido! Tente novamente: "))
    inserirLinha()

    return comandoAtual

# ================================================================================

cmndEsc = novaEntrada()

if cmndEsc == 0:
    print("Saindo da Estação de Recarga!")
    exit()

# ================================================================================

while cmndEsc == 1:

    idAtual = len(sessoes) + 1

    print(f"""
Iniciando nova sessão de recarga!

Potência do Carregamento: {potencia} kW
Valor do Kwh: {preco_kWh} kWh
Valor da Tarifa: {tarifa}R$/kWh""")

    valorCarregado = int(input("\nInsira o valor a ser carregado: "))

    tempEstim = valorCarregado / potencia
    custoAtual = valorCarregado * (preco_kWh + tarifa)

    print(f"\nTempo estimado: {tempEstim:.2f} horas")
    print(f"Custo da recarga = {custoAtual:.2f}R$\n")

    sessaoAtual = Sessao(id = idAtual, energia = valorCarregado, tempo = tempEstim, custo = custoAtual)
    sessoes.append(sessaoAtual)

    print("Sessão Registrada com sucesso!\n")
    inserirLinha()

    cmndEsc = notNovaEntrada()

# ================================================================================

while cmndEsc == 2:
    print(sessoes)
    inserirLinha()

    cmndEsc = notNovaEntrada()

# ================================================================================

# while cmndEsc == 3: