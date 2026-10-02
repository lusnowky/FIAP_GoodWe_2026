# ATENÇÃO! O CODIGO PRECISA DA IMPLEMENTAÇÃO DO RASPBERRY PI PICO
# ================================================================================
#                                    VARIÁVEIS
# ================================================================================

carros = []
comandosDisponiveis = [0, 1, 2, 3]

preco_kWh = 1.97
tarifa = 0.89

potenciaMax = 15 # Em kW

carregando = False
bloqueada = False
erro = False

# ================================================================================
#                                 CLASS INFOCARRO
# ================================================================================

class InfoCarro:
    def __init__(self, idCarro, apelido, dmndVeiculo, custo):
        self.idCarro = idCarro
        self.apelido = apelido
        self.dmndVeiculo = dmndVeiculo
        self.custo = custo
    
    def __repr__(self):
        return (f"\nID do veículo = {self.idCarro}"
                f"\nNome do veícuilo = {self.apelido}"
                f"\nEnergia Solicitada = {self.dmndVeiculo} kW\n")

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
[ 1 ] Adicionar novo veículo
[ 2 ] Listar carros
[ 3 ] Realizar recarga
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
#                                 ADD NOVO VEÍCULO
# ================================================================================

def cmndEsc01():

    idAtual =  len(carros) + 1
    
    print(f"""
Energia disponível: {potenciaMax} kW
Valor do Kwh: {preco_kWh} kWh
Valor da Tarifa: {tarifa}R$/kWh""")

    nomeVeiculo = str(input("Selecione um apelido para o veículo: "))
    dmndEngAtual = int(input("Quantidade de energia a ser carregada (em kW): "))

    custoAtual = dmndEngAtual * (preco_kWh + tarifa)

    carroAtual =  InfoCarro(
        idCarro = idAtual,
        apelido = nomeVeiculo,
        dmndVeiculo = dmndEngAtual,
        custo = custoAtual
    )

    carros.append(carroAtual)

    print("Veículo adicionado com sucesso!")
    inserirLinha()

# ================================================================================
#                                  LISTAR CARROS
# ================================================================================

def cmndEsc02():

    if len(carros) == 0:
        print("\nNenhum veículo registrado ainda.\n")
    else:
        print(carros)
    inserirLinha()


# ================================================================================
#                               REALIZAR RECARGA
# ================================================================================

def cmndEsc03():

    if len(carros) == 0:
        print("\nNenhum veículo foi registrado para realizar a recarga.\n")
    
    else:
        
        demandaTotal = sum(carro.enrgSolicitada for carro in carros)
        tempoTotal = demandaTotal / potenciaMax
        totalVeiculos = len(carros)
        totalCusto = sum(carro.custo for carro in carros)

        if demandaTotal <= potenciaMax:
        
            energiaPorcarro = round(potenciaMax / totalVeiculos, 2)

            print(f"""
Estatísticas da Recarga:

Energia disponível: {potenciaMax} kW
Demanda total de energia: {demandaTotal} kW
Valor total da recarga: R$ {totalCusto}
Total de veículos: {totalVeiculos}
Distribuição de energia por veículo: {energiaPorcarro} kW

Informações dos veículos:

{carros}
""")

            input("Pressione ENTER para prosseguir com a recarga...")
            print("Recarga concluída!")

        else:
            print(f"""
======================= !! AVISO !! =======================
A demanda total de energia excede a energia disponível!!
Energia total necessária para recarga ==> {demandaTotal} kW
Potência máxima disponível ==> {potenciaMax} kW
            
Ativando modo de carregamento dinâmico...""")
            input("Pressione ENTER para prosseguir com o carregamento...")

            fatorReducao = round(potenciaMax / demandaTotal, 2)

            
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

    cmndEsc = notNovaEntrada()
