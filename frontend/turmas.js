const turmas = [
    "mds",
    "estrutura de dados",
    "banco de dados"
];

const entrarButtons =
    document.querySelectorAll(".entrar");

const novaTurma =
    document.getElementById("novaTurma");

entrarButtons.forEach((button) => {

    button.addEventListener("click", () => {

        alert("Abrindo turma...");

    });

});

novaTurma.addEventListener("click", () => {

    const nome =
        prompt("Digite o nome da nova turma:");

    if (!nome) {

        alert("Digite um nome para a turma.");
        return;

    }

    alert(`Turma "${nome}" criada com sucesso!`);

});

document
    .getElementById("buscarTurma")
    .addEventListener("click", () => {

        const busca =
            document
            .getElementById("buscaTurma")
            .value
            .toLowerCase()
            .trim();

        const mensagem =
            document.getElementById("mensagemErro");

        if (busca === "") {

            mensagem.textContent =
                "Digite o nome de uma turma.";

            return;
        }

        if (!turmas.includes(busca)) {

            mensagem.textContent =
                "Turma não encontrada.";

            return;
        }

        mensagem.textContent =
            "Turma encontrada!";
    });