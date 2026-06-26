const cargoUsuario = "Aluno";
// Troque para "Professor" ou "Monitor" para testar

const btnNovaDuvida =
    document.getElementById("btnNovaDuvida");

const formulario =
    document.getElementById("formulario");

const lista =
    document.getElementById("listaDuvidas");

btnNovaDuvida.addEventListener("click", function() {

    formulario.classList.toggle("escondido");

});

document.getElementById("publicar")
    .addEventListener("click", function() {

        const titulo =
            document.getElementById("titulo").value.trim();

        const descricao =
            document.getElementById("descricao").value.trim();

        const atribuida =
            document.getElementById("atribuida").value;

        if (titulo === "" || descricao === "") {

            alert("Preencha todos os campos.");
            return;
        }

        const card = document.createElement("div");

        card.className = "card";

        let botaoResolver = "";

        if (!(cargoUsuario === "Aluno" &&
                atribuida ===
                "Apenas professores e monitores")) {

            botaoResolver =
                `<button class="btnResolver">
                Resolver
            </button>`;
        }

        card.innerHTML = `
        <h3>${titulo}</h3>

        <p class="info">
            <strong>Atribuída a:</strong>
            ${atribuida}
        </p>

        <p class="info">
            <strong>Status:</strong>
            <span class="status status-aberta">
                Aberta
            </span>
        </p>

        <p>${descricao}</p>

        <div class="respostas"></div>

        <textarea
            class="campo-resposta"
            placeholder="Digite sua resposta">
        </textarea>

        <button class="btnResponder">
            Responder
        </button>

        ${botaoResolver}
    `;

        lista.prepend(card);

        const btnResponder =
            card.querySelector(".btnResponder");

        btnResponder.addEventListener("click", function() {

            const status =
                card.querySelector(".status");

            if (status.textContent === "Resolvida") {

                alert("Essa dúvida já foi resolvida.");
                return;
            }

            const campo =
                card.querySelector(".campo-resposta");

            const texto = campo.value.trim();

            if (texto === "") {

                alert("Digite uma resposta.");
                return;
            }

            const respostas =
                card.querySelector(".respostas");

            const resposta =
                document.createElement("div");

            resposta.className = "resposta";

            resposta.innerHTML = `
            <p>
                <strong>Maria (Aluno)</strong>
            </p>

            <p>${texto}</p>
        `;

            respostas.appendChild(resposta);

            campo.value = "";
        });

        const btnResolver =
            card.querySelector(".btnResolver");

        if (btnResolver) {

            btnResolver.addEventListener("click", function() {

                const status =
                    card.querySelector(".status");

                status.textContent = "Resolvida";

                status.classList.remove("status-aberta");

                status.classList.add("status-resolvida");

                alert("Dúvida resolvida.");
            });
        }

        document.getElementById("titulo").value = "";
        document.getElementById("descricao").value = "";

        formulario.classList.add("escondido");
    });