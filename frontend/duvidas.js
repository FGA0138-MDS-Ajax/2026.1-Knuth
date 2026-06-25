const btnNovaDuvida = document.getElementById("btnNovaDuvida");
const formulario = document.getElementById("formulario");
const lista = document.getElementById("listaDuvidas");

btnNovaDuvida.addEventListener("click", () => {
    formulario.classList.toggle("escondido");
});

document.getElementById("publicar").addEventListener("click", async () => {
    // 1. Captura os valores
    const descricao = document.getElementById("descricao").value;

    if (descricao === "") {
        alert("Preencha o campo de descrição (texto da pergunta).");
        return;
    }

    // 2. Monta o objeto exatamente como o Swagger exige
    const novaPergunta = {
        texto: descricao, 
        turma_id: 1, // Ajuste para o ID da turma desejada
        is_restrita_professor: false,
        is_restrita_monitor: false
    };

    // 3. Envia para o Backend
    try {
        const response = await fetch("http://127.0.0.1:8000/perguntas/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify(novaPergunta)
        });

        if (response.ok) {
            const data = await response.json();

            // 4. Cria o card na tela com o retorno do banco
            const card = document.createElement("div");
            card.classList.add("card");
            card.innerHTML = `
                <h3>Pergunta #${data.id}</h3>
                <p>${data.texto}</p>
            `;
            lista.prepend(card);

            // Limpa campos
            document.getElementById("descricao").value = "";
            formulario.classList.add("escondido");
            alert("Pergunta publicada com sucesso!");
        } else {
            alert("Erro ao publicar no banco de dados.");
        }
    } catch (error) {
        console.error("Erro na comunicação:", error);
    }
});