function filtrarDisciplinas() {

    let input = document
        .getElementById("pesquisa")
        .value
        .toLowerCase();

    let disciplinas =
        document.querySelectorAll(".disciplina");

    disciplinas.forEach(card => {

        let texto =
            card.innerText.toLowerCase();

        if (texto.includes(input)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }

    });
}