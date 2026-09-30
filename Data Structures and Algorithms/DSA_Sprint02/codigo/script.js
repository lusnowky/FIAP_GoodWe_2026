// Variáveis globais
let preco_kwh = 1.97;
let tarifa    = 0.89;
let potencia_carregador = 7; // kW por carro 

// Limites para tarifação dinâmica
let LIMITE_CARROS = 3;   // acima disso → tarifa extra
let LIMITE_KWH    = 80;  // acima disso → tarifa extra
let ADICIONAL_DINAMICO = 0.30; // R$/kWh extra quando dispara

// Histórico de sessões (array de objetos)
let historico = [];

// Lê a quantidade de carros salva na página anterior
let qntdCarros = parseInt(localStorage.getItem("qntdCarros"));

if (!qntdCarros || qntdCarros <= 0) {
    alert("Acesse pelo menu inicial.");
    window.location.href = "index.html";
}

// Gera os formulários dinamicamente
let container = document.getElementById("formularios");

for (let i = 1; i <= qntdCarros; i++) {
    container.innerHTML +=
        "<h3>Carro " + i + "</h3>" +
        "<input type='text'   id='nome_"    + i + "' placeholder='Nome do motorista'> " +
        "<input type='text'   id='modelo_"  + i + "' placeholder='Modelo do carro'> " +
        "<input type='number' id='energia_" + i + "' placeholder='Energia (kWh)'> <br><br>";
}

