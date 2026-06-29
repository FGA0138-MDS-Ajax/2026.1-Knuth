const form = document.getElementById("loginForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    // campo matrícula existe no layout mas não é usado na autenticação

    // O endpoint /token espera application/x-www-form-urlencoded
    const corpo = new URLSearchParams();
    corpo.append("username", email);
    corpo.append("password", senha);

    try {
        const resposta = await fetch(`${API_BASE_URL}/token`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: corpo,
        });

        if (!resposta.ok) {
            const erro = await resposta.json();
            alert(erro.detail || "E-mail ou senha inválidos.");
            return;
        }

        const dados = await resposta.json();

        // Salva o token para uso nas demais páginas
        localStorage.setItem("access_token", dados.access_token);

        window.location.href = "dashboard.html";
    } catch {
        // Cai aqui se o servidor estiver fora do ar ou sem rede
        alert("Não foi possível conectar ao servidor. Tente novamente.");
    }
});
const linkEsqueci = document.getElementById("esqueciSenha");

linkEsqueci.addEventListener("click", async (e) => {
    e.preventDefault();

    const email = prompt("Digite seu e-mail para recuperação de senha:");

    if (!email) return;

    try {
        const resposta = await fetch(`${API_BASE_URL}/forgot-password`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email })
        });

        let dados;

        // tenta ler JSON mesmo se vier vazio
        try {
            dados = await resposta.json();
        } catch {
            dados = {};
        }

        if (resposta.ok) {
            alert("Se o e-mail existir, enviamos instruções de recuperação.");
        } else {
            alert(dados.detail || "Erro ao solicitar recuperação de senha.");
        }

    } catch (erro) {
        console.error(erro);
        alert("Erro de conexão com o servidor.");
    }
});