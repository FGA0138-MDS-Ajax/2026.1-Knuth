const btnNovoTopico = document.getElementById("btnNovoTopico");
const formulario = document.getElementById("formulario");
const listaTopicos = document.getElementById("listaTopicos");

/* abrir formulário */
btnNovoTopico.addEventListener("click", () => {
    formulario.classList.toggle("escondido");
});

/* publicar tópico */
document.getElementById("publicar").addEventListener("click", () => {

    const titulo = document.getElementById("titulo").value;
    const autor = document.getElementById("autor").value;
    const disciplina = document.getElementById("disciplina").value;
    const descricao = document.getElementById("descricao").value;

    if (!titulo || !autor || !disciplina || !descricao) {
        alert("Preencha todos os campos.");
        return;
    }

    const card = document.createElement("div");
    card.classList.add("card-topico");

    card.innerHTML = `
        <h3>${titulo}</h3>
        <p class="info">👤 ${autor}</p>
        <p class="info">📚 ${disciplina}</p>
        <p>${descricao}</p>

        <button class="btn-responder">Responder</button>

        <span class="respostas">💬 0 respostas</span>
    `;

    listaTopicos.prepend(card);

    formulario.classList.add("escondido");

    document.getElementById("titulo").value = "";
    document.getElementById("autor").value = "";
    document.getElementById("disciplina").value = "";
    document.getElementById("descricao").value = "";

    /* =========================
       RESPOSTAS
    ========================= */

    const btnResponder = card.querySelector(".btn-responder");
    const contador = card.querySelector(".respostas");

    let aberto = false;
    let qtd = 0;

    const area = document.createElement("div");
    const lista = document.createElement("div");
    const textarea = document.createElement("textarea");
    const btnEnviar = document.createElement("button");

    lista.classList.add("lista-respostas");
    textarea.placeholder = "Escreva sua resposta...";
    btnEnviar.textContent = "Enviar";

    area.appendChild(lista);
    area.appendChild(textarea);
    area.appendChild(btnEnviar);

    area.style.display = "none";
    area.style.flexDirection = "column";

    card.appendChild(area);

    /* abrir/fechar */
    btnResponder.addEventListener("click", () => {
        aberto = !aberto;
        area.style.display = aberto ? "flex" : "none";
    });

    /* enviar resposta */
    btnEnviar.addEventListener("click", () => {

        const texto = textarea.value.trim();

        if (!texto) {
            alert("Escreva uma resposta.");
            return;
        }

        const p = document.createElement("p");
        p.textContent = "💬 " + texto;

        lista.appendChild(p);

        textarea.value = "";

        qtd++;
        contador.textContent = `💬 ${qtd} respostas`;
    });

});

/* pesquisa */
document.getElementById("pesquisa").addEventListener("input", (e) => {

    const texto = e.target.value.toLowerCase();

    document.querySelectorAll(".card-topico").forEach(card => {

        card.style.display =
            card.textContent.toLowerCase().includes(texto)
                ? "block"
                : "none";

    });

});