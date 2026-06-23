document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");

    // Função de Logout do Menu Lateral
    const btnSair = document.getElementById("btnSair");
    if (btnSair) {
        btnSair.addEventListener("click", () => {
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
        });
    }

    // 1. Carrega os dados do Perfil
    async function carregarPerfil() {
        try {
            // Se não tiver token, já pula direto para o erro para preencher os dados de teste
            if (!token) throw new Error("Modo protótipo sem backend");

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
            console.error("Backend offline. Carregando dados de teste para o layout:", error);
            // Preenche com dados provisórios em vez de redirecionar para o login
            document.getElementById("perfilNome").innerText = "Ester Almeida";
            document.getElementById("perfilMatricula").innerText = "202600123";
            document.getElementById("perfilCurso").innerText = "Engenharia (UnB)";
            document.getElementById("perfilEmail").innerText = "ester@knuths.com";
        }
    }

    // 2. Carrega Turmas e Avisos
    async function carregarDadosAcademicos() {
        try {
            if (!token) throw new Error("Sem token");
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
            document.getElementById("listaTurmas").innerHTML = "<li>Aguardando conexão com o servidor...</li>";
        }

        try {
            if (!token) throw new Error("Sem token");
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
            document.getElementById("listaAvisos").innerHTML = "<p>Aguardando conexão com o servidor...</p>";
        }
    }

    // 3. Buscador
    const btnBuscar = document.getElementById("btnBuscar");
    if (btnBuscar) {
        btnBuscar.addEventListener("click", () => {
            const termoBusca = document.getElementById("inputBusca").value;
            if (!termoBusca) return;
            
            console.log(`Enviando busca para: /disciplinas/buscar?q=${termoBusca}`);
            alert(`A busca por "${termoBusca}" foi solicitada. O backend precisa criar esta rota!`);
        });
    }

    // Inicializa as funções ao abrir a página
    carregarPerfil();
    carregarDadosAcademicos();
});