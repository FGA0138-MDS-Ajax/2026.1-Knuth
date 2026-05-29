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

    if (nome) {

        alert(`Turma "${nome}" criada com sucesso!`);
    }

});