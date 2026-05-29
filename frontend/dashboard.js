// Pega o botão com o ID correto do HTML
const btnSair = document.getElementById("btnSair");

btnSair.addEventListener("click", () => {
    // Limpa os dados e volta pro login
    localStorage.removeItem("access_token"); 
    localStorage.removeItem("user_name");    
    window.location.href = "login.html";     
});