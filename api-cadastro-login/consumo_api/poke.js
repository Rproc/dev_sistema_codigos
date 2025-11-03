const API_URL = "https://pokeapi.co/api/v2/pokemon/";
const form = document.getElementById("formPokemon");
const inputNome = document.getElementById("nomePokemon");
const resultado = document.getElementById("resultado");

form.addEventListener("submit", (e) => {
	e.preventDefault(); // impede o recarregamento da página

	const nome = inputNome.value.trim().toLowerCase();

	if (!nome) {
		resultado.innerHTML = "<p>Por favor, digite um nome.</p>";
		return;
	}

	fetch(API_URL + nome)
		.then((resposta) => {
			if (!resposta.ok) {
				throw new Error("Pokémon não encontrado");
			}
			return resposta.json();
		})
		.then((dados) => {
			resultado.innerHTML = `
        <h2>${dados.name} (#${dados.id})</h2>
        <img src="${dados.sprites.front_default}" alt="${dados.name}">
        <p>Tipo: ${dados.types.map((t) => t.type.name).join(", ")}</p>
      `;
			inputNome.value = ""; // limpa o campo após a busca
		})
		.catch((erro) => {
			resultado.innerHTML = `<p>${erro.message}</p>`;
		});
});
