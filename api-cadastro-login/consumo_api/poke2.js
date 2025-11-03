const API_URL = "https://pokeapi.co/api/v2/pokemon/";
const form = document.getElementById("formPokemon");
const inputNome = document.getElementById("nomePokemon");
const resultado = document.getElementById("resultado");

form.addEventListener("submit", (event) => {
	event.preventDefault();

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
			const nomeFormatado =
				dados.name.charAt(0).toUpperCase() + dados.name.slice(1);
			const tipos = dados.types.map((t) => t.type.name).join(", ");
			const altura = (dados.height / 10).toFixed(1); // decímetros → metros
			const peso = (dados.weight / 10).toFixed(1); // hectogramas → kg

			resultado.innerHTML = `
        <h2>${nomeFormatado} (#${dados.id})</h2>
        <img src="${dados.sprites.front_default}" alt="${dados.name}">
        <p>Tipo: ${tipos}</p>
        <p>Altura: ${altura} m</p>
        <p>Peso: ${peso} kg</p>
      `;

			inputNome.value = "";
		})
		.catch((erro) => {
			resultado.innerHTML = `<p>${erro.message}</p>`;
		});
});
