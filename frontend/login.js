const form = document.getElementById("loginForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            // O FastAPI geralmente espera os dados assim no login:
            body: new URLSearchParams({
                'username': email,
                'password': senha
            })
        });

        if (response.ok) {
            const data = await response.json();
            // Salva o token se a API retornar um (opcional, mas recomendado)
            localStorage.setItem("token", data.access_token);
            alert("Login realizado com sucesso!");
            window.location.href = "dashboard.html";
        } else {
            alert("E-mail ou senha incorretos!");
        }
    } catch (err) {
        alert("Erro ao conectar ao servidor.");
    }
});