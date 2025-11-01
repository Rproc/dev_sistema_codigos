// Seleciona elementos do DOM usando querySelector
const titulo = document.querySelector("#titulo"); // Seleciona o elemento pelo ID
const descricao = document.querySelector("#descricao"); // Seleciona o parágrafo
const botaoTexto = document.querySelector(".btn"); // Seleciona o primeiro botão com classe .btn
const botaoDestaque = document.querySelector(".destaque"); // Seleciona o botão de destaque

// Evento: ao clicar, o texto do parágrafo muda
botaoTexto.addEventListener("click", () => {
	descricao.textContent = "O texto foi alterado com sucesso!";
	titulo.textContent = "Texto Modificado!";
});

// Evento: ao clicar, alterna a classe CSS no título
botaoDestaque.addEventListener("click", () => {
	titulo.classList.toggle("destaqueAtivo");
	// .toggle() adiciona a classe se ela não existir, e remove se já existir
});
