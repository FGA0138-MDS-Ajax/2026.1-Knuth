document.addEventListener("DOMContentLoaded", () => {
    
    // --- Lógica Sair ---
    const btnSair = document.getElementById("btnSair");
    if (btnSair) {
        btnSair.addEventListener("click", () => window.location.href = "login.html");
    }

    // --- BANCO DE DADOS SIMULADO DAS DISCIPLINAS ---
    const dadosDisciplinas = {
        "mds": { nome: "💻 Engenharia de Software (MDS)", desc: "Fórum Geral • Turmas: A, B e C" },
        "estrutura-de-dados": { nome: "📘 Estrutura de Dados", desc: "Fórum Geral • Turmas: A e B" },
        "banco-de-dados": { nome: "🗄️ Banco de Dados", desc: "Fórum Geral • Turmas: A" },
        "calculo-1": { nome: "📐 Cálculo 1", desc: "Fórum Geral • Turmas: A, B, C e D" },
        "sistemas-digitais": { nome: "🔌 Sistemas Digitais", desc: "Fórum Geral • Turmas: A e B" },
        "fisica-1": { nome: "🍎 Física 1", desc: "Fórum Geral • Turmas: A e C" }
    };

    // --- Captura o ID vindo da URL (ex: ?id=mds) ---
    const params = new URLSearchParams(window.location.search);
    const idDisciplina = params.get("id") || "mds"; // Padrão mds caso não venha ID

    // Atualiza os textos da tela com base na disciplina clicada
    const infoMateria = dadosDisciplinas[idDisciplina];
    if (infoMateria) {
        document.getElementById("nomeDisciplina").textContent = infoMateria.nome;
        document.getElementById("descDisciplina").textContent = infoMateria.desc;
    }

    // --- Lógica do Botão se Inscrever ---
    const btnInscrever = document.getElementById("btnInscrever");
    if (btnInscrever) {
        // Verifica se já estava inscrito antes
        if (localStorage.getItem("inscrito_" + idDisciplina)) {
            btnInscrever.textContent = "Inscrito ✓";
            btnInscrever.style.background = "#22c55e"; // Muda para verde
            btnInscrever.style.color = "white";
            btnInscrever.disabled = true; // Desativa para não clicar de novo
        }

        btnInscrever.addEventListener("click", () => {
            btnInscrever.textContent = "Inscrito ✓";
            btnInscrever.style.background = "#22c55e";
            btnInscrever.style.color = "white";
            btnInscrever.disabled = true; 
            
            // Salva a inscrição no navegador
            localStorage.setItem("inscrito_" + idDisciplina, JSON.stringify(infoMateria));
            
            alert(`Você foi matriculado em uma turma de ${infoMateria ? infoMateria.nome : "disciplina"}! Ela agora aparecerá no seu painel de Turmas.`);
        });
    }

    // --- Controle do Modal de Dúvidas ---
    const modalDuvida = document.getElementById("modalDuvida");
    const btnPublicar = document.getElementById("btnPublicarDuvida");
    const btnCancelar = document.getElementById("btnCancelarDuvida");
    const btnConfirmar = document.getElementById("btnConfirmarDuvida");

    if (btnPublicar) btnPublicar.addEventListener("click", () => modalDuvida.classList.remove("oculta"));
    if (btnCancelar) btnCancelar.addEventListener("click", () => modalDuvida.classList.add("oculta"));

    if (btnConfirmar) {
        btnConfirmar.addEventListener("click", () => {
            const textarea = document.getElementById("textoDuvida");
            const texto = textarea.value.trim();

            if (!texto) {
                alert("Escreva sua dúvida antes de publicar.");
                return;
            }

            const feed = document.getElementById("feedDuvidas");
            const novaDuvidaHTML = `
                <div class="duvida-card">
                    <div class="duvida-header">
                        <span class="autor">Você</span>
                        <span class="tempo">Agora</span>
                    </div>
                    <p>${texto}</p>
                    <button class="btn-responder">Responder</button>
                </div>
            `;

            feed.insertAdjacentHTML("afterbegin", novaDuvidaHTML);
            textarea.value = "";
            modalDuvida.classList.add("oculta");
        });
    }
});