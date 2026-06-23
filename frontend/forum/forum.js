const btnNovoTopico =
    document.getElementById("btnNovoTopico");

const formulario =
    document.getElementById("formulario");

const listaTopicos =
    document.getElementById("listaTopicos");

/* Abrir e fechar formulário */

btnNovoTopico.addEventListener("click", () => {

    formulario.classList.toggle("escondido");

});

/* Publicar tópico */

document
    .getElementById("publicar")
    .addEventListener("click", () => {

        const titulo =
            document.getElementById("titulo").value;

        const autor =
            document.getElementById("autor").value;

        const disciplina =
            document.getElementById("disciplina").value;

        const descricao =
            document.getElementById("descricao").value;

        if (
            titulo === "" ||
            autor === "" ||
            disciplina === "" ||
            descricao === ""
        ) {
            alert("Preencha todos os campos.");
            return;
        }

        const card =
            document.createElement("div");

        card.classList.add("card-topico");

        card.innerHTML = `
            <h3>${titulo}</h3>

            <p class="info">
                👤 ${autor}
            </p>

            <p class="info">
                📚 ${disciplina}
            </p>

            <p>
                ${descricao}
            </p>

            <span class="respostas">
                💬 0 respostas
            </span>
        `;

        listaTopicos.prepend(card);

        document.getElementById("titulo").value = "";
        document.getElementById("autor").value = "";
        document.getElementById("disciplina").value = "";
        document.getElementById("descricao").value = "";

        formulario.classList.add("escondido");

    });

/* Pesquisa de tópicos */

document
    .getElementById("pesquisa")
    .addEventListener("input", (e) => {

        const texto =
            e.target.value.toLowerCase();

        const topicos =
            document.querySelectorAll(".card-topico");

        topicos.forEach((topico) => {

            const conteudo =
                topico.textContent.toLowerCase();

            if (conteudo.includes(texto)) {
                topico.style.display = "block";
            } else {
                topico.style.display = "none";
            }

        });

    });