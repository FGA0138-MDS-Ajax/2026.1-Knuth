const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "login.html";
}

const containerTurmas = document.getElementById("containerTurmas");
const tituloTurmas = document.getElementById("tituloTurmas");
const mensagemErro = document.getElementById("mensagemErro");

// Botões e Modais
const btnNovaTurma = document.getElementById("novaTurma");
const btnEntrarCodigo = document.getElementById("btnEntrarCodigo");
const modalCriar = document.getElementById("modalCriar");
const modalEntrar = document.getElementById("modalEntrar");

const btnCancelarCriar = document.getElementById("btnCancelarCriar");
const btnCancelarEntrar = document.getElementById("btnCancelarEntrar");

const btnConfirmarCriar = document.getElementById("btnConfirmarCriar");
const btnConfirmarEntrar = document.getElementById("btnConfirmarEntrar");

const selectDisciplina = document.getElementById("selectDisciplina");

let todasTurmas = [];

function authHeader() {
    return { "Authorization": `Bearer ${token}` };
}

function jsonAuthHeaders() {
    return {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
    };
}

// Configura o painel baseado nas permissões do usuário
function configurarAcesso() {
    const role = getLoggedUserRole();
    if (role === "aluno") {
        if (btnNovaTurma) btnNovaTurma.style.display = "none";
    } else if (role === "professor") {
        if (btnEntrarCodigo) btnEntrarCodigo.style.display = "none";
    }
}

// Carrega as turmas do servidor
async function carregarTurmas() {
    try {
        const res = await fetch(`${API_BASE_URL}/turmas/minhas_turmas`, {
            headers: authHeader()
        });
        if (res.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }
        if (!res.ok) {
            containerTurmas.innerHTML = `<p style="color:#ef4444; text-align:center;">Erro ao carregar turmas.</p>`;
            return;
        }
        todasTurmas = await res.json();
        renderizarTurmas(todasTurmas);
    } catch (e) {
        console.error("Falha ao buscar turmas:", e);
        containerTurmas.innerHTML = `<p style="color:#ef4444; text-align:center;">Erro de conexão com o servidor.</p>`;
    }
}

