const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "login.html";
}

document.getElementById("btnSair").addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_name");
    window.location.href = "login.html";
});

function authHeader() {
    return { "Authorization": `Bearer ${token}` };
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

function formatarData(isoString) {
    return new Date(isoString).toLocaleString("pt-BR", {
        day: "2-digit", month: "2-digit", year: "numeric",
        hour: "2-digit", minute: "2-digit",
    });
}

// ─── Perfil ───────────────────────────────────────────────────────────────────

async function carregarPerfil() {
    try {
        const resposta = await fetch(`${API_BASE_URL}/me`, {
            headers: authHeader(),
        });
        if (tratarNaoAutorizado(resposta.status)) return;
        if (!resposta.ok) throw new Error();

        const dados = await resposta.json();
        const nome  = dados.aluno_nome || dados.sub.split("@")[0];
        const cargo = dados.is_professor ? "Professor" : (dados.is_admin ? "Administrador" : "Aluno");

        document.getElementById("perfilNome").textContent      = dados.aluno_nome     || dados.sub.split("@")[0];
        document.getElementById("perfilMatricula").textContent = dados.aluno_matricula || "Não informada";
        document.getElementById("perfilCurso").textContent     = dados.aluno_curso     || "Não informado";
        document.getElementById("perfilEmail").textContent     = dados.aluno_email     || dados.sub;
        document.getElementById("sidebarNome").textContent     = nome;
        document.getElementById("sidebarCargo").textContent    = cargo;

        localStorage.setItem("user_name", nome);
    } catch {
        const nomeSalvo = localStorage.getItem("user_name") || "Usuário";
        document.getElementById("perfilNome").textContent  = nomeSalvo;
        document.getElementById("sidebarNome").textContent = nomeSalvo;
    }
}

// ─── Turmas e Dúvidas Recentes ────────────────────────────────────────────────

async function carregarDadosAcademicos() {
    const listaTurmasEl = document.getElementById("listaTurmas");
    const listaAvisosEl = document.getElementById("listaAvisos");

    try {
        const resposta = await fetch(`${API_BASE_URL}/turmas/minhas_turmas`, {
            headers: authHeader(),
        });
        if (tratarNaoAutorizado(resposta.status)) return;

        if (!resposta.ok) {
            listaTurmasEl.innerHTML = "<li>Nenhuma turma encontrada.</li>";
            listaAvisosEl.innerHTML = "<p>Sem dúvidas recentes.</p>";
            return;
        }

        const turmas = await resposta.json();

        if (turmas.length === 0) {
            listaTurmasEl.innerHTML = "<li>Você não está matriculado em nenhuma turma.</li>";
            listaAvisosEl.innerHTML = "<p>Sem dúvidas recentes.</p>";
            return;
        }

        listaTurmasEl.innerHTML = turmas.map(t => `
            <li>
                <strong>${escaparHTML(t.descricao)}</strong>
                — ${escaparHTML(t.disciplina?.nome || "Geral")}
                <small>(${escaparHTML(t.periodo)})</small>
            </li>
        `).join("");

        await carregarDuvidasRecentes(turmas, listaAvisosEl);
    } catch (erro) {
        console.error("Falha ao carregar dados acadêmicos:", erro);
        listaTurmasEl.innerHTML = "<li>Aguardando conexão com o servidor...</li>";
        listaAvisosEl.innerHTML = "<p>Aguardando conexão com o servidor...</p>";
    }
}

async function carregarDuvidasRecentes(turmas, container) {
    try {
        const requisicoes = turmas.map((turma) =>
            fetch(`${API_BASE_URL}/perguntas/turma/${turma.id}`, {
                headers: authHeader(),
            }).then(r => r.ok ? r.json() : [])
        );

        const resultados = await Promise.all(requisicoes);
        const todas      = resultados.flat();

        todas.sort((a, b) => new Date(b.data_criacao) - new Date(a.data_criacao));

        const recentes = todas.slice(0, 5);

        if (recentes.length === 0) {
            container.innerHTML = "<p>Nenhuma dúvida recente.</p>";
            return;
        }

        container.innerHTML = recentes.map(p => `
            <div class="aviso-card">
                <strong>${escaparHTML(p.texto.substring(0, 60))}${p.texto.length > 60 ? "..." : ""}</strong>
                <small> · ${formatarData(p.data_criacao)}</small>
            </div>
        `).join("");
    } catch (erro) {
        console.error("Falha ao carregar dúvidas recentes:", erro);
        container.innerHTML = "<p>Não foi possível carregar as dúvidas.</p>";
    }
}

// ─── Buscador ─────────────────────────────────────────────────────────────────

document.getElementById("btnBuscar").addEventListener("click", () => {
    const termoBusca = document.getElementById("inputBusca").value.trim();
    if (!termoBusca) return;
    alert(`Busca por "${termoBusca}" ainda não está disponível no servidor.`);
});

carregarPerfil();
carregarDadosAcademicos();
