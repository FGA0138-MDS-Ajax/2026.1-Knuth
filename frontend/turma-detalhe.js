document.addEventListener("DOMContentLoaded", () => {
    
    // --- Lógica do Botão Sair ---
    const btnSair = document.getElementById("btnSair");
    if (btnSair) {
        btnSair.addEventListener("click", () => window.location.href = "login.html");
    }

    // ==========================================
    // TRAVA DE PERFIL (CONTROLE DE ACESSO)
    // ==========================================
    // CORREÇÃO: Pegue o cargo de forma mais confiável
    const userRole = localStorage.getItem("user_role") || "aluno"; 

    const btnPromoverMonitor = document.getElementById("btnPromoverMonitor");
    const btnEncerrarTurma = document.getElementById("btnEncerrarTurma");

    // Esconde os botões exclusivos se o usuário NÃO for professor nem administrador
    if (userRole !== "professor" && userRole !== "admin") {
        if (btnPromoverMonitor) btnPromoverMonitor.style.display = "none";
        if (btnEncerrarTurma) btnEncerrarTurma.style.display = "none";
    }

    // --- Elementos dos Modais ---
    const modalDuvida = document.getElementById("modalDuvida");
    const modalPromover = document.getElementById("modalPromover");
    const modalEncerrar = document.getElementById("modalEncerrar");

    // --- Abertura dos Modais ---
    const btnPublicarDuvida = document.getElementById("btnPublicarDuvida");
    if (btnPublicarDuvida) {
        btnPublicarDuvida.addEventListener("click", () => modalDuvida.classList.remove("oculta"));
    }
    
    // Só adiciona os eventos de clique se os botões estiverem visíveis na tela
    if (userRole === "professor" || userRole === "admin") {
        if (btnPromoverMonitor) btnPromoverMonitor.addEventListener("click", () => modalPromover.classList.remove("oculta"));
        if (btnEncerrarTurma) btnEncerrarTurma.addEventListener("click", () => modalEncerrar.classList.remove("oculta"));
    }

    // --- Fechamento dos Modais (Botões Cancelar) ---
    const btnCancelarDuvida = document.getElementById("btnCancelarDuvida");
    if (btnCancelarDuvida) btnCancelarDuvida.addEventListener("click", () => modalDuvida.classList.add("oculta"));
    
    const btnCancelarPromover = document.getElementById("btnCancelarPromover");
    if (btnCancelarPromover) btnCancelarPromover.addEventListener("click", () => modalPromover.classList.add("oculta"));
    
    const btnCancelarEncerrar = document.getElementById("btnCancelarEncerrar");
    if (btnCancelarEncerrar) btnCancelarEncerrar.addEventListener("click", () => modalEncerrar.classList.add("oculta"));

    // --- Ações de Confirmação ---

    // 1. Publicar Dúvida (Coloca no topo do Feed)
    const btnConfirmarDuvida = document.getElementById("btnConfirmarDuvida");
    if (btnConfirmarDuvida) {
        btnConfirmarDuvida.addEventListener("click", () => {
            const textarea = document.getElementById("textoDuvida");
            if (!textarea) return; // Segurança contra IDs ausentes
            
            const texto = textarea.value.trim();
            if (!texto) {
                alert("Escreva sua dúvida antes de publicar.");
                return;
            }

            const feed = document.getElementById("feedDuvidas");
            if (!feed) return; // Segurança contra IDs ausentes
            
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

    // 2. Promover Monitor
    const btnConfirmarPromover = document.getElementById("btnConfirmarPromover");
    if (btnConfirmarPromover) {
        btnConfirmarPromover.addEventListener("click", () => {
            const inputMatricula = document.getElementById("inputMatricula");
            if (!inputMatricula) return;
            
            const matricula = inputMatricula.value.trim();
            if (!matricula) {
                alert("Digite a matrícula do aluno.");
                return;
            }
            alert(`O aluno com matrícula ${matricula} foi promovido a monitor!`);
            inputMatricula.value = "";
            modalPromover.classList.add("oculta");
        });
    }

    // 3. Encerrar Turma
    const btnConfirmarEncerrar = document.getElementById("btnConfirmarEncerrar");
    if (btnConfirmarEncerrar) {
        btnConfirmarEncerrar.addEventListener("click", () => {
            alert("A turma foi encerrada com sucesso. Ela não aparecerá mais para os alunos.");
            modalEncerrar.classList.add("oculta");
            window.location.href = "turmas.html"; 
        });
    }
});