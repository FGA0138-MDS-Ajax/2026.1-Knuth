
const token = localStorage.getItem("access_token");
// Pega o nome salvo no login (ou usa "Usuário" como padrão)
const nomeSalvo = localStorage.getItem("user_name") || "Usuário";

if (!token) {
    // Se não tiver token, redireciona para a tela de login
    window.location.href = "login.html";
} else {
    // Se tiver token, atualiza os textos da página com o nome
    document.getElementById("boas-vindas").innerText = `Bem-vinda, ${nomeSalvo}!`;
    document.getElementById("nome-usuario").innerText = nomeSalvo;
}

// Configura o funcionamento do botão "Sair da conta"
document.getElementById("btnLogout").addEventListener("click", () => {
    localStorage.removeItem("access_token"); // Apaga o token
    localStorage.removeItem("user_name");    // Apaga o nome
    window.location.href = "login.html";     // Volta para o login
});