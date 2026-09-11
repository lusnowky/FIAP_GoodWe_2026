# ================================================================================
#                                    VARIÁVEIS
# ================================================================================
sessoes = []
comandosDisponiveis = [0, 1, 2, 3, 4, 5]

preco_kWh = 1.97
tarifa = 0.89
potencia = 7

# ================================================================================
#                                   CLASS SESSÃO
# ================================================================================

class Sessao:
    def __init__(self, id, energia, tempo, custo):
        self.id = id
        self.energia = energia
        self.tempo = tempo
        self.custo = custo

    def __repr__(self):
        return (f"\nID da sessão = {self.id}\n"
                f"Energia carregada = {self.energia} kWh\n"
                f"Tempo de carregamento = {self.tempo:.2f} horas\n"
                f"Custo total = R$ {self.custo:.2f}\n")

# ================================================================================
#                                    MENSAGENS
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
[ 3 ] Buscar sessão
[ 4 ] Ordenar sessões
[ 5 ] Estatísticas
""")

# ================================================================================
#                                  ENTRADAS
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

    print("\nSelecione um novo comando:")
    msgComandos()

    comandoAtual = int(input("Insira o comando desejado: "))

    while comandoAtual not in comandosDisponiveis:
        comandoAtual = int(input("Comando Inválido! Tente novamente: "))
    inserirLinha()

    return comandoAtual

# ================================================================================
#                                   BUBBLE SORTS
# ================================================================================

def bubbleSortID(lista):

    n = len(lista)

    for i in range(n):
        for j in range(n - 1 - i):
            if lista[j].id > lista[j + 1].id:
                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista

def bubbleSortEnergia(lista):

    n = len(lista)

    for i in range(n):
        for j in range(n - 1 - i):
            if lista[j].energia > lista[j + 1].energia:
                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista

def bubbleSortTempo(lista):

    n = len(lista)

    for i in range(n):
        for j in range(n - 1 - i):
            if lista[j].tempo > lista[j + 1].tempo:
                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista

def bubbleSortCusto(lista):

    n = len(lista)

    for i in range(n):
        for j in range(n - 1 - i):
            if lista[j].custo > lista[j + 1].custo:
                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista


# ================================================================================
#                                 BUSCA SEQUENCIAL
# ================================================================================

def busca_sequencial(lista, idProcurado):

    for i in range(len(lista)):
        if lista[i].id == idProcurado:
            return i

    return -1

# ================================================================================
#                               NOVA SESSÃO DE RECARGA
# ================================================================================

def cmndEsc01():

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

    sessaoAtual = Sessao(
        id = idAtual,
        energia = valorCarregado,
        tempo = tempEstim,
        custo = custoAtual
    )

    sessoes.append(sessaoAtual)

    print("Sessão Registrada com sucesso!\n")
    inserirLinha()

# ================================================================================
#                                  LISTAR SESSÕES
# ================================================================================

def cmndEsc02():

    if len(sessoes) == 0:
        print("\nNenhuma sessão registrada ainda.\n")
    else:
        print(sessoes)
    inserirLinha()

# ================================================================================
#                                  BUSCAR SESSÃO
# ================================================================================

def cmndEsc03():

    print(f"\nIniciando busca...")
    sessaoProcurada = int(input("Insira o ID da sessão desejada: "))

    resultadoBusca = busca_sequencial(sessoes, sessaoProcurada)

    if resultadoBusca != -1:
        print("Sessão encontrada!")
        print(sessoes[resultadoBusca])
        inserirLinha()

    else:
        print("\nSessão não encontrada! Tente novamente ou escolha outro comando")
        print("[ 1 ] Tentar novamente\n[ 2 ] Escolher outro comando\n[ 3 ] Sair\n")

        escolhacmndEsc3 = int(input("Selecione a opção desejada: "))

        if escolhacmndEsc3 == 1:
            cmndEsc03()

        elif escolhacmndEsc3 == 3:
            exit()
        
        else:
            print("\nOpção inválida! Retornando ao menu principal...")
            inserirLinha()

# ================================================================================
#                                  ORDENAR SESSÕES
# ================================================================================

def cmndEsc04():

    print("\nOrdenando sessões...")
    print("Critérios de ordenação disponíveis:\n[ 1 ] ID\n[ 2 ] Energia\n[ 3 ] Tempo\n[ 4 ] Custo\n")

    critOrd = int(input("Selecione o critério desejado: "))
    vetorOrdenado = []

    if critOrd == 1:
        sessoesOrg = bubbleSortID(sessoes)
        print("\nSessões ordenadas por ID:\n")
        print(sessoesOrg)
        inserirLinha()

    elif critOrd == 2:
        sessoesOrg = bubbleSortEnergia(sessoes)
        print("\nSessões ordenadas por Energia:\n")
        print(sessoesOrg)
        inserirLinha()

    elif critOrd == 3:
        sessoesOrg = bubbleSortTempo(sessoes)
        print("\nSessões ordenadas por Tempo:\n")
        print(sessoesOrg)
        inserirLinha()

    elif critOrd == 4:
        sessoesOrg = bubbleSortCusto(sessoes)
        print("\nSessões ordenadas por Custo:\n")
        print(sessoesOrg)
        inserirLinha()

    else:
        print("\nCritério inválido! Tente novamente ou escolha outro comando")
        print("[ 1 ] Tentar novamente\n[ 2 ] Escolher outro comando\n[ 3 ] Sair\n")

        escolhacmndEsc4 = int(input("Selecione a opção desejada: "))

        if escolhacmndEsc4 == 1:
            cmndEsc04()

        elif escolhacmndEsc4 == 3:
            exit()

# ================================================================================
#                              ESTATÍSTICAS DAS SESSÕES
# ================================================================================

def cmndEsc05():

    print("\nEstatísticas das sessões de recarga:\n")
    print(f"Total de sessões: {len(sessoes)}\n")

    if len(sessoes) > 0:

        energiaTotal = sum(sessao.energia for sessao in sessoes)
        tempoTotal = sum(sessao.tempo for sessao in sessoes)
        custoTotal = sum(sessao.custo for sessao in sessoes)

        maiorEnergia = max(sessao.energia for sessao in sessoes)
        menorEnergia = min(sessao.energia for sessao in sessoes)

        maiorCusto = max(sessao.custo for sessao in sessoes)
        menorCusto = min(sessao.custo for sessao in sessoes)

        print(f"Energia total carregada: {energiaTotal:.2f} kWh")
        print(f"Tempo total de carregamento: {tempoTotal:.2f} horas")
        print(f"Custo total das recargas: R$ {custoTotal:.2f}\n")

        print(f"Maior energia consumida em uma sessão: {maiorEnergia:.2f} kWh")
        print(f"Menor energia consumida em uma sessão: {menorEnergia:.2f} kWh")
        print(f"Maior custo de uma sessão: R$ {maiorCusto:.2f}")
        print(f"Menor custo de uma sessão: R$ {menorCusto:.2f}")

    else:
        print("Nenhuma sessão registrada ainda.\n")

    inserirLinha()

# ================================================================================
#                                   LOOP PRINCIPAL
# ================================================================================

cmndEsc = novaEntrada()

while True:

    if cmndEsc == 0:
        print("Saindo da Estação de Recarga!")
        inserirLinha()
        print()
        exit()

    elif cmndEsc == 1:
        cmndEsc01()

    elif cmndEsc == 2:
        cmndEsc02()

    elif cmndEsc == 3:
        cmndEsc03()

    elif cmndEsc == 4:
        cmndEsc04()

    elif cmndEsc == 5:
        cmndEsc05()

    cmndEsc = notNovaEntrada()
