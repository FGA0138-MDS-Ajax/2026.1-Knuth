async function carregarCursos() {
    const select = document.getElementById("curso_id");
    try {
        const resposta = await fetch(`${API_BASE_URL}/cursos/`);
        if (!resposta.ok) throw new Error();
        const cursos = await resposta.json();
        select.innerHTML = '<option value="">Selecione o curso</option>';
        cursos.forEach(curso => {
            const option = document.createElement("option");
            option.value = curso.id;
            option.textContent = curso.nome;
            select.appendChild(option);
        });
    } catch {
        select.innerHTML = '<option value="">Erro ao carregar cursos</option>';
    }
}

carregarCursos();

const form = document.getElementById("cadastroForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const matricula = document.getElementById("matricula").value;
    const curso_id = parseInt(document.getElementById("curso_id").value);
    const senha = document.getElementById("senha").value;
    const confirmarSenha = document.getElementById("confirmarSenha").value;

    if (senha !== confirmarSenha) {
        alert("As senhas não coincidem.");
        return;
    }

    if (!curso_id) {
        alert("Selecione um curso.");
        return;
    }

    try {
        const resposta = await fetch(`${API_BASE_URL}/usuarios/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
            username: email,  
            password: senha,  
            nome: nome,
            matricula: matricula,
            curso_id: curso_id
        }),
    });
       if (!resposta.ok) {
            const erro = await resposta.json();
            console.error("Erro do servidor:", erro); 
            alert(JSON.stringify(erro));
            return;
}

        alert("Conta criada com sucesso! Faça login para continuar.");
        window.location.href = "../login.html";
    } catch {
        alert("Não foi possível conectar ao servidor. Tente novamente.");
    }
});
