const form =
    document.getElementById("loginForm");

form.addEventListener("submit", (e) => {

    e.preventDefault();

    window.location.href = "dashboard.html";

});