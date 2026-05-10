// Variáveis
let preco_kwh = 1.97; // Preço do kWh em reais
let tarifa = 0.89; // Tarifa fixa em reais por sessão definida
let sessoes = []; // Array para armazenar as sessões de recarga
let sessaoAtual = null; // Variável para armazenar a sessão atual em andamento

// Função para iniciar a recarga
function iniciarRecarga() {
    let nome = document.getElementById("nome").value;
    let energia = parseFloat(document.getElementById("energia").value); // parseFloat serve para aceitar números decimais

    if (nome === "" || isNaN(energia)) { // Verifica se os campos estão preenchidos corretamente
        alert("Preencha todos os campos");
        return;
    }

    let total = (energia * preco_kwh) + tarifa; // Calcula o total da sessão com base na energia consumida e na tarifa fixa

    sessaoAtual = {
        nome: nome,
        energia: energia,
        total: total,
        inicio: new Date().toLocaleTimeString(), // Registra o horário de início da sessão
        fim: null,
        status: "Carregando"
    };

    document.getElementById("saida").innerHTML = // Exibe os detalhes da sessão atual
        "Sessão iniciada!<br>" +
        "<br>Usuário: " + nome + "<br>" +
        "Início: " + sessaoAtual.inicio + "<br>" +
        "Status: " + sessaoAtual.status;
}

// Função para encerrar a recarga
function encerrarRecarga() {
    if (sessaoAtual === null) {
        alert("Nenhuma sessão ativa.");
        return;
    }

    sessaoAtual.fim = new Date().toLocaleTimeString(); // Registra o horário de fim da sessão
    sessaoAtual.status = "Concluída";

    sessoes.push(sessaoAtual);

    document.getElementById("saida").innerHTML =
        "Sessão encerrada!<br>" +
        "<br>Usuário: " + sessaoAtual.nome + "<br>" +
        "Início: " + sessaoAtual.inicio + "<br>" +
        "Fim: " + sessaoAtual.fim + "<br>" +
        "Total: R$ " + sessaoAtual.total.toFixed(2);

    sessaoAtual = null;
}

// Função para mostrar histórico
function mostrarHistorico() {
    let saida = document.getElementById("saida");

    if (sessoes.length === 0) {
        saida.innerHTML = "<p>Nenhuma sessão registrada.</p>";
        return;
    }

    let tabela =
        "<table class='historico-table'>" +
        "<thead>" +
        "<tr>" +
        "<th>Usuário</th>" +
        "<th>Energia (kWh)</th>" +
        "<th>Total (R$)</th>" +
        "<th>Início</th>" +
        "<th>Fim</th>" +
        "<th>Status</th>" +
        "</tr>" +
        "</thead>" +
        "<tbody>";

    for (let i = 0; i < sessoes.length; i++) { // Itera sobre as sessões registradas para preencher a tabela
        tabela += // Adiciona uma linha para cada sessão, exibindo os detalhes de cada uma
            "<tr>" +
            "<td>" + sessoes[i].nome + "</td>" + // Exibe o nome do usuário
            "<td>" + sessoes[i].energia + "</td>" + // Exibe a energia consumida
            "<td>" + sessoes[i].total.toFixed(2) + "</td>" + // Exibe o total da sessão
            "<td>" + sessoes[i].inicio + "</td>" + // Exibe o horário de início da sessão
            "<td>" + (sessoes[i].fim ? sessoes[i].fim : "-") + "</td>" + // Exibe o horário de fim da sessão, senão mostra "-" se a sessão ainda não foi encerrada
            "<td>" + sessoes[i].status + "</td>" + // Exibe o status da sessão (Carregando ou Concluída)
            "</tr>";
    }

    tabela += "</tbody></table>";
    saida.innerHTML = tabela; // Exibe a tabela de histórico no elemento de saída
}