function filtrarDisciplinas() {

    let input = document
        .getElementById("pesquisa")
        .value
        .toLowerCase();

    let disciplinas =
        document.querySelectorAll(".disciplina");

    let encontrou = false;

    disciplinas.forEach(card => {

        let texto =
            card.innerText.toLowerCase();

        if (texto.includes(input)) {

            card.style.display = "block";
            encontrou = true;

        } else {

            card.style.display = "none";

        }

    });

    let mensagem =
        document.getElementById("mensagem-sem-resultados");

    if (encontrou) {

        mensagem.style.display = "none";

    } else {

        mensagem.style.display = "block";

    }
}
