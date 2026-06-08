const API_BASE_URL = "http://127.0.0.1:8000";

async function carregarTurmas() {
    try {
        const response = await fetch(`${API_BASE_URL}/turmas/`);
        if (!response.ok) throw new Error("Erro ao buscar turmas");
        
        const turmas = await response.json();
        const container = document.getElementById("listaTurmas");
        
        container.innerHTML = turmas.map(t => `
            <div class="card">
                <h3>📘 ${t.descricao || "Turma sem nome"}</h3>
                <p>ID: ${t.id} | Horário: ${t.horario}</p>
                <button class="entrar" data-id="${t.id}">Entrar na Turma</button>
            </div>
        `).join('');

        adicionarEventosEntrar();
    } catch (err) {
        console.error("Falha na integração:", err);
    }
}

document.getElementById("btnCriar")?.addEventListener("click", async () => {
    const novaTurma = {
        descricao: document.getElementById("descInput").value,
        horario: document.getElementById("horarioInput").value,
        periodo: "2026.1",
        disciplina_id: parseInt(document.getElementById("discIdInput").value),
        professor_id: parseInt(document.getElementById("profIdInput").value)
    };

    try {
        const response = await fetch(`${API_BASE_URL}/turmas/`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify(novaTurma)
        });

        if (response.ok) {
            alert("Turma criada com sucesso!");
            carregarTurmas();
        } else {
            const erro = await response.json();
            console.error("Detalhes do erro:", erro);
            alert(`Erro ao criar turma: ${erro.detail || "Verifique o console"}`);
        }
    } catch (err) {
        console.error("Erro na requisição:", err);
    }
});

function adicionarEventosEntrar() {
    document.querySelectorAll(".entrar").forEach(button => {
        button.addEventListener("click", async () => {
            const idTurma = button.getAttribute("data-id");
            const response = await fetch(`${API_BASE_URL}/turmas/${idTurma}/matricular`, {
                method: "POST",
                headers: { 
                    "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                    "Content-Type": "application/json" 
                }
            });
            
            if (response.ok) {
                alert("Matrícula realizada!");
            } else {
                const erro = await response.json();
                alert(`Erro ao matricular: ${erro.detail || "Verifique o console!"}`);
            }
        });
    });
}

document.getElementById("buscarTurma")?.addEventListener("click", async () => {
    const busca = document.getElementById("buscaTurma").value.toLowerCase().trim();
    const mensagem = document.getElementById("mensagemErro");

    try {
        const response = await fetch(`${API_BASE_URL}/turmas/`);
        const turmas = await response.json();
        
        const encontrada = turmas.find(t => t.descricao.toLowerCase().includes(busca));
        mensagem.textContent = encontrada ? "Turma encontrada!" : "Turma não encontrada.";
    } catch {
        mensagem.textContent = "Erro ao buscar no servidor.";
    }
});

carregarTurmas();