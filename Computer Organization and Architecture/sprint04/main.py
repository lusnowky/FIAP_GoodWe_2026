from machine import Pin,I2C  # type: ignore[import-not-found]
from time import sleep
from liquid_crystal_pico import LiquidCrystalPico   # type: ignore[import-not-found]
import sys
import time

try:
    from gpio_lcd import GpioLcd    # type: ignore[import-not-found]
except ImportError:
    pass


# ================================
# CONFIGURAÇÃO DOS LEDs
# ================================

ledVerde = Pin(2, Pin.OUT)
ledAmarelo = Pin(3, Pin.OUT)
ledVermelho = Pin(4, Pin.OUT)

ledVerde.value(0)
ledAmarelo.value(0)
ledVermelho.value(0)

def apagarLeds():
    ledVerde.value(0)
    ledAmarelo.value(0)
    ledVermelho.value(0)

# ================================
# MAPEAMENTO LCD
# ================================

lcd = GpioLcd(
    rs_pin=Pin(12),      # GP12
    enable_pin=Pin(13),  # GP13
    d4_pin=Pin(16),      # GP16
    d5_pin=Pin(17),      # GP17
    d6_pin=Pin(18),      # GP18
    d7_pin=Pin(19),      # GP19
    num_lines=2,
    num_columns=16
)

# ================================================================================
#                                    VARIÁVEIS
# ================================================================================

carros = []
comandosDisponiveis = [1, 2, 3, 4, 5]

preco_kWh = 1.97
tarifa = 0.89

potenciaMax = 8 # Em kW (energia disponível - pode ser alterada pelo comando 4)

carregando = False
bloqueada = False
erro = False

# ================================================================================
#                                 CLASS INFOCARRO
# ================================================================================

class InfoCarro:
    def __init__(self, idCarro, apelido, bateria, dmndVeiculo, custo):
        self.idCarro = idCarro
        self.apelido = apelido
        self.bateria = bateria            # em %
        self.dmndVeiculo = dmndVeiculo
        self.custo = custo
        self.estado = "AGUARDANDO"        # ATIVA, REDUZIDA ou ESPERA
    
    def __repr__(self):
        return (f"\nID do veículo = {self.idCarro}"
                f"\nNome do veículo = {self.apelido}"
                f"\nBateria = {self.bateria}%"
                f"\nEnergia Solicitada = {self.dmndVeiculo} kW"
                f"\nEstado da recarga = {self.estado}\n")


