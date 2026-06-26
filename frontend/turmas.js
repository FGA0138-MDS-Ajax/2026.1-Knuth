const turmas = [
    "mds",
    "estrutura de dados",
    "banco de dados"
];

// Elementos dos Modais
const modalCriar = document.getElementById("modalCriar");
const modalEntrar = document.getElementById("modalEntrar");

// Botões para Abrir Modais
const btnNovaTurma = document.getElementById("novaTurma");
const btnEntrarCodigo = document.getElementById("btnEntrarCodigo");

// Botões para Fechar Modais
const btnCancelarCriar = document.getElementById("btnCancelarCriar");
const btnCancelarEntrar = document.getElementById("btnCancelarEntrar");

// Botões de Confirmação
const btnConfirmarCriar = document.getElementById("btnConfirmarCriar");
const btnConfirmarEntrar = document.getElementById("btnConfirmarEntrar");

// Ações: Abrir Modais
btnNovaTurma.addEventListener("click", () => {
    modalCriar.classList.remove("oculta");
});

btnEntrarCodigo.addEventListener("click", () => {
    modalEntrar.classList.remove("oculta");
});

// Ações: Fechar Modais
btnCancelarCriar.addEventListener("click", () => {
    modalCriar.classList.add("oculta");
});

btnCancelarEntrar.addEventListener("click", () => {
    modalEntrar.classList.add("oculta");
});

// Ação: Confirmar Criação de Turma
btnConfirmarCriar.addEventListener("click", () => {
    const nome = document.getElementById("inputNomeTurma").value.trim();
    const disciplina = document.getElementById("inputDisciplina").value.trim();

    if (!nome || !disciplina) {
        alert("Preencha todos os campos para criar a turma.");
        return;
    }

    alert(`Turma "${nome}" vinculada à disciplina "${disciplina}" criada com sucesso!`);
    modalCriar.classList.add("oculta");
    
    // Limpa os campos depois de criar
    document.getElementById("inputNomeTurma").value = "";
    document.getElementById("inputDisciplina").value = "";
});

// Ação: Confirmar Entrada com Código
btnConfirmarEntrar.addEventListener("click", () => {
    const codigo = document.getElementById("inputCodigoAcesso").value.trim();

    if (!codigo) {
        alert("Digite o código de acesso.");
        return;
    }

    alert(`Entrando na turma com o código: ${codigo}`);
    modalEntrar.classList.add("oculta");
    
    // Limpa o campo
    document.getElementById("inputCodigoAcesso").value = "";
});

// Ação: Busca
document.getElementById("buscarTurma").addEventListener("click", () => {
    const busca = document.getElementById("buscaTurma").value.toLowerCase().trim();
    const mensagem = document.getElementById("mensagemErro");

    if (busca === "") {
        mensagem.textContent = "Digite o nome de uma turma.";
        mensagem.style.color = "red";
        return;
    }

    if (!turmas.includes(busca)) {
        mensagem.textContent = "Turma não encontrada.";
        mensagem.style.color = "red";
        return;
    }

    mensagem.textContent = "Turma encontrada!";
    mensagem.style.color = "green";
});
document.addEventListener("DOMContentLoaded", () => {
    const containerTurmas = document.querySelector(".cards");
    
    if (containerTurmas) {
        // Varre o localStorage procurando inscrições
        for (let i = 0; i < localStorage.length; i++) {
            let key = localStorage.key(i);
            
            if (key.startsWith("inscrito_")) {
                let infoMateria = JSON.parse(localStorage.getItem(key));
                let idMateria = key.replace("inscrito_", "");
                
                // Cria o card da nova turma na tela
                let novaTurmaHTML = `
                    <div class="card turma">
                        <h2>${infoMateria.nome.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, '').trim()}</h2>
                        <p>Turma Nova | Professor(a) a definir</p>
                        <span>Código: ${idMateria.toUpperCase()}-2026</span>
                        <button onclick="window.location.href='turma-detalhe.html'">Entrar na Turma</button>
                    </div>
                `;
                
                containerTurmas.insertAdjacentHTML("beforeend", novaTurmaHTML);
            }
        }
    }
});