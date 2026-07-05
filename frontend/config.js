// URL base da API — altere aqui se a porta do backend mudar
const API_BASE_URL = "http://localhost:8000";

function decodeJWT(token) {
    try {
        const base64Url = token.split('.')[1];
        let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        while (base64.length % 4) {
            base64 += '=';
        }
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

function getLoggedUserRole() {
    const token = localStorage.getItem("access_token");
    if (!token) return null;
    const payload = decodeJWT(token);
    if (!payload) return null;
    if (payload.is_admin) return "admin";
    if (payload.is_professor) return "professor";
    if (payload.is_aluno) return "aluno";
    return null;
}

async function initSidebar() {
    const sidebarNome = document.getElementById("sidebarNome");
    const sidebarCargo = document.getElementById("sidebarCargo");
    
    // Configura o link ativo com base no nome do arquivo
    const filename = window.location.pathname.split("/").pop();
    const links = {
        "dashboard.html": "menuGeral",
        "dashboard-academico.html": "menuAcademico",
        "turmas.html": "menuTurmas",
        "turma-detalhe.html": "menuTurmas",
        "disciplinas.html": "menuDisciplinas",
        "disciplina-detalhe.html": "menuDisciplinas",
        "duvidas.html": "menuDuvidas"
    };
    
    const activeId = links[filename];
    if (activeId) {
        // Remove classe active antiga e adiciona ao correto
        document.querySelectorAll(".sidebar ul li a").forEach(a => a.classList.remove("active"));
        const el = document.getElementById(activeId);
        if (el) el.classList.add("active");
    }
    
    const token = localStorage.getItem("access_token");
    if (!token) return;
    
    let profileData = null;
    try {
        const cached = localStorage.getItem("user_profile_cache");
        if (cached) {
            profileData = JSON.parse(cached);
        } else {
            const res = await fetch(`${API_BASE_URL}/me`, {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (res.status === 401) {
                localStorage.removeItem("access_token");
                localStorage.removeItem("user_profile_cache");
                window.location.href = "login.html";
                return;
            }
            if (res.ok) {
                profileData = await res.json();
                localStorage.setItem("user_profile_cache", JSON.stringify(profileData));
            }
        }
    } catch (e) {
        console.error("Erro ao carregar perfil para a sidebar", e);
    }
    
    if (profileData) {
        const nome = profileData.aluno_nome || profileData.professor_nome || profileData.sub.split("@")[0];
        const cargo = profileData.is_professor ? "Professor" : (profileData.is_admin ? "Administrador" : "Aluno");
        
        if (sidebarNome) sidebarNome.textContent = nome;
        if (sidebarCargo) sidebarCargo.textContent = cargo;
        
        localStorage.setItem("user_name", nome);
    } else {
        const nomeSalvo = localStorage.getItem("user_name") || "Usuário";
        if (sidebarNome) sidebarNome.textContent = nomeSalvo;
    }
    
    // Configura o evento de Sair
    const btnSair = document.getElementById("btnSair");
    if (btnSair) {
        btnSair.addEventListener("click", (e) => {
            e.preventDefault();
            localStorage.removeItem("access_token");
            localStorage.removeItem("user_name");
            localStorage.removeItem("user_profile_cache");
            window.location.href = "login.html";
        });
    }
}

document.addEventListener("DOMContentLoaded", initSidebar);