carros.append(InfoCarro(1, "EV1", 45, 2, 2 * (preco_kWh + tarifa)))
carros.append(InfoCarro(2, "EV2", 20, 2.5, 2.5 * (preco_kWh + tarifa)))
carros.append(InfoCarro(3, "EV3", 70, 3, 3 * (preco_kWh + tarifa)))

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
[ 1 ] Adicionar novo veículo
[ 2 ] Listar carros
[ 3 ] Realizar recarga
[ 4 ] Definir energia disponível
[ 5 ] Representação de dados
""")

# ================================================================================
#                                  ENTRADAS
# ================================================================================

def lerInteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Valor inválido! Digite apenas números inteiros.")

def lerNumero(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Valor inválido! Digite apenas números (ex.: 2.5).")


def statusAguardando():
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("STATUS:")
    lcd.move_to(0, 1)
    lcd.putstr(f"Aguardando...")


def novaEntrada():
    comandoAtual = None
    
    statusAguardando()

    if comandoAtual is None:
        msgBemVindo()
        msgComandos()
        comandoAtual = lerInteiro("Insira o comando desejado: ")

        while comandoAtual not in comandosDisponiveis:
            comandoAtual = lerInteiro("Comando Inválido! Tente novamente: ")
        inserirLinha()

    return comandoAtual

def notNovaEntrada():
    input("Pressione ENTER para continuar...")
    inserirLinha()

    print("\nSelecione um novo comando:")
    msgComandos()

    statusAguardando()

    comandoAtual = lerInteiro("Insira o comando desejado: ")

    while comandoAtual not in comandosDisponiveis:
        comandoAtual = lerInteiro("Comando Inválido! Tente novamente: ")
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

    bateriaAtual = lerInteiro("Nível atual da bateria (0 a 100%): ")
    while bateriaAtual < 0 or bateriaAtual > 100:
        bateriaAtual = lerInteiro("Valor inválido! Digite de 0 a 100: ")

    dmndEngAtual = lerNumero("Quantidade de energia a ser carregada (em kW): ")
    while dmndEngAtual <= 0:
        dmndEngAtual = lerNumero("Valor inválido! Digite um valor maior que 0: ")

    custoAtual = dmndEngAtual * (preco_kWh + tarifa)

    carroAtual =  InfoCarro(
        idCarro = idAtual,
        apelido = nomeVeiculo,
        bateria = bateriaAtual,
        dmndVeiculo = dmndEngAtual,
        custo = custoAtual
    )

    carros.append(carroAtual)

    print("Veículo adicionado com sucesso!")
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("VEICULO")
    lcd.move_to(0, 1)
    lcd.putstr("ADICIONADO!")
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


def pegarBateria(carro):
    return carro.bateria

def cmndEsc03():
    global carregando, bloqueada, erro

    apagarLeds()   

    if len(carros) == 0:
        print("\nNenhum veículo foi registrado para realizar a recarga.\n")
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("SEM VEICULOS")
        lcd.move_to(0, 1)
        lcd.putstr("REGISTRADOS!")
    
    else:
        demandaTotal = sum(carro.dmndVeiculo for carro in carros)
        totalVeiculos = len(carros)
        totalCusto = sum(carro.custo for carro in carros)

        # ------------------ SITUAÇÃO 1: ENERGIA SUFICIENTE ------------------
        if demandaTotal <= potenciaMax:

            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(f"{len(carros)} VEICULOS")
            lcd.move_to(0, 1)
            lcd.putstr("DETECTADOS")

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
                carro.estado = "ATIVA"   
                print(f" -> {carro.apelido} ({carro.bateria}%): {carro.dmndVeiculo} kW - {carro.estado}")  
            print()

            input("Pressione ENTER para prosseguir com a recarga...")
            lcd.clear()
            lcd.move_to(0, 0)
            print("Carregando...")
            ledVerde.value(1)
            print("LED VERDE ACESO - RECARGA ATIVA")   
            time.sleep(5)
            print("Recarga concluída!")
            print("Status da estação: RECARGA ATIVA")   
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("RECARGA")          
            lcd.move_to(0, 1)
            lcd.putstr("ATIVA")
            carregando = False

        # ------------------ ENERGIA INSUFICIENTE ------------------
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

            # ------------- SITUAÇÃO 2: DISPONIBILIDADE LIMITADA -------------
            # (todos recebem pelo menos 50% do que pediram)
            if fatorReducao >= 0.5:

                print("\nModulando e rebalanceando a potência dos carregadores:")
                for carro in carros:
                    potenciaReduzida = round(carro.dmndVeiculo * fatorReducao, 2)
                    carro.estado = "REDUZIDA"
                    print(f" -> Veículo [{carro.apelido}]: Limitado de {carro.dmndVeiculo} kW para {potenciaReduzida} kW")
                
                print(f"\nPotência total reajustada e estabilizada com segurança em: {potenciaMax} kW")
                print(f"Valor total a ser cobrado: R$ {totalCusto:.2f}\n")

                ledAmarelo.value(1)
                print("LED AMARELO ACESO - RECARGA CONTROLADA")
                print("Status da estação: RECARGA CONTROLADA")   
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("RECARGA")
                lcd.move_to(0, 1)
                lcd.putstr("CONTROLADA")

            # ------------- SITUAÇÃO 3: BAIXA DISPONIBILIDADE -------------
            # Prioridade para quem tem MENOS bateria. Quem não conseguir pelo
            # menos 50% do que pediu fica em espera.
            else:

                print("\nEnergia muito baixa! Prioridade para os veículos com menor bateria:")
                restante = potenciaMax
                for carro in sorted(carros, key=pegarBateria):
                    minimo = carro.dmndVeiculo / 2

                    if restante > 0 and restante >= minimo:
                        if restante >= carro.dmndVeiculo:
                            potencia = carro.dmndVeiculo
                            carro.estado = "ATIVA"
                            ledVerde.value(1)
                            print("LED VERDE ACESO")
                        else:
                            potencia = restante
                            carro.estado = "REDUZIDA"
                            ledAmarelo.value(1)
                            print("LED AMARELO ACESO")
                        restante = restante - potencia
                        print(f" -> Veículo [{carro.apelido}] ({carro.bateria}%): {potencia} kW - {carro.estado}")
                    else:
                        carro.estado = "ESPERA"
                        ledVermelho.value(1)
                        print("LED VERMELHO ACESO")
                        print(f" -> Veículo [{carro.apelido}] ({carro.bateria}%): 0 kW - EM ESPERA")

                print(f"\nPotência total utilizada: {potenciaMax - restante} kW de {potenciaMax} kW\n")
                print("Status da estação: RECARGA LIMITADA")   

                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("RECARGA")
                lcd.move_to(0, 1)
                lcd.putstr("LIMITADA")
            
            time.sleep(1)
            print("Carregamento dinâmico concluído com sucesso!")
            carregando = False
            bloqueada = False

    inserirLinha()


# ================================================================================
#                              DEFINIR ENERGIA DISPONÍVEL
# ================================================================================

def cmndEsc04():
    global potenciaMax

    print(f"""