// Função principal para iniciar as recargas
function iniciarRecargas() {
    let saida = document.getElementById("saida");
    let totalGeralKwh = 0;
    let totalGeralReais = 0;
    let resultado = "";
    let log = "";
    let carros = []; // guarda os dados de cada carro para o histórico

    // 1ª passagem: coleta e valida os campos
    for (let i = 1; i <= qntdCarros; i++) {
        let nome   = document.getElementById("nome_"    + i).value;
        let modelo = document.getElementById("modelo_"  + i).value;
        let energia = parseFloat(document.getElementById("energia_" + i).value);

        if (nome === "" || modelo === "" || isNaN(energia) || energia <= 0) {
            alert("Preencha todos os campos do Carro " + i + " corretamente.");
            return;
        }

        totalGeralKwh += energia;
        carros.push({ nome: nome, modelo: modelo, energia: energia });
    }

    // Tarifação 
    let tarifaDinamica = false;
    let preco_atual = preco_kwh;
    let motivo = "";

    if (qntdCarros > LIMITE_CARROS) {
        tarifaDinamica = true;
        motivo += "mais de " + LIMITE_CARROS + " carros";
    }
    if (totalGeralKwh > LIMITE_KWH) {
        tarifaDinamica = true;
        motivo += (motivo !== "" ? " e " : "") + "mais de " + LIMITE_KWH + " kWh na sessão";
    }

    if (tarifaDinamica) {
        preco_atual = preco_kwh + ADICIONAL_DINAMICO;
        resultado += "<p style='color:#f0a04a;'><strong>⚡ Tarifação dinâmica aplicada</strong> (" + motivo + ")<br>" +
                     "Preço ajustado: R$ " + preco_kwh.toFixed(2) + " + R$ " + ADICIONAL_DINAMICO.toFixed(2) + " = R$ " + preco_atual.toFixed(2) + "/kWh</p>";
    }

    // ── Controle de demanda — previsão de tempo ─────────
    // Carros carregam em paralelo, mas quanto mais carros, maior a disputa de potência
    // Fórmula: tempo = energiaTotal / (potencia_carregador * qntdCarros) — em horas
    let tempoPrevisto = totalGeralKwh / (potencia_carregador * qntdCarros); // horas
    let horas   = Math.floor(tempoPrevisto);
    let minutos = Math.round((tempoPrevisto - horas) * 60);
    let tempoStr = (horas > 0 ? horas + "h " : "") + minutos + "min";

    resultado += "<p><strong>Previsão de tempo da sessão: " + tempoStr + "</strong><br>" +
                 "<small style='color:#8891a8;'>Base: " + potencia_carregador + " kW por carro, " + qntdCarros + " carro(s) em paralelo</small></p>";

    // Aviso de alta demanda
    if (qntdCarros > LIMITE_CARROS || totalGeralKwh > LIMITE_KWH) {
        resultado += "<p style='color:#f06060;'> Alta demanda detectada — o tempo de recarga pode ser maior que o previsto.</p>";
    }

    resultado += "<hr style='border-color:#2a2f42; margin:16px 0;'>";

    // 2ª passagem: calcula o total de cada carro e monta o resultado final
    let horarioInicio = new Date().toLocaleTimeString();

    for (let i = 0; i < carros.length; i++) {
        let total = (carros[i].energia * preco_atual) + tarifa;
        totalGeralReais += total;

        // Tempo individual estimado (proporção de energia do carro)
        let tempoIndividual = carros[i].energia / potencia_carregador; // horas
        let hInd = Math.floor(tempoIndividual);
        let mInd = Math.round((tempoIndividual - hInd) * 60);
        let tempoIndStr = (hInd > 0 ? hInd + "h " : "") + mInd + "min";

        resultado +=
            "<p><strong>Carro " + (i+1) + " — " + carros[i].nome + " (" + carros[i].modelo + ")</strong><br>" +
            "Energia: " + carros[i].energia.toFixed(2) + " kWh | " +
            "Tempo est.: " + tempoIndStr + " | " +
            "Total: R$ " + total.toFixed(2) + "</p>";

        // Log simulado para cada carro
        log +=
            "Carro " + (i+1) + " conectado<br>" +
            carros[i].nome + " | " + carros[i].modelo + " | " + carros[i].energia.toFixed(2) + " kWh<br>" +
            "Energia solicitada: " + carros[i].energia.toFixed(2) + " kWh | Valor: R$ " + total.toFixed(2) + "<br>" +
            "Sessão encerrada para Carro " + (i+1) + "<br><br>";
    }

    resultado += "<p><strong>Total geral: R$ " + totalGeralReais.toFixed(2) + "</strong></p>";

    // Registra no histórico
    historico.push({
        horario:    horarioInicio,
        qntdCarros: qntdCarros,
        totalKwh:   totalGeralKwh,
        totalReais: totalGeralReais,
        dinamica:   tarifaDinamica ? "Sim" : "Não"
    });

    // Monta a saída final
    saida.innerHTML =
        "<h3>Resumo da Sessão</h3>" +
        resultado +

        // Log
        "<h3>Log</h3>" +
        "<div class='log'>" +
        "Sistema inicializado — " + qntdCarros + " ponto(s) de carga ativo(s)<br><br>" +
        log +
        "Sessão registrada às " + horarioInicio +
        "</div>" +

        // Histórico
        "<br> <br> <h3>Histórico de Sessões</h3>" +
        montarTabelaHistorico();

    saida.scrollIntoView({ behavior: "smooth" });
}

// Função para montar a tabela do histórico
function montarTabelaHistorico() {
    if (historico.length === 0) {
        return "<p>Nenhuma sessão registrada ainda.</p>";
    }

    let tabela =
        "<table class='historico-table'>" +
        "<thead><tr>" +
        "<th>Horário</th>" +
        "<th>Carros</th>" +
        "<th>Total kWh</th>" +
        "<th>Total R$</th>" +
        "<th>Tarifa Dinâmica</th>" +
        "</tr></thead><tbody>";

    for (let i = 0; i < historico.length; i++) {
        tabela +=
            "<tr>" +
            "<td>" + historico[i].horario    + "</td>" +
            "<td>" + historico[i].qntdCarros + "</td>" +
            "<td>" + historico[i].totalKwh   + "</td>" +
            "<td>R$ " + historico[i].totalReais.toFixed(2) + "</td>" +
            "<td>" + historico[i].dinamica   + "</td>" +
            "</tr>";
    }

    tabela += "</tbody></table>";
    return tabela;
}