// Renderiza os cards das turmas na tela
function renderizarTurmas(lista) {
    if (lista.length === 0) {
        containerTurmas.innerHTML = `<p style="color:#666; text-align:center; padding: 20px;">Você não está em nenhuma turma no momento.</p>`;
        tituloTurmas.textContent = "📚 Minhas Turmas (0)";
        return;
    }
    
    tituloTurmas.textContent = `📚 Minhas Turmas (${lista.length})`;
    containerTurmas.innerHTML = "";
    
    lista.forEach(t => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <h3>💻 ${t.descricao}</h3>
            <p><strong>Disciplina:</strong> ${t.disciplina?.nome || "Geral"}</p>
            <p><strong>👨‍🏫 Professor:</strong> ${t.professor?.nome || "A definir"}</p>
            <p><strong>Horário:</strong> ${t.horario}</p>
            <p><strong>Período:</strong> ${t.periodo}</p>
            <p style="font-size:12px;color:#888;">Código de Acesso: ${t.codigo_acesso}</p>
            <button class="entrar" onclick="window.location.href='turma-detalhe.html?id=${t.id}'">
                Acessar
            </button>
        `;
        containerTurmas.appendChild(card);
    });
}

// Carrega as disciplinas disponíveis no modal de criação
async function carregarDisciplinasSelect() {
    try {
        const res = await fetch(`${API_BASE_URL}/disciplinas/`, {
            headers: authHeader()
        });
        if (res.ok) {
            const disc = await res.json();
            selectDisciplina.innerHTML = '<option value="">Selecione a Disciplina...</option>';
            disc.forEach(d => {
                const option = document.createElement("option");
                option.value = d.id;
                option.textContent = d.nome;
                selectDisciplina.appendChild(option);
            });
        }
    } catch (e) {
        console.error("Erro ao carregar disciplinas para o select:", e);
    }
}

// Abrir e fechar Modais
if (btnNovaTurma) {
    btnNovaTurma.addEventListener("click", () => {
        carregarDisciplinasSelect();
        modalCriar.classList.remove("oculta");
    });
}

if (btnEntrarCodigo) {
    btnEntrarCodigo.addEventListener("click", () => {
        modalEntrar.classList.remove("oculta");
    });
}

btnCancelarCriar.addEventListener("click", () => modalCriar.classList.add("oculta"));
btnCancelarEntrar.addEventListener("click", () => modalEntrar.classList.add("oculta"));

// Confirmar Criar Turma (Professor)
btnConfirmarCriar.addEventListener("click", async () => {
    const nome = document.getElementById("inputNomeTurma").value.trim();
    const disciplinaId = parseInt(selectDisciplina.value);
    const horario = document.getElementById("inputHorario").value.trim();
    const periodo = document.getElementById("inputPeriodo").value.trim();
    
    if (!nome || !disciplinaId || !horario || !periodo) {
        alert("Preencha todos os campos para criar a turma.");
        return;
    }
    
    const profile = JSON.parse(localStorage.getItem("user_profile_cache") || "{}");
    const professorId = profile.professor_id;
    
    if (!professorId) {
        alert("Erro: ID do professor não encontrado no perfil.");
        return;
    }
    
    // Gera código de acesso aleatório de 6 caracteres
    const cod = Math.random().toString(36).substring(2, 8).toUpperCase();
    
    try {
        const res = await fetch(`${API_BASE_URL}/turmas/`, {
            method: "POST",
            headers: jsonAuthHeaders(),
            body: JSON.stringify({
                descricao: nome,
                horario,
                periodo,
                disciplina_id: disciplinaId,
                professor_id: professorId,
                codigo_acesso: cod
            })
        });
        
        if (res.ok) {
            alert(`Turma criada com sucesso! Código de acesso: ${cod}`);
            modalCriar.classList.add("oculta");
            // Limpa campos
            document.getElementById("inputNomeTurma").value = "";
            document.getElementById("inputHorario").value = "";
            selectDisciplina.value = "";
            carregarTurmas();
        } else {
            const err = await res.json();
            alert(err.detail || "Erro ao criar turma.");
        }
    } catch (e) {
        alert("Falha ao comunicar com o servidor.");
    }
});

// Confirmar Entrar em Turma via Código (Aluno)
btnConfirmarEntrar.addEventListener("click", async () => {
    const codigo = document.getElementById("inputCodigoAcesso").value.trim().toUpperCase();
    
    if (!codigo) {
        alert("Digite o código de acesso.");
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE_URL}/turmas/codigo_acesso?codigo_acesso=${codigo}`, {
            method: "POST",
            headers: authHeader()
        });
        
        if (res.ok) {
            alert("Você entrou na turma com sucesso!");
            modalEntrar.classList.add("oculta");
            document.getElementById("inputCodigoAcesso").value = "";
            carregarTurmas();
        } else {
            const err = await res.json();
            alert(err.detail || "Código de acesso inválido ou você já está na turma.");
        }
    } catch (e) {
        alert("Falha ao comunicar com o servidor.");
    }
});

// Pesquisa local
document.getElementById("buscarTurma").addEventListener("click", () => {
    const busca = document.getElementById("buscaTurma").value.toLowerCase().trim();
    if (busca === "") {
        renderizarTurmas(todasTurmas);
        mensagemErro.textContent = "";
        return;
    }
    
    const filtradas = todasTurmas.filter(t => 
        t.descricao.toLowerCase().includes(busca) || 
        (t.disciplina?.nome || "").toLowerCase().includes(busca) ||
        (t.professor?.nome || "").toLowerCase().includes(busca)
    );
    
    renderizarTurmas(filtradas);
    if (filtradas.length === 0) {
        mensagemErro.textContent = "Nenhuma turma encontrada.";
        mensagemErro.style.color = "red";
    } else {
        mensagemErro.textContent = "Resultados encontrados.";
        mensagemErro.style.color = "green";
    }
});

// Init
configurarAcesso();
carregarTurmas();