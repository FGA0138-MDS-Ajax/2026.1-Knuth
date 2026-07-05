const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "login.html";
}

const params = new URLSearchParams(window.location.search);
const idDisciplina = params.get("id");

function authHeader() {
    return { "Authorization": `Bearer ${token}` };
}

async function carregarDetalheDisciplina() {
    if (!idDisciplina) {
        window.location.href = "disciplinas.html";
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE_URL}/disciplinas/${idDisciplina}`, {
            headers: authHeader()
        });
        if (res.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }
        if (!res.ok) {
            alert("Disciplina não encontrada.");
            window.location.href = "disciplinas.html";
            return;
        }
        const d = await res.json();
        
        document.getElementById("nomeDisciplina").textContent = `💻 ${d.nome}`;
        document.getElementById("descDisciplina").textContent = `Código: ${d.codigo} • Fórum Geral`;
        
        const feed = document.getElementById("feedDuvidas");
        feed.innerHTML = `
            <div class="duvida-card">
                <div class="duvida-header">
                    <span class="autor">Aviso</span>
                    <span class="tempo">Agora</span>
                </div>
                <p>Este é o fórum geral da disciplina <strong>${d.nome}</strong>. Para tirar dúvidas interativas sobre a matéria, por favor acesse a página de <strong>Dúvidas</strong> ou selecione uma de suas <strong>Turmas</strong>.</p>
            </div>
        `;
    } catch (e) {
        console.error("Falha ao carregar disciplina:", e);
    }
}

// Inscrição simulada
const btnInscrever = document.getElementById("btnInscrever");
if (btnInscrever) {
    if (localStorage.getItem("inscrito_" + idDisciplina)) {
        btnInscrever.textContent = "Inscrito ✓";
        btnInscrever.style.background = "#22c55e";
        btnInscrever.style.color = "white";
        btnInscrever.disabled = true;
    }
    btnInscrever.addEventListener("click", () => {
        btnInscrever.textContent = "Inscrito ✓";
        btnInscrever.style.background = "#22c55e";
        btnInscrever.style.color = "white";
        btnInscrever.disabled = true;
        localStorage.setItem("inscrito_" + idDisciplina, "true");
        alert("Inscrição efetuada com sucesso!");
    });
}

// Modal de dúvida
const modalDuvida = document.getElementById("modalDuvida");
const btnPublicar = document.getElementById("btnPublicarDuvida");
const btnCancelar = document.getElementById("btnCancelarDuvida");
const btnConfirmar = document.getElementById("btnConfirmarDuvida");

if (btnPublicar) btnPublicar.addEventListener("click", () => modalDuvida.classList.remove("oculta"));
if (btnCancelar) btnCancelar.addEventListener("click", () => modalDuvida.classList.add("oculta"));

if (btnConfirmar) {
    btnConfirmar.addEventListener("click", () => {
        alert("Para publicar dúvidas interativas, por favor use a seção de Dúvidas ou selecione uma Turma específica.");
        modalDuvida.classList.add("oculta");
    });
}

carregarDetalheDisciplina();