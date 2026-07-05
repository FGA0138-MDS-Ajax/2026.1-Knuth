const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "login.html";
}

let todasDisciplinas = [];

function authHeader() {
    return { "Authorization": `Bearer ${token}` };
}

async function carregarDisciplinas() {
    const container = document.querySelector(".cards");
    try {
        const res = await fetch(`${API_BASE_URL}/disciplinas/`, {
            headers: authHeader()
        });
        if (res.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }
        if (!res.ok) {
            container.innerHTML = `<p style="color:#ef4444;text-align:center;">Erro ao carregar disciplinas do servidor.</p>`;
            return;
        }
        todasDisciplinas = await res.json();
        renderizarDisciplinas(todasDisciplinas);
    } catch (e) {
        console.error("Falha ao buscar disciplinas:", e);
        container.innerHTML = `<p style="color:#ef4444;text-align:center;">Erro de conexão com o servidor.</p>`;
    }
}

function renderizarDisciplinas(lista) {
    const container = document.querySelector(".cards");
    const mensagem = document.getElementById("mensagem-sem-resultados");
    container.innerHTML = "";
    
    if (lista.length === 0) {
        mensagem.style.display = "block";
        return;
    }
    
    mensagem.style.display = "none";
    lista.forEach(d => {
        const card = document.createElement("div");
        card.className = "card disciplina";
        card.innerHTML = `
            <h2>${d.nome}</h2>
            <p>Código: ${d.codigo}</p>
            <span>Fórum geral da disciplina</span>
            <button onclick="window.location.href='disciplina-detalhe.html?id=${d.id}'">Acessar Fórum</button>
        `;
        container.appendChild(card);
    });
}

function filtrarDisciplinas() {
    const input = document.getElementById("pesquisa").value.toLowerCase().trim();
    if (input === "") {
        renderizarDisciplinas(todasDisciplinas);
        return;
    }
    
    const filtradas = todasDisciplinas.filter(d => 
        d.nome.toLowerCase().includes(input) || 
        d.codigo.toLowerCase().includes(input)
    );
    renderizarDisciplinas(filtradas);
}

// Inicializa
carregarDisciplinas();