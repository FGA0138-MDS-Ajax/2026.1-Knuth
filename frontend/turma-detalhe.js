const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "login.html";
}

const params = new URLSearchParams(window.location.search);
const turmaId = parseInt(params.get("id"));

if (!turmaId) {
    window.location.href = "turmas.html";
}

const feedDuvidas = document.getElementById("feedDuvidas");

function authHeader() {
    return { "Authorization": `Bearer ${token}` };
}

function jsonAuthHeaders() {
    return {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
    };
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

// ─── Carregar Turma ───────────────────────────────────────────────────────────
async function carregarTurma() {
    try {
        const res = await fetch(`${API_BASE_URL}/turmas/${turmaId}`, {
            headers: authHeader()
        });
        if (res.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }
        if (!res.ok) {
            alert("Turma não encontrada.");
            window.location.href = "turmas.html";
            return;
        }
        const t = await res.json();
        
        document.getElementById("nomeTurma").textContent = `💻 ${t.descricao}`;
        document.getElementById("profMateriaTurma").textContent = `${t.disciplina?.nome || "Geral"} | Professor(a): ${t.professor?.nome || "A definir"}`;
        document.getElementById("codigoAcessoTurma").textContent = t.codigo_acesso;
        
        configurarAcesso(t);
        carregarDuvidas();
    } catch (e) {
        console.error("Falha ao carregar turma:", e);
    }
}

// ─── Configurar Acesso ────────────────────────────────────────────────────────
function configurarAcesso(turma) {
    const role = getLoggedUserRole();
    const btnPromover = document.getElementById("btnPromoverMonitor");
    const btnEncerrar = document.getElementById("btnEncerrarTurma");
    
    // Oculta ações se não for professor da turma ou admin
    if (role === "aluno") {
        if (btnPromover) btnPromover.style.display = "none";
        if (btnEncerrar) btnEncerrar.style.display = "none";
    }
}

// ─── Carregar Perguntas (Fórum) ────────────────────────────────────────────────
async function carregarDuvidas() {
    feedDuvidas.innerHTML = `<p style="color:#666; font-size:14px; text-align:center; padding: 20px;">Carregando fórum...</p>`;
    
    try {
        const res = await fetch(`${API_BASE_URL}/perguntas/turma/${turmaId}`, {
            headers: authHeader()
        });
        if (res.ok) {
            const perguntas = await res.json();
            feedDuvidas.innerHTML = "";
            if (perguntas.length === 0) {
                feedDuvidas.innerHTML = `<p style="color:#666; font-size:14px; text-align:center; padding: 20px;">Nenhuma dúvida neste fórum ainda. Envie a primeira!</p>`;
                return;
            }
            // Ordena mais recentes no topo
            perguntas.sort((a,b) => new Date(b.data_criacao) - new Date(a.data_criacao));
            perguntas.forEach(renderizarPergunta);
        }
    } catch (e) {
        console.error("Erro ao carregar dúvidas:", e);
    }
}

function renderizarPergunta(p) {
    const card = document.createElement("div");
    card.className = "duvida-card";
    card.id = `pergunta-${p.id}`;
    card.innerHTML = `
        <div class="duvida-header">
            <span class="autor">${escaparHTML(p.aluno?.nome || "Usuário")}</span>
            <span class="tempo">${formatarData(p.data_criacao)}</span>
        </div>
        <p>${escaparHTML(p.texto)}</p>
        
        <div style="margin-top: 15px;">
            <button class="btn-responder" onclick="toggleRespostas(${p.id})">💬 Ver Respostas</button>
        </div>
        
        <div class="respostas-container oculta" id="respostas-container-${p.id}" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee;">
            <div id="respostas-lista-${p.id}" style="margin-bottom: 15px;"></div>
            <div style="display: flex; gap: 10px;">
                <input type="text" id="resposta-input-${p.id}" placeholder="Escreva uma resposta..." style="flex:1; padding: 8px; border:1px solid #ccc; border-radius:6px; outline:none;">
                <button class="btn-primario" onclick="enviarResposta(${p.id})" style="padding: 8px 15px; font-size: 13px;">Responder</button>
            </div>
        </div>
    `;
    feedDuvidas.appendChild(card);
}

// Toggle Respostas
async function toggleRespostas(perguntaId) {
    const container = document.getElementById(`respostas-container-${perguntaId}`);
    const isOculta = container.classList.contains("oculta");
    
    if (isOculta) {
        container.classList.remove("oculta");
        carregarRespostas(perguntaId);
    } else {
        container.classList.add("oculta");
    }
}

// Carregar Respostas
async function carregarRespostas(perguntaId) {
    const lista = document.getElementById(`respostas-lista-${perguntaId}`);
    lista.innerHTML = "<small style='color:#888;'>Carregando respostas...</small>";
    
    try {
        const res = await fetch(`${API_BASE_URL}/respostas/pergunta/${perguntaId}`, {
            headers: authHeader()
        });
        if (res.ok) {
            const respostas = await res.json();
            lista.innerHTML = "";
            if (respostas.length === 0) {
                lista.innerHTML = "<small style='color:#888;'>Nenhuma resposta ainda.</small>";
                return;
            }
            respostas.forEach(r => {
                const div = document.createElement("div");
                div.style.marginBottom = "10px";
                div.style.background = "#f9f9f9";
                div.style.padding = "8px 12px";
                div.style.borderRadius = "6px";
                div.innerHTML = `
                    <div style="display:flex; justify-content:space-between; font-size:11px; color:#666; margin-bottom:4px;">
                        <strong>${escaparHTML(r.usuario?.username || "Usuário")}</strong>
                        <span>${formatarData(r.data_criacao)}</span>
                    </div>
                    <p style="font-size: 13px; color:#333; margin:0;">${escaparHTML(r.texto)}</p>
                `;
                lista.appendChild(div);
            });
        }
    } catch (e) {
        console.error("Erro ao carregar respostas:", e);
    }
}

// Enviar Resposta
async function enviarResposta(perguntaId) {
    const input = document.getElementById(`resposta-input-${perguntaId}`);
    const texto = input.value.trim();
    if (!texto) return;
    
    try {
        const res = await fetch(`${API_BASE_URL}/respostas/`, {
            method: "POST",
            headers: jsonAuthHeaders(),
            body: JSON.stringify({
                texto: texto,
                pergunta_id: perguntaId
            })
        });
        if (res.ok) {
            input.value = "";
            carregarRespostas(perguntaId);
        } else {
            alert("Erro ao enviar resposta.");
        }
    } catch (e) {
        alert("Falha de conexão.");
    }
}

// ─── Modal Dúvida ─────────────────────────────────────────────────────────────
const modalDuvida = document.getElementById("modalDuvida");
const btnPublicarDuvida = document.getElementById("btnPublicarDuvida");
const btnCancelarDuvida = document.getElementById("btnCancelarDuvida");
const btnConfirmarDuvida = document.getElementById("btnConfirmarDuvida");

if (btnPublicarDuvida) {
    btnPublicarDuvida.addEventListener("click", () => modalDuvida.classList.remove("oculta"));
}
if (btnCancelarDuvida) {
    btnCancelarDuvida.addEventListener("click", () => modalDuvida.classList.add("oculta"));
}

if (btnConfirmarDuvida) {
    btnConfirmarDuvida.addEventListener("click", async () => {
        const textarea = document.getElementById("textoDuvida");
        const texto = textarea.value.trim();
        if (!texto) {
            alert("Escreva sua dúvida antes de publicar.");
            return;
        }
        
        try {
            const res = await fetch(`${API_BASE_URL}/perguntas/`, {
                method: "POST",
                headers: jsonAuthHeaders(),
                body: JSON.stringify({
                    texto: texto,
                    turma_id: turmaId,
                    is_restrita_professor: false,
                    is_restrita_monitor: false,
                    prioridade: "media"
                })
            });
            if (res.ok) {
                textarea.value = "";
                modalDuvida.classList.add("oculta");
                carregarDuvidas();
            } else {
                const err = await res.json();
                alert(err.detail || "Erro ao publicar dúvida.");
            }
        } catch (e) {
            alert("Falha ao comunicar com o servidor.");
        }
    });
}

// ─── Modal Promover Monitor ───────────────────────────────────────────────────
const modalPromover = document.getElementById("modalPromover");
const btnPromoverMonitor = document.getElementById("btnPromoverMonitor");
const btnCancelarPromover = document.getElementById("btnCancelarPromover");
const btnConfirmarPromover = document.getElementById("btnConfirmarPromover");

if (btnPromoverMonitor) {
    btnPromoverMonitor.addEventListener("click", () => modalPromover.classList.remove("oculta"));
}
if (btnCancelarPromover) {
    btnCancelarPromover.addEventListener("click", () => modalPromover.classList.add("oculta"));
}

if (btnConfirmarPromover) {
    btnConfirmarPromover.addEventListener("click", async () => {
        const inputMatricula = document.getElementById("inputMatricula");
        const matricula = inputMatricula.value.trim();
        if (!matricula) {
            alert("Digite a matrícula do aluno.");
            return;
        }
        
        try {
            // 1. Busca o aluno pela matrícula
            const resBusca = await fetch(`${API_BASE_URL}/alunos/busca?matricula=${matricula}`, {
                headers: authHeader()
            });
            if (!resBusca.ok) {
                alert("Aluno não encontrado com esta matrícula.");
                return;
            }
            const alunos = await resBusca.json();
            if (alunos.length === 0) {
                alert("Aluno não encontrado com esta matrícula.");
                return;
            }
            const aluno = alunos[0];
            
            // 2. Promove para monitor
            const resPromover = await fetch(`${API_BASE_URL}/turmas/${aluno.id}/monitorar/${turmaId}`, {
                method: "POST",
                headers: authHeader()
            });
            if (resPromover.ok) {
                alert(`O aluno ${aluno.nome} foi promovido a monitor desta turma!`);
                modalPromover.classList.add("oculta");
                inputMatricula.value = "";
            } else {
                const err = await resPromover.json();
                alert(err.detail || "Erro ao promover aluno.");
            }
        } catch (e) {
            alert("Falha de conexão com o servidor.");
        }
    });
}

// ─── Modal Encerrar Turma ─────────────────────────────────────────────────────
const modalEncerrar = document.getElementById("modalEncerrar");
const btnEncerrarTurma = document.getElementById("btnEncerrarTurma");
const btnCancelarEncerrar = document.getElementById("btnCancelarEncerrar");
const btnConfirmarEncerrar = document.getElementById("btnConfirmarEncerrar");

if (btnEncerrarTurma) {
    btnEncerrarTurma.addEventListener("click", () => modalEncerrar.classList.remove("oculta"));
}
if (btnCancelarEncerrar) {
    btnCancelarEncerrar.addEventListener("click", () => modalEncerrar.classList.add("oculta"));
}

if (btnConfirmarEncerrar) {
    btnConfirmarEncerrar.addEventListener("click", async () => {
        try {
            const res = await fetch(`${API_BASE_URL}/turmas/${turmaId}`, {
                method: "DELETE",
                headers: authHeader()
            });
            if (res.ok) {
                alert("Turma encerrada e deletada com sucesso!");
                modalEncerrar.classList.add("oculta");
                window.location.href = "turmas.html";
            } else {
                alert("Erro ao encerrar turma.");
            }
        } catch (e) {
            alert("Falha ao comunicar com o servidor.");
        }
    });
}

// Init
carregarTurma();