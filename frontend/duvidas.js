const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "login.html";
}

const btnNovaDuvida    = document.getElementById("btnNovaDuvida");
const formulario       = document.getElementById("formulario");
const lista            = document.getElementById("listaDuvidas");
const seletorTurma     = document.getElementById("seletorTurma");
const filtroStatus     = document.getElementById("filtroStatus");
const filtroPrioridade = document.getElementById("filtroPrioridade");
const mensagemVazio    = document.getElementById("mensagemVazio");

let turmaAtual          = null;
let perguntasCarregadas = [];

function authHeader() {
    return { "Authorization": `Bearer ${token}` };
}

function jsonAuthHeaders() {
    return {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
    };
}

function tratarNaoAutorizado(status) {
    if (status === 401) {
        localStorage.removeItem("access_token");
        window.location.href = "login.html";
        return true;
    }
    return false;
}

function escaparHTML(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}

function classeBadgeStatus(status) {
    return { "aberta": "aberta", "em andamento": "em-andamento", "resolvida": "resolvida" }[status] || "aberta";
}

function classeBadgePrioridade(prioridade) {
    return { "baixa": "baixa", "media": "media", "alta": "alta" }[prioridade] || "media";
}

function labelPrioridade(prioridade) {
    return { "baixa": "Baixa", "media": "Média", "alta": "Alta" }[prioridade] || "Média";
}

function formatarData(isoString) {
    return new Date(isoString).toLocaleString("pt-BR", {
        day: "2-digit", month: "2-digit", year: "numeric",
        hour: "2-digit", minute: "2-digit",
    });S
}

// ─── Turmas ───────────────────────────────────────────────────────────────────

