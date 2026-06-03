document.getElementById("cadastroForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const matricula = document.getElementById("matricula").value;
    const tipo = document.getElementById("tipo").value;
    const senha = document.getElementById("senha").value;
    const confirma = document.getElementById("confirmaSenha").value;

    if (senha !== confirma) {
        alert("As senhas não coincidem!");
        return;
    }

    const dados = {
        username: email,
        password: senha,
        is_active: true,
        is_aluno: tipo === "aluno",
        is_monitor: tipo === "monitor",
        is_professor: tipo === "professor",
        is_admin: false
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/usuarios", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });

        if (response.ok) {
            alert("Cadastro realizado com sucesso!");
        } else {
            const erro = await response.json();
            alert("Erro ao cadastrar: " + JSON.stringify(erro));
        }
    } catch (err) {
        console.error(err);
        alert("Erro de conexão com o servidor!");
    }
});