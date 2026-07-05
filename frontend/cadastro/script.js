// Alterna campos com base no tipo de usuário
const tipoUsuarioSelect = document.getElementById("tipoUsuario");
const matriculaInput = document.getElementById("matricula");
const cursoSelect = document.getElementById("curso_id");

tipoUsuarioSelect.addEventListener("change", () => {
    const tipo = tipoUsuarioSelect.value;
    if (tipo === "professor") {
        matriculaInput.style.display = "none";
        matriculaInput.required = false;
        cursoSelect.style.display = "none";
        cursoSelect.required = false;
    } else {
        matriculaInput.style.display = "block";
        matriculaInput.required = true;
        cursoSelect.style.display = "block";
        cursoSelect.required = true;
    }
});

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
    const tipoUsuario = document.getElementById("tipoUsuario").value;
    const senha = document.getElementById("senha").value;
    const confirmarSenha = document.getElementById("confirmarSenha").value;

    if (senha !== confirmarSenha) {
        alert("As senhas não coincidem.");
        return;
    }

    const isAluno = (tipoUsuario === "aluno");

    if (isAluno) {
        const curso_id = parseInt(document.getElementById("curso_id").value);
        if (!curso_id) {
            alert("Selecione um curso.");
            return;
        }
    }

    try {
        const respostaUsuario = await fetch(`${API_BASE_URL}/usuarios/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: email,
                password: senha,
                is_aluno: isAluno,
                is_professor: !isAluno
            }),
        });

        if (!respostaUsuario.ok) {
            const erro = await respostaUsuario.json();
            alert(erro.detail || "Erro ao criar usuário.");
            return;
        }

        if (isAluno) {
            const matricula = document.getElementById("matricula").value;
            const curso_id = parseInt(document.getElementById("curso_id").value);

            const respostaAluno = await fetch(`${API_BASE_URL}/alunos/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    nome,
                    email,
                    matricula,
                    curso_id
                }),
            });

            if (!respostaAluno.ok) {
                const erro = await respostaAluno.json();
                alert(erro.detail || "Usuário criado, mas erro ao criar perfil de aluno.");
                return;
            }
        } else {
            const respostaProf = await fetch(`${API_BASE_URL}/professores/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    nome,
                    email
                }),
            });

            if (!respostaProf.ok) {
                const erro = await respostaProf.json();
                alert(erro.detail || "Usuário criado, mas erro ao criar perfil de professor.");
                return;
            }
        }

        alert("Conta criada com sucesso! Faça login para continuar.");
        window.location.href = "../login.html";
    } catch {
        alert("Não foi possível conectar ao servidor. Tente novamente.");
    }
});