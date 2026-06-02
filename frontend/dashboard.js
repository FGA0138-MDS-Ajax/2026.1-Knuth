// Pega o botão com o ID correto do HTML
const btnSair = document.getElementById("btnSair");

btnSair.addEventListener("click", () => {
    // Limpa os dados e volta pro login
    localStorage.removeItem("access_token"); 
    localStorage.removeItem("user_name");    
    window.location.href = "login.html";     
});
const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "login.html";
} else {
    carregarUsuario();
}

async function carregarUsuario() {
    try {
        // Busca os dados do usuário logado usando o token salvo
        const resposta = await fetch(`${API_BASE_URL}/me`, {
            headers: { "Authorization": `Bearer ${token}` },
        });

        if (resposta.status === 401) {
            // Token expirado ou inválido — volta para o login
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }

        if (!resposta.ok) {
            throw new Error("Erro ao buscar dados do usuário.");
        }

        const dados = await resposta.json();

        const nome = dados.aluno_nome || dados.sub || "Usuário";
        document.getElementById("boas-vindas").innerText = `Bem-vinda, ${nome}!`;
        document.getElementById("nome-usuario").innerText = nome;

        // Salva o nome para uso em outras páginas se necessário
        localStorage.setItem("user_name", nome);
    } catch {
        // Servidor fora do ar — exibe o nome em cache se existir
        const nomeSalvo = localStorage.getItem("user_name") || "Usuário";
        document.getElementById("boas-vindas").innerText = `Bem-vinda, ${nomeSalvo}!`;
        document.getElementById("nome-usuario").innerText = nomeSalvo;
    }
}

document.getElementById("btnLogout").addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_name");
    window.location.href = "login.html";
});
