const form =
    document.getElementById("loginForm");

form.addEventListener("submit", (e) => {

    e.preventDefault();

    
    const email = form.querySelector('input[type="email"]').value;
    // Extrai o nome antes do '@' apenas para simular o nome da pessoa
    const nomeIdentificado = email.split('@')[0]; 
    alert("Login realizado!");
        // token
    localStorage.setItem("access_token", "token_simulado_123");
    
    // Leva o usuário para a dashboard
    window.location.href = "dashboard.html";


});



   

    