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
