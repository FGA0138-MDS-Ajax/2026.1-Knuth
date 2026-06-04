const API_BASE_URL = "http://127.0.0.1:8000";

async function carregarTurmas() {
    try {
        const response = await fetch(`${API_BASE_URL}/turmas/`);
        if (!response.ok) throw new Error("Erro ao buscar turmas");
        
        const turmas = await response.json();
        const container = document.getElementById("listaTurmas");
        
        container.innerHTML = turmas.map(t => `
            <div class="card">
                <h3>📘 ${t.nome || "Turma sem nome"}</h3>
                <p>ID: ${t.id}</p>
                <button class="entrar" data-id="${t.id}">Entrar</button>
            </div>
        `).join('');

        adicionarEventosEntrar();
    } catch (err) {
        console.error("Falha na integração:", err);
    }
}

document.getElementById("novaTurma").addEventListener("click", async () => {
    const nome = prompt("Digite o nome da nova turma:");
    if (!nome) return;

    try {
        const response = await fetch(`${API_BASE_URL}/turmas/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome: nome })
        });

        if (response.ok) {
            alert("Turma criada!");
            carregarTurmas(); // Atualiza a tela
        } else {
            alert("Erro ao criar turma.");
        }
    } catch (err) {
        console.error("Erro na criação:", err);
    }
});

function adicionarEventosEntrar() {
    document.querySelectorAll(".entrar").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.getAttribute("data-id");
            alert(`Abrindo turma ID: ${id}...`);
        });
    });
}

document.getElementById("buscarTurma")?.addEventListener("click", async () => {
    const busca = document.getElementById("buscaTurma").value.toLowerCase().trim();
    const mensagem = document.getElementById("mensagemErro");

    try {
        const response = await fetch(`${API_BASE_URL}/turmas/`);
        const turmas = await response.json();
        
        const encontrada = turmas.find(t => t.nome.toLowerCase() === busca);
        
        mensagem.textContent = encontrada ? "Turma encontrada!" : "Turma não encontrada.";
    } catch {
        mensagem.textContent = "Erro ao buscar no servidor.";
    }
});

// Inicializa ao abrir a página
carregarTurmas();