from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ================================================================================
#                                    VARIÁVEIS
# ================================================================================

sessoes = []      # lista de objetos Sessao (uma por carro)
historico = []    # lista de dicionários (uma por "Confirmar Recargas")

preco_kWh = 1.97
tarifa = 0.89
potencia = 7

# Tarifação dinâmica (Sprint 02)
LIMITE_CARROS = 3
LIMITE_KWH = 80
ADICIONAL_DINAMICO = 0.30

# ================================================================================
#                                   CLASS SESSÃO
# ================================================================================

class Sessao:
    def __init__(self, id, nome, modelo, energia, tempo, custo):
        self.id = id
        self.nome = nome
        self.modelo = modelo
        self.energia = energia
        self.tempo = tempo
        self.custo = custo

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
#                                  FUNÇÃO AUXILIAR
# ================================================================================

def formatarTempo(horasDecimais):
    horas = int(horasDecimais)
    minutos = round((horasDecimais - horas) * 60)
    return (f"{horas}h " if horas > 0 else "") + f"{minutos}min"

# Filtros usados nos templates (formato brasileiro: 1.234,56)
@app.template_filter("brl")
def brl(valor):
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.template_filter("num")
def num(valor):
    return f"{valor:.2f}".replace(".", ",")

@app.template_filter("tempo")
def tempo(horasDecimais):
    return formatarTempo(horasDecimais)

# ================================================================================
#                           PÁGINA INICIAL (quantos carros?)
# ================================================================================

@app.route("/")
def index():
    return render_template("index.html")

# ================================================================================
#                      NOVA SESSÃO DE RECARGA (formulário + cálculo)
# ================================================================================

@app.route("/recarga", methods=["GET", "POST"])
def recarga():

    # Quantidade de carros vem do formulário da página inicial (GET)
    # ou do campo escondido do formulário de recarga (POST)
    try:
        qntdCarros = int(request.values.get("qntd"))
    except (TypeError, ValueError):
        qntdCarros = 0

    if qntdCarros <= 0:
        return redirect("/")

    # GET -> só mostra os formulários
    if request.method == "GET":
        return render_template("recarga.html", qntd=qntdCarros)

    # POST -> valida, calcula e registra
    carros = []
    for i in range(1, qntdCarros + 1):
        nome = request.form.get(f"nome_{i}", "").strip()
        modelo = request.form.get(f"modelo_{i}", "").strip()
        try:
            energia = float(request.form.get(f"energia_{i}"))
        except (TypeError, ValueError):
            energia = 0

        if nome == "" or modelo == "" or energia <= 0:
            return render_template("recarga.html", qntd=qntdCarros,
                                   erro=f"Preencha todos os campos do Carro {i} corretamente.")

        carros.append({"nome": nome, "modelo": modelo, "energia": energia})

    totalKwh = sum(c["energia"] for c in carros)

    # Tarifação dinâmica
    motivos = []
    if qntdCarros > LIMITE_CARROS:
        motivos.append(f"mais de {LIMITE_CARROS} carros")
    if totalKwh > LIMITE_KWH:
        motivos.append(f"mais de {LIMITE_KWH} kWh na sessão")

    dinamica = len(motivos) > 0
    adicional = ADICIONAL_DINAMICO if dinamica else 0
    precoAtual = preco_kWh + tarifa + adicional

    # Previsão de tempo (carros em paralelo)
    tempoSessao = formatarTempo(totalKwh / (potencia * qntdCarros))

    # Cria uma Sessao para cada carro
    novas = []
    totalReais = 0
    log = [f"Sistema inicializado — {qntdCarros} ponto(s) de carga ativo(s)", ""]

    for i, c in enumerate(carros, start=1):
        idAtual = len(sessoes) + 1
        tempEstim = c["energia"] / potencia
        custoAtual = c["energia"] * precoAtual

        sessao = Sessao(idAtual, c["nome"], c["modelo"], c["energia"], tempEstim, custoAtual)
        sessoes.append(sessao)
        novas.append(sessao)
        totalReais += custoAtual

        log.append(f"Carro {i} conectado (sessão {idAtual})")
        log.append(f"{c['nome']} | {c['modelo']} | {num(c['energia'])} kWh | Valor: {brl(custoAtual)}")
        log.append(f"Sessão encerrada para Carro {i}")
        log.append("")

    historico.append({
        "qntdCarros": qntdCarros,
        "totalKwh": totalKwh,
        "totalReais": totalReais,
        "dinamica": "Sim" if dinamica else "Não"
    })

    resumo = {
        "dinamica": dinamica,
        "motivo": " e ".join(motivos),
        "precoBase": preco_kWh + tarifa,
        "adicional": adicional,
        "precoAtual": precoAtual,
        "tempoSessao": tempoSessao,
        "totalReais": totalReais
    }

    return render_template("recarga.html", qntd=qntdCarros, resumo=resumo,
                           novas=novas, log=log, historico=historico,
                           potencia=potencia)

# ================================================================================
#        SESSÕES: LISTAR, BUSCAR, ORDENAR E ESTATÍSTICAS (tudo em /sessoes)
# ================================================================================

@app.route("/sessoes")
def listar():

    lista = sessoes[:]      # cópia, para a ordenação não bagunçar a lista original
    titulo = "Sessões (ordem de registro)"

    # ---- Ordenar ----
    criterio = request.args.get("ordenar")

    if criterio == "id":
        lista = bubbleSortID(lista)
        titulo = "Sessões ordenadas por ID"
    elif criterio == "energia":
        lista = bubbleSortEnergia(lista)
        titulo = "Sessões ordenadas por Energia"
    elif criterio == "tempo":
        lista = bubbleSortTempo(lista)
        titulo = "Sessões ordenadas por Tempo"
    elif criterio == "custo":
        lista = bubbleSortCusto(lista)
        titulo = "Sessões ordenadas por Custo"

    # ---- Buscar ----
    busca = None
    idBusca = request.args.get("buscar")

    if idBusca:
        try:
            posicao = busca_sequencial(sessoes, int(idBusca))
        except ValueError:
            posicao = -1

        if posicao != -1:
            busca = {"encontrada": True, "sessao": sessoes[posicao]}
        else:
            busca = {"encontrada": False}

    # ---- Estatísticas ----
    stats = None
    if len(sessoes) > 0:
        stats = {
            "total": len(sessoes),
            "energiaTotal": sum(s.energia for s in sessoes),
            "tempoTotal": sum(s.tempo for s in sessoes),
            "custoTotal": sum(s.custo for s in sessoes),
            "maiorEnergia": max(s.energia for s in sessoes),
            "menorEnergia": min(s.energia for s in sessoes),
            "maiorCusto": max(s.custo for s in sessoes),
            "menorCusto": min(s.custo for s in sessoes)
        }

    return render_template("sessoes.html", lista=lista, titulo=titulo, criterio=criterio,
                           busca=busca, stats=stats, historico=historico)

if __name__ == "__main__":
    app.run(debug=True)