async function carregarTurmas() {
    try {
        const resposta = await fetch(`${API_BASE_URL}/turmas/minhas_turmas`, {
            headers: authHeader(),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) { console.error("Erro ao carregar turmas."); return; }

        const turmas = await resposta.json();
        turmas.forEach((turma) => {
            const option = document.createElement("option");
            option.value = turma.id;
            option.textContent = `${turma.descricao} — ${turma.periodo}`;
            seletorTurma.appendChild(option);
        });
    } catch (erro) {
        console.error("Falha na conexão ao carregar turmas:", erro);
    }
}

// ─── Perguntas ────────────────────────────────────────────────────────────────

async function carregarPerguntas(turmaId) {
    lista.innerHTML = "";
    mensagemVazio.classList.add("escondido");

    try {
        const resposta = await fetch(`${API_BASE_URL}/perguntas/turma/${turmaId}`, {
            headers: authHeader(),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) { console.error("Erro ao carregar perguntas."); return; }

        perguntasCarregadas = await resposta.json();
        filtrarPerguntas();
    } catch (erro) {
        console.error("Falha na conexão ao carregar perguntas:", erro);
    }
}

async function criarPergunta() {
    const texto             = document.getElementById("textoPergunta").value.trim();
    const restritaProfessor = document.getElementById("restritaProfessor").checked;
    const restritaMonitor   = document.getElementById("restritaMonitor").checked;
    const prioridade        = document.getElementById("prioridade").value;

    if (texto.length < 5 || texto.length > 500) {
        alert("A dúvida deve ter entre 5 e 500 caracteres.");
        return;
    }
    if (!turmaAtual) {
        alert("Selecione uma turma primeiro.");
        return;
    }

    try {
        const resposta = await fetch(`${API_BASE_URL}/perguntas/`, {
            method: "POST",
            headers: jsonAuthHeaders(),
            body: JSON.stringify({
                texto,
                turma_id: turmaAtual,
                is_restrita_professor: restritaProfessor,
                is_restrita_monitor: restritaMonitor,
                prioridade,
            }),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) {
            const erro = await resposta.json();
            alert(erro.detail || "Erro ao publicar dúvida.");
            return;
        }

        const novaPergunta = await resposta.json();
        perguntasCarregadas.unshift(novaPergunta);

        document.getElementById("textoPergunta").value       = "";
        document.getElementById("restritaProfessor").checked = false;
        document.getElementById("restritaMonitor").checked   = false;
        document.getElementById("prioridade").value          = "media";
        formulario.classList.add("escondido");
        filtrarPerguntas();
    } catch (erro) {
        console.error("Falha ao criar pergunta:", erro);
        alert("Não foi possível conectar ao servidor.");
    }
}

async function atualizarStatus(perguntaId, novoStatus) {
    try {
        const resposta = await fetch(`${API_BASE_URL}/perguntas/${perguntaId}`, {
            method: "PUT",
            headers: jsonAuthHeaders(),
            body: JSON.stringify({ status: novoStatus }),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) {
            const erro = await resposta.json();
            alert(erro.detail || "Erro ao atualizar status.");
            return;
        }

        const atualizada = await resposta.json();
        const idx = perguntasCarregadas.findIndex(p => p.id === perguntaId);
        if (idx !== -1) perguntasCarregadas[idx].status = atualizada.status;

        const badgeEl = lista.querySelector(`.card[data-id="${perguntaId}"] .badge-status`);
        if (badgeEl) {
            badgeEl.className   = `badge-status ${classeBadgeStatus(novoStatus)}`;
            badgeEl.textContent = novoStatus;
        }
    } catch (erro) {
        console.error("Falha ao atualizar status:", erro);
        alert("Não foi possível conectar ao servidor.");
    }
}

// ─── Respostas ────────────────────────────────────────────────────────────────

async function carregarRespostas(perguntaId) {
    const container = document.getElementById(`respostas-${perguntaId}`);
    container.innerHTML = `<p style="color:#aaa;font-size:13px">Carregando...</p>`;

    try {
        const resposta = await fetch(`${API_BASE_URL}/respostas/pergunta/${perguntaId}`, {
            headers: authHeader(),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) { container.innerHTML = ""; return; }

        const desta = await resposta.json();

        container.innerHTML = "";

        if (desta.length === 0) {
            container.innerHTML = `<p style="color:#aaa;font-size:13px">Nenhuma resposta ainda.</p>`;
            return;
        }
        desta.forEach(r => renderizarResposta(container, r));
    } catch (erro) {
        console.error("Falha ao carregar respostas:", erro);
        container.innerHTML = "";
    }
}

async function criarResposta(perguntaId) {
    const textarea = document.getElementById(`textoResposta-${perguntaId}`);
    const texto    = textarea.value.trim();

    if (texto.length < 5 || texto.length > 500) {
        alert("A resposta deve ter entre 5 e 500 caracteres.");
        return;
    }

    try {
        const resposta = await fetch(`${API_BASE_URL}/respostas/`, {
            method: "POST",
            headers: jsonAuthHeaders(),
            body: JSON.stringify({ texto, pergunta_id: perguntaId }),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) {
            const erro = await resposta.json();
            alert(erro.detail || "Erro ao publicar resposta.");
            return;
        }

        const novaResposta = await resposta.json();
        textarea.value = "";

        const container  = document.getElementById(`respostas-${perguntaId}`);
        const placeholder = container.querySelector("p");
        if (placeholder) placeholder.remove();

        renderizarResposta(container, novaResposta);
    } catch (erro) {
        console.error("Falha ao criar resposta:", erro);
        alert("Não foi possível conectar ao servidor.");
    }
}

function cargoUsuario(usuario) {
    if (usuario.is_admin)     return "Administrador";
    if (usuario.is_professor) return "Professor";
    return "Aluno";
}

function renderizarResposta(container, resposta) {
    const div = document.createElement("div");
    div.classList.add("resposta-card");
    div.innerHTML = `
        <p class="resposta-autor">
            ${escaparHTML(resposta.usuario.username)}
            <span style="font-weight:normal;color:#666">· ${cargoUsuario(resposta.usuario)}</span>
        </p>
        <p class="resposta-data">📅 ${formatarData(resposta.data_criacao)}</p>
        <p class="resposta-texto">${escaparHTML(resposta.texto)}</p>
    `;
    container.appendChild(div);
}

// ─── Renderização ─────────────────────────────────────────────────────────────

function filtrarPerguntas() {
    lista.innerHTML = "";

    const statusFiltro     = filtroStatus.value;
    const prioridadeFiltro = filtroPrioridade.value;

    const resultado = perguntasCarregadas.filter(p => {
        const passaStatus     = statusFiltro === "todas"     || p.status === statusFiltro;
        const passaPrioridade = prioridadeFiltro === "todas" || p.prioridade === prioridadeFiltro;
        return passaStatus && passaPrioridade;
    });

    if (resultado.length === 0) {
        mensagemVazio.classList.remove("escondido");
        return;
    }
    mensagemVazio.classList.add("escondido");
    resultado.forEach(renderizarPergunta);
}

function renderizarPergunta(pergunta) {
    const badgesRestricao = [
        pergunta.is_restrita_professor ? `<span class="badge-restricao">🔒 Só professor</span>` : "",
        pergunta.is_restrita_monitor   ? `<span class="badge-restricao">🔒 Só monitor</span>`   : "",
    ].join("");

    const card = document.createElement("div");
    card.classList.add("card");
    card.dataset.id = pergunta.id;
    card.innerHTML = `
        <div class="card-cabecalho">
            <p>${escaparHTML(pergunta.texto)}</p>
            <div class="badges">
                <span class="badge-status ${classeBadgeStatus(pergunta.status)}">${pergunta.status}</span>
                <span class="badge-prioridade ${classeBadgePrioridade(pergunta.prioridade)}">${labelPrioridade(pergunta.prioridade)}</span>
                ${badgesRestricao}
            </div>
        </div>
        <p class="info-card">📅 ${formatarData(pergunta.data_criacao)}</p>
        <select class="select-status" data-pergunta-id="${pergunta.id}">
            <option value="aberta"       ${pergunta.status === "aberta"       ? "selected" : ""}>Aberta</option>
            <option value="em andamento" ${pergunta.status === "em andamento" ? "selected" : ""}>Em andamento</option>
            <option value="resolvida"    ${pergunta.status === "resolvida"    ? "selected" : ""}>Resolvida</option>
        </select>
        <div class="respostas-section">
            <button class="btn-toggle-respostas" data-pergunta-id="${pergunta.id}">
                💬 Ver respostas
            </button>
            <div class="lista-respostas escondido" id="respostas-${pergunta.id}"></div>
            <div class="form-resposta">
                <textarea
                    placeholder="Escreva uma resposta..."
                    id="textoResposta-${pergunta.id}"
                ></textarea>
                <button class="btn-responder" data-pergunta-id="${pergunta.id}">
                    Responder
                </button>
            </div>
        </div>
    `;
    lista.appendChild(card);
}

// ─── Event Listeners ──────────────────────────────────────────────────────────

seletorTurma.addEventListener("change", async () => {
    const id = parseInt(seletorTurma.value);
    if (!id) {
        turmaAtual = null;
        btnNovaDuvida.disabled = true;
        lista.innerHTML = "";
        mensagemVazio.classList.add("escondido");
        formulario.classList.add("escondido");
        return;
    }
    turmaAtual = id;
    btnNovaDuvida.disabled = false;
    await carregarPerguntas(id);
});

filtroStatus.addEventListener("change", filtrarPerguntas);
filtroPrioridade.addEventListener("change", filtrarPerguntas);

btnNovaDuvida.addEventListener("click", () => {
    formulario.classList.toggle("escondido");
});

document.getElementById("publicar").addEventListener("click", criarPergunta);

lista.addEventListener("change", (e) => {
    if (!e.target.classList.contains("select-status")) return;
    atualizarStatus(parseInt(e.target.dataset.perguntaId), e.target.value);
});

lista.addEventListener("click", async (e) => {
    const btnToggle    = e.target.closest(".btn-toggle-respostas");
    const btnResponder = e.target.closest(".btn-responder");

    if (btnToggle) {
        const perguntaId = parseInt(btnToggle.dataset.perguntaId);
        const container  = document.getElementById(`respostas-${perguntaId}`);
        const visivel    = !container.classList.contains("escondido");

        if (visivel) {
            container.classList.add("escondido");
            btnToggle.textContent = "💬 Ver respostas";
        } else {
            container.classList.remove("escondido");
            btnToggle.textContent = "💬 Ocultar respostas";
            if (container.children.length === 0) {
                await carregarRespostas(perguntaId);
            }
        }
    }

    if (btnResponder) {
        await criarResposta(parseInt(btnResponder.dataset.perguntaId));
    }
});

carregarTurmas();
