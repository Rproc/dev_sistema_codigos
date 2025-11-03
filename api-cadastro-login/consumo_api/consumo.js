const API_URL = "https://jsonplaceholder.typicode.com/users";
const btnCarregar = document.getElementById("btnCarregar");
const lista = document.getElementById("listaUsuarios");

// Quando o botão for clicado, chamamos a função que busca os dados
btnCarregar.addEventListener("click", () => {
	fetch(API_URL) // Faz a requisição HTTP para a API
		.then((resposta) => resposta.json()) // Converte a resposta em JSON
		.then((usuarios) => {
			// Limpa a lista antes de preencher
			lista.innerHTML = "";

			// Percorre o array de usuários retornado pela API
			usuarios.forEach((usuario) => {
				const item = document.createElement("li");
				item.textContent = `${usuario.name} (${usuario.email})`;
				lista.appendChild(item);
			});
		})
		.catch((erro) => {
			console.error("Erro ao buscar usuários:", erro);
			lista.innerHTML = "<li>Erro ao carregar os dados.</li>";
		});
});
