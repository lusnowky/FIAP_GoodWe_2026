import sys
import time

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
                f"\nNome do veículo = {self.apelido}"
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
        for carro in carros:
            print(carro)
    inserirLinha()


# ================================================================================
#                               REALIZAR RECARGA
# ================================================================================

def cmndEsc03():
    global carregando, bloqueada, erro

    if len(carros) == 0:
        print("\nNenhum veículo foi registrado para realizar a recarga.\n")
    
    else:
        demandaTotal = sum(carro.dmndVeiculo for carro in carros)
        tempoTotal = demandaTotal / potenciaMax
        totalVeiculos = len(carros)
        totalCusto = sum(carro.custo for carro in carros)

        if demandaTotal <= potenciaMax:
            carregando = True
            bloqueada = False
            erro = False
        
            energiaPorcarro = round(demandaTotal / totalVeiculos, 2)

            print(f"""
Estatísticas da Recarga (Modo Normal):

Energia disponível: {potenciaMax} kW
Demanda total de energia: {demandaTotal} kW
Valor total da recarga: R$ {totalCusto:.2f}
Total de veículos: {totalVeiculos}
Distribuição de energia por veículo: {energiaPorcarro} kW

Informações dos veículos:
""")
            for carro in carros:
                print(f" -> {carro.apelido}: {carro.dmndVeiculo} kW")
            print()

            input("Pressione ENTER para prosseguir com a recarga...")
            print("Carregando...")
            time.sleep(1)
            print("Recarga concluída!")
            carregando = False

        else:
            carregando = True
            bloqueada = True
            erro = False

            print(f"""
======================= !! AVISO !! =======================
A demanda total de energia excede a energia disponível!!
Energia total necessária para recarga ==> {demandaTotal} kW
Potência máxima disponível ==> {potenciaMax} kW
            
Ativando modo de carregamento dinâmico...""")
            input("Pressione ENTER para prosseguir com o carregamento...")


            fatorReducao = potenciaMax / demandaTotal

            print("\nModulando e rebalanceando a potência dos carregadores:")
            for carro in carros:
                potenciaReduzida = round(carro.dmndVeiculo * fatorReducao, 2)
                print(f" -> Veículo [{carro.apelido}]: Limitado de {carro.dmndVeiculo} kW para {potenciaReduzida} kW")
            
            print(f"\nPotência total reajustada e estabilizada com segurança em: {potenciaMax} kW")
            print(f"Valor total a ser cobrado: R$ {totalCusto:.2f}\n")
            
            time.sleep(1)
            print("Carregamento dinâmico concluído com sucesso!")
            carregando = False
            bloqueada = False

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
        sys.exit()

    elif cmndEsc == 1:
        cmndEsc01()

    elif cmndEsc == 2:
        cmndEsc02()

    elif cmndEsc == 3:
        cmndEsc03()

    cmndEsc = notNovaEntrada()
