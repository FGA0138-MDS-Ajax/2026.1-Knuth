const lista = document.getElementById("listaDuvidas");

const usuarioLogado = {
    nome: "Maria Eduarda",
    cargo: "Professor"
};

document
    .getElementById("publicar")
    .addEventListener("click", () => {

        const titulo =
            document.getElementById("titulo").value;

        const descricao =
            document.getElementById("descricao").value;

        const atribuida =
            document.getElementById("atribuida").value;

        if (titulo === "" || descricao === "") {
            alert("Preencha todos os campos");
            return;
        }

        const card = document.createElement("div");
        card.classList.add("card");

        card.innerHTML = `
            <h3>${titulo}</h3>

            <p><strong>Autor:</strong>
            ${usuarioLogado.nome} (${usuarioLogado.cargo})
            </p>

            <p><strong>Status:</strong>
            <span class="status">Aberta</span>
            </p>

            <p><strong>Atribuída a:</strong>
            ${atribuida}</p>

            <p>${descricao}</p>

            <hr>

            <div class="respostas"></div>

            <textarea
                class="campoResposta"
                placeholder="Digite sua resposta">
            </textarea>

            <button class="btnResponder">
                Responder
            </button>

            <button class="btnResolver">
                Resolver
            </button>
        `;

        lista.prepend(card);

        const campo =
            card.querySelector(".campoResposta");

        const btnResponder =
            card.querySelector(".btnResponder");

        const btnResolver =
            card.querySelector(".btnResolver");

        const respostas =
            card.querySelector(".respostas");

        // Regra para esconder resposta
        if (
            atribuida === "Apenas professores e monitores" &&
            usuarioLogado.cargo === "Aluno"
        ) {

            campo.style.display = "none";
            btnResponder.style.display = "none";
        }

        btnResponder.addEventListener("click", () => {

            const texto = campo.value;

            if (texto === "") {
                alert("Digite uma resposta.");
                return;
            }

            const resposta =
                document.createElement("div");

            resposta.classList.add("resposta");

            resposta.innerHTML = `
                <strong>
                    ${usuarioLogado.nome}
                    (${usuarioLogado.cargo})
                </strong>

                <p>${texto}</p>
            `;

            respostas.appendChild(resposta);

            campo.value = "";
        });

        btnResolver.addEventListener("click", () => {

            card.querySelector(".status").textContent =
                "Resolvida";

            campo.disabled = true;
            btnResponder.disabled = true;
        });

        document.getElementById("titulo").value = "";
        document.getElementById("descricao").value = "";
    });