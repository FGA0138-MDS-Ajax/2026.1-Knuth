document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");

    // Redireciona para login se não estiver logado
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    // Função de Logout do Menu Lateral
    document.getElementById("btnSair").addEventListener("click", () => {
        localStorage.removeItem("access_token");
        window.location.href = "login.html";
    });

    // 1. Carrega os dados do Perfil
    async function carregarPerfil() {
        try {
            const response = await fetch("http://localhost:8000/me", {
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (!response.ok) throw new Error("Sessão expirada");

            const payload = await response.json();
            
            document.getElementById("perfilNome").innerText = payload.aluno_nome || payload.sub.split('@')[0];
            document.getElementById("perfilMatricula").innerText = payload.aluno_matricula || "Não informada";
            document.getElementById("perfilCurso").innerText = payload.aluno_curso || "Não informado";
            document.getElementById("perfilEmail").innerText = payload.aluno_email || payload.sub;

        } catch (error) {
            console.error("Erro no perfil:", error);
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
        }
    }

    // 2. Carrega Turmas e Avisos
    async function carregarDadosAcademicos() {
        // Buscar Minhas Turmas (TODO Backend)
        try {
            const responseTurmas = await fetch("http://localhost:8000/me/disciplinas", {
                headers: { "Authorization": `Bearer ${token}` }
            });
            
            const listaTurmas = document.getElementById("listaTurmas");
            if (responseTurmas.ok) {
                const turmas = await responseTurmas.json();
                listaTurmas.innerHTML = turmas.map(t => `<li>${t.nome}</li>`).join("");
            } else {
                listaTurmas.innerHTML = "<li>Nenhuma disciplina encontrada.</li>";
            }
        } catch (error) {
            console.error("Aguardando backend para turmas.", error);
            document.getElementById("listaTurmas").innerHTML = "<li>Aguardando conexão com o servidor...</li>";
        }

        // Buscar Avisos (TODO Backend)
        try {
            const responseAvisos = await fetch("http://localhost:8000/avisos", {
                headers: { "Authorization": `Bearer ${token}` }
            });

            const listaAvisos = document.getElementById("listaAvisos");
            if (responseAvisos.ok) {
                const avisos = await responseAvisos.json();
                listaAvisos.innerHTML = avisos.map(a => `
                    <div class="aviso-card">
                        <strong>${a.disciplina}</strong>: ${a.mensagem}
                    </div>
                `).join("");
            } else {
                listaAvisos.innerHTML = "<p>Nenhuma atualização recente.</p>";
            }
        } catch (error) {
            console.error("Aguardando backend para avisos.", error);
            document.getElementById("listaAvisos").innerHTML = "<p>Aguardando conexão com o servidor...</p>";
        }
    }

    // 3. Lógica do Buscador
    document.getElementById("btnBuscar").addEventListener("click", () => {
        const termoBusca = document.getElementById("inputBusca").value;
        if (!termoBusca) return;
        
        console.log(`Enviando busca para: /disciplinas/buscar?q=${termoBusca}`);
        alert(`A busca por "${termoBusca}" foi solicitada. O backend precisa criar esta rota!`);
    });

    // Inicializa as funções ao abrir a página
    carregarPerfil();
    carregarDadosAcademicos();
});