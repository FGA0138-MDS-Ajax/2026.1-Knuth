// ==========================================
// MÓDULO: DASHBOARD ACADÊMICO
// ==========================================

// INTEGRAÇÃO
// 1. Criar rota GET /me/disciplinas -> Retorna as turmas que o aluno está matriculado.
// 2. Criar rota GET /avisos -> Retorna as últimas atualizações das turmas do aluno.
// 3. Criar rota GET /disciplinas/buscar?q={texto} -> Retorna resultados da pesquisa.

async function carregarDashboardAcademico() {
    const token = localStorage.getItem("access_token");

    // 1. Carregar Minhas Turmas
    try {
        // Substituir a URL abaixo pela rota real do backend
        const responseTurmas = await fetch("http://localhost:8000/me/disciplinas", {
            headers: { "Authorization": `Bearer ${token}` }
        });
        
        const listaTurmas = document.getElementById("listaTurmas");
        if (responseTurmas.ok) {
            const turmas = await responseTurmas.json();
            listaTurmas.innerHTML = turmas.map(t => `<li>${t.nome} - Prof. ${t.professor}</li>`).join("");
        } else {
            listaTurmas.innerHTML = "<li>Nenhuma disciplina encontrada.</li>";
        }
    } catch (error) {
        console.error("Erro ao carregar turmas. O backend está rodando?", error);
    }

    // 2. Carregar Mural de Avisos
    try {
        // Substituir a URL abaixo pela rota real do backend
        const responseAvisos = await fetch("http://localhost:8000/avisos", {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const listaAvisos = document.getElementById("listaAvisos");
        if (responseAvisos.ok) {
            const avisos = await responseAvisos.json();
            listaAvisos.innerHTML = avisos.map(a => `
                <div class="aviso-card">
                    <strong>${a.disciplina}</strong>: ${a.mensagem} <em>(${a.data})</em>
                </div>
            `).join("");
        } else {
            listaAvisos.innerHTML = "<p>Nenhuma atualização recente.</p>";
        }
    } catch (error) {
        console.error("Erro ao carregar avisos.", error);
    }
}

// 3. Lógica do Buscador
document.getElementById("btnBuscar").addEventListener("click", async () => {
    const termoBusca = document.getElementById("inputBusca").value;
    if (!termoBusca) return;

    //  Integração: Ligar com a rota de busca do backend
    console.log(`Enviando busca para o backend: /disciplinas/buscar?q=${termoBusca}`);
    alert(`A busca por "${termoBusca}" será exibida aqui em breve!`);
});

// Inicializa os painéis ao carregar a página
carregarDashboardAcademico();