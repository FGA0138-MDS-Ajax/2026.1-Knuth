const btnNovaDuvida = document.getElementById("btnNovaDuvida");
const formulario = document.getElementById("formulario");
const lista = document.getElementById("listaDuvidas");

const filtro =
    document.getElementById("filtroPrioridade");

let duvidas = [];

btnNovaDuvida.addEventListener("click", () => {
    formulario.classList.toggle("escondido");
});

function renderizarDuvidas() {

    lista.innerHTML = "";

    let resultado = duvidas;

    if (filtro.value !== "Todas") {
        resultado = duvidas.filter(
            duvida => duvida.prioridade === filtro.value
        );
    }

    resultado.forEach((duvida) => {

        const card = document.createElement("div");

        card.classList.add("card");

        card.innerHTML = `
            <h3>${duvida.titulo}</h3>

            <p class="info">
                📚 ${duvida.disciplina}
            </p>

            <p class="info">
                ⚠️ Prioridade: ${duvida.prioridade}
            </p>

            <p class="info">
                📌 Status: ${duvida.status}
            </p>

            <p>
                ${duvida.descricao}
            </p>

            <select class="alterarStatus">
                <option value="Aberta" ${duvida.status === "Aberta" ? "selected" : ""}>
                    Aberta
                </option>

                <option value="Em andamento" ${duvida.status === "Em andamento" ? "selected" : ""}>
                    Em andamento
                </option>

                <option value="Resolvida" ${duvida.status === "Resolvida" ? "selected" : ""}>
                    Resolvida
                </option>
            </select>
        `;

        const selectStatus =
            card.querySelector(".alterarStatus");

        selectStatus.addEventListener("change", (e) => {
            duvida.status = e.target.value;
        });

        lista.prepend(card);
    });
}

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

        const status =
            document.getElementById("status").value;

        if (
            titulo === "" ||
            disciplina === "" ||
            prioridade === "" ||
            descricao === ""
        ) {
            alert("Preencha todos os campos.");
            return;
        }

        duvidas.unshift({
            titulo,
            disciplina,
            prioridade,
            descricao,
            status
        });

        renderizarDuvidas();

        document.getElementById("titulo").value = "";
        document.getElementById("disciplina").value = "";
        document.getElementById("prioridade").value = "";
        document.getElementById("descricao").value = "";

        formulario.classList.add("escondido");
    });

filtro.addEventListener("change", renderizarDuvidas);