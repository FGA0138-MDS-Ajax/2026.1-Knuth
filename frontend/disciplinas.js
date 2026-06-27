document.addEventListener("DOMContentLoaded", () => {
    const btnSair = document.getElementById("btnSair");
    if (btnSair) {
        btnSair.addEventListener("click", () => window.location.href = "login.html");
    }
});

// Banco de dados simulado com TODAS as disciplinas do sistema
const bancoGlobalDisciplinas = [
    { nome: "MDS", desc: "Desenvolvimento de Software" },
    { nome: "Estrutura de Dados", desc: "Listas, Pilhas e Filas" },
    { nome: "Banco de Dados", desc: "SQL e Modelagem" },
    { nome: "Cálculo 1", desc: "Limites, Derivadas e Integrais" },
    { nome: "Sistemas Digitais", desc: "Portas lógicas e circuitos combinacionais" },
    { nome: "Física 1", desc: "Mecânica Clássica e Cinemática" }
];

function filtrarDisciplinas() {
    let input = document.getElementById("pesquisa").value.toLowerCase().trim();
    let container = document.querySelector(".cards");
    let mensagem = document.getElementById("mensagem-sem-resultados");

    // Se a busca estiver vazia, exibe apenas as 3 disciplinas padrões do usuário
    if (input === "") {
        mensagem.style.display = "none";
        mostrarDisciplinasPadrao();
        return;
    }

    // Procura o termo digitado no banco global de disciplinas
    let resultados = bancoGlobalDisciplinas.filter(disciplina => 
        disciplina.nome.toLowerCase().includes(input) || 
        disciplina.desc.toLowerCase().includes(input)
    );

    // Limpa a tela para colocar os resultados da busca
    container.innerHTML = "";

    if (resultados.length > 0) {
        mensagem.style.display = "none";
        
        // Cria os cards dinamicamente na tela para cada resultado encontrado
        resultados.forEach(disciplina => {
            container.innerHTML += `
                <div class="card disciplina">
                    <h2>${disciplina.nome}</h2>
                    <p>${disciplina.desc}</p>
                    <span>Fórum geral da disciplina</span>
                    <button onclick="window.location.href='disciplina-detalhe.html'">Acessar Fórum</button>
                </div>
            `;
        });
    } else {
        // Se não achar nada no banco global, mostra a mensagem de erro
        mensagem.style.display = "block";
    }
}

// Função para renderizar a visão inicial (apenas as matriculadas)
function mostrarDisciplinasPadrao() {
    let container = document.querySelector(".cards");
    container.innerHTML = `
        <div class="card disciplina">
            <h2>MDS</h2>
            <p>Desenvolvimento de Software</p>
            <span>Fórum geral da disciplina</span>
            <button onclick="window.location.href='disciplina-detalhe.html'">Acessar Fórum</button>
        </div>
        <div class="card disciplina">
            <h2>Estrutura de Dados</h2>
            <p>Listas, Pilhas e Filas</p>
            <span>Fórum geral da disciplina</span>
            <button onclick="window.location.href='disciplina-detalhe.html'">Acessar Fórum</button>
        </div>
        <div class="card disciplina">
            <h2>Banco de Dados</h2>
            <p>SQL e Modelagem</p>
            <span>Fórum geral da disciplina</span>
            <button onclick="window.location.href='disciplina-detalhe.html'">Acessar Fórum</button>
        </div>
    `;
}