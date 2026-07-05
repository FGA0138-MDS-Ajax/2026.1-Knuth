const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "login.html";
}

// A sidebar e o botão sair são gerenciados automaticamente pelo config.js

const feedDuvidas      = document.getElementById("feedDuvidas");
const seletorTurmaFeed = document.getElementById("seletorTurmaFeed");

let turmasMap = {};

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
        localStorage.removeItem("user_profile_cache");
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

function formatarData(isoString) {
    return new Date(isoString).toLocaleString("pt-BR", {
        day: "2-digit", month: "2-digit", year: "numeric",
        hour: "2-digit", minute: "2-digit",
    });
}

// ─── Perfil ───────────────────────────────────────────────────────────────────

async function carregarPerfil() {
    try {
        const cached = localStorage.getItem("user_profile_cache");
        let dados;
        if (cached) {
            dados = JSON.parse(cached);
        } else {
            const resposta = await fetch(`${API_BASE_URL}/me`, {
                headers: authHeader(),
            });
            if (tratarNaoAutorizado(resposta.status)) return;
            if (!resposta.ok) throw new Error();
            dados = await resposta.json();
            localStorage.setItem("user_profile_cache", JSON.stringify(dados));
        }

        const nome = dados.aluno_nome || dados.professor_nome || dados.sub.split("@")[0];
        document.getElementById("boas-vindas").textContent = `Olá, ${nome}!`;
    } catch {
        const nomeSalvo = localStorage.getItem("user_name") || "Usuário";
        document.getElementById("boas-vindas").textContent = `Olá, ${nomeSalvo}!`;
    }
}

// ─── Turmas ───────────────────────────────────────────────────────────────────

async function carregarTurmas() {
    try {
        const resposta = await fetch(`${API_BASE_URL}/turmas/minhas_turmas`, {
            headers: authHeader(),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) return;

        const turmas = await resposta.json();

        turmasMap = {};
        turmas.forEach((turma) => {
            turmasMap[turma.id] = {
                descricao:  turma.descricao,
                periodo:    turma.periodo,
                disciplina: turma.disciplina?.nome || "Geral",
            };

            const option = document.createElement("option");
            option.value = turma.id;
            option.textContent = `${turma.descricao} — ${turma.disciplina?.nome || "Geral"}`;
            seletorTurmaFeed.appendChild(option);
        });

        await carregarFeedDuvidas(turmas);
    } catch (erro) {
        console.error("Falha ao carregar turmas:", erro);
    }
}

// ─── Feed de Dúvidas Recentes ─────────────────────────────────────────────────

async function carregarFeedDuvidas(turmas) {
    if (!turmas || turmas.length === 0) {
        feedDuvidas.innerHTML = `<p class="feed-estado">Você não está matriculado em nenhuma turma ainda.</p>`;
        return;
    }

    try {
        const requisicoes = turmas.map((turma) =>
            fetch(`${API_BASE_URL}/perguntas/turma/${turma.id}`, {
                headers: authHeader(),
            }).then(r => r.ok ? r.json() : [])
        );

        const resultados     = await Promise.all(requisicoes);
        const todasPerguntas = resultados.flat();

        todasPerguntas.sort(
            (a, b) => new Date(b.data_criacao) - new Date(a.data_criacao)
        );

        feedDuvidas.innerHTML = "";

        const recentes = todasPerguntas.slice(0, 10);

        if (recentes.length === 0) {
            feedDuvidas.innerHTML = `<p class="feed-estado">Nenhuma dúvida ainda. Seja o primeiro a perguntar!</p>`;
            return;
        }

        recentes.forEach(renderizarCardFeed);
    } catch (erro) {
        console.error("Falha ao carregar feed:", erro);
        feedDuvidas.innerHTML = `<p class="feed-estado">Não foi possível carregar as dúvidas.</p>`;
    }
}

function criarCardFeed(pergunta) {
    const turmaInfo  = turmasMap[pergunta.turma_id] || {};
    const disciplina = turmaInfo.disciplina || "Geral";
    const turmaDesc  = turmaInfo.descricao  || `Turma ${pergunta.turma_id}`;

    const card = document.createElement("div");
    card.classList.add("feed-card-duvida");
    card.innerHTML = `
        <div class="feed-card-header">
            <span class="feed-disciplina">📚 ${escaparHTML(disciplina)} · ${escaparHTML(turmaDesc)}</span>
            <span class="badge-feed-status ${classeBadgeStatus(pergunta.status)}">${pergunta.status}</span>
        </div>
        <p class="feed-card-texto">${escaparHTML(pergunta.texto)}</p>
        <p class="feed-card-data">📅 ${formatarData(pergunta.data_criacao)}</p>
        <a href="duvidas.html" class="feed-link-ver">Ver na página de Dúvidas →</a>
    `;
    return card;
}

function renderizarCardFeed(pergunta) {
    feedDuvidas.appendChild(criarCardFeed(pergunta));
}

// ─── Postagem Rápida ──────────────────────────────────────────────────────────

async function publicarDuvidaRapida() {
    const texto   = document.getElementById("textoDuvida").value.trim();
    const turmaId = parseInt(seletorTurmaFeed.value);

    if (!turmaId) {
        alert("Selecione uma turma para postar a dúvida.");
        return;
    }
    if (texto.length < 5 || texto.length > 500) {
        alert("A dúvida deve ter entre 5 e 500 caracteres.");
        return;
    }

    try {
        const resposta = await fetch(`${API_BASE_URL}/perguntas/`, {
            method: "POST",
            headers: jsonAuthHeaders(),
            body: JSON.stringify({
                texto,
                turma_id: turmaId,
                is_restrita_professor: false,
                is_restrita_monitor: false,
            }),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) {
            const erro = await resposta.json();
            alert(erro.detail || "Erro ao publicar dúvida.");
            return;
        }

        const novaPergunta = await resposta.json();
        document.getElementById("textoDuvida").value = "";

        const novoCard    = criarCardFeed(novaPergunta);
        const estadoVazio = feedDuvidas.querySelector(".feed-estado");
        if (estadoVazio) estadoVazio.remove();

        feedDuvidas.insertBefore(novoCard, feedDuvidas.firstChild);
    } catch (erro) {
        console.error("Falha ao publicar dúvida:", erro);
        alert("Não foi possível conectar ao servidor.");
    }
}

document.getElementById("btnPublicarFeed").addEventListener("click", publicarDuvidaRapida);

carregarPerfil();
carregarTurmas();
