const btnNovaDuvida =
    document.getElementById("btnNovaDuvida");

const formulario =
    document.getElementById("formulario");

const lista =
    document.getElementById("listaDuvidas");

btnNovaDuvida.addEventListener("click", () => {

    formulario.classList.toggle("escondido");

});

document
    .getElementById("publicar")
    .addEventListener("click", () => {

        const titulo =
            document.getElementById("titulo").value;

        const disciplina =
            document.getElementById("disciplina").value;

        const prioridade =
            document.getElementById("prioridade").value;

        const descricao =
            document.getElementById("descricao").value;

        if (
            titulo === "" ||
            disciplina === "" ||
            prioridade === "" ||
            descricao === ""
        ) {
            alert("Preencha todos os campos.");
            return;
        }

        const card =
            document.createElement("div");

        card.classList.add("card");

        card.innerHTML = `
        <h3>${titulo}</h3>

        <p class="info">
        📚 ${disciplina}
        </p>

        <p class="info">
        ⚠️ Prioridade: ${prioridade}
        </p>

        <p>${descricao}</p>
    `;

        lista.prepend(card);

        document.getElementById("titulo").value = "";
        document.getElementById("disciplina").value = "";
        document.getElementById("prioridade").value = "";
        document.getElementById("descricao").value = "";

        formulario.classList.add("escondido");

    });