// Explicação 101 (Rápido)
// DOM (Document Object Model)
// Basicamente, pega o HTML e
// transforma em uma arvore

// document
//  ┗ html
//  ┃ ┣ body
//  ┃ ┃ ┣ form
//  ┃ ┃ ┣ h1
//  ┃ ┃ ┗ ul
//  ┃ ┗ head
// O JS pode acessar e alterar qualquer parte
// dessa arvore

// let/var/const
const form = document.getElementById("formTarefa");

const inputTarefa = document.getElementById("tarefa");

const lista = document.getElementById("listaTarefas");

form.addEventListener("submit", function (e) {
	e.preventDefault();
	// impede o recarregamento automatico
	// da pagina

	// Pegar o campo
	const texto = inputTarefa.value.trim();
	// verificar se esta vazio
	if (texto === "") {
		alert("Informe uma tarefa");
		return;
	}
	// se existir uma tarefa, a ideia é
	// colocar na lista

	// criar um elemento <li>
	let novaTarefa = document.createElement("li");
	// Inserir o texto dentro do elemento
	novaTarefa.textContent = texto;
	// Criação do botão
	let botaoDelete = document.createElement("button");
	botaoDelete.textContent = "Deletar";
	botaoDelete.classList.add("btn-delete");
	// Clicou no remover -> remove o item
	botaoDelete.addEventListener("click", function () {
		novaTarefa.remove();
		// DOM que remove o <li>
	});
	// Adiciona o novo item <li> na lista <ul>

	// Adicionar botão dentro de cada <li>
	novaTarefa.appendChild(botaoDelete);
	// adiciona <li> no <ul>
	lista.appendChild(novaTarefa);
	// limpar o campo após adicionar
	inputTarefa.value = "";
	// leva o foco de volta para o campo de
	// escrita
	inputTarefa.focus();
});