Energia disponível atual: {potenciaMax} kW

[ 1 ] Alta disponibilidade (8 kW)
[ 2 ] Disponibilidade limitada (5 kW)
[ 3 ] Baixa disponibilidade (2 kW)
[ 4 ] Digitar outro valor
""")

    opcao = lerInteiro("Escolha uma opção: ")
    while opcao < 1 or opcao > 4:
        opcao = lerInteiro("Opção inválida! Escolha de 1 a 4: ")

    if opcao == 1:
        potenciaMax = 8
    elif opcao == 2:
        potenciaMax = 5
    elif opcao == 3:
        potenciaMax = 2
    else:
        potenciaMax = lerNumero("Digite a energia disponível (em kW): ")
        while potenciaMax < 0:
            potenciaMax = lerNumero("Valor inválido! Digite um valor maior ou igual a 0: ")

    print(f"\nEnergia disponível atualizada para {potenciaMax} kW")
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("ENERGIA ALTERADA")
    lcd.move_to(0, 1)
    lcd.putstr(f"{potenciaMax} kW")
    inserirLinha()


# ================================================================================
#                            REPRESENTAÇÃO DE DADOS
# ================================================================================

def cmndEsc05():
    energiaW = int(potenciaMax * 1000)   # converte kW para W (número inteiro)

    print(f"""
Energia disponível: {energiaW} W

Decimal:      {energiaW}
Hexadecimal:  {hex(energiaW)}
Binário:      {bin(energiaW)[2:]}
""")

    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(f"HEX {hex(energiaW)}")
    lcd.move_to(0, 1)
    lcd.putstr(bin(energiaW)[2:])
    inserirLinha()


# ================================================================================
#                                   LOOP PRINCIPAL
# ================================================================================


cmndEsc = novaEntrada()

while True:

    if cmndEsc == 1:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("ADICIONANDO NOVO")
        lcd.move_to(0, 1)
        lcd.putstr("VEICULO...")
        cmndEsc01()

    elif cmndEsc == 2:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("LISTANDO")
        lcd.move_to(0, 1)
        lcd.putstr("VEICULOS...")
        cmndEsc02()

    elif cmndEsc == 3:
        cmndEsc03()

    elif cmndEsc == 4:
        cmndEsc04()

    elif cmndEsc == 5:
        cmndEsc05()

    cmndEsc = notNovaEntrada()