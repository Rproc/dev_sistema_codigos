// Pegar os elementos do HTML/CSS com
// querySelector() -> DOM

const titulo = document.querySelector("#titulo");

const descricao = document.querySelector("#descricao");

const btnTexto = document.querySelector(".btn");

const btnDestaque = document.querySelector(".destaque");

const btnTroca = document.querySelector("#btnCor");
// Evento ao clicar no texto
// Aqui mudaremos o titulo

btnTexto.addEventListener("click", () => {
	titulo.textContent = "Aula 05";
	descricao.textContent = "Raphamengo";
});

btnDestaque.addEventListener("click", function () {
	descricao.classList.toggle("destaqueAtivo");
});

// Trocar cor de fundo
btnTroca.addEventListener("click", () => {
	const cores = [
		"red",
		"green",
		"blue",
		"pink",
		"purple",
		"orange",
		"yellow",
		"#ff36ab",
		"#e3f2fd",
		"#7c6a0a",
	];

	const corAtual = document.body.style.backgroundColor;
	let novaCor = cores[Math.floor(Math.random() * cores.length)];

	while (novaCor === corAtual) {
		novaCor = cores[Math.floor(Math.random() * cores.length)];
	}
	document.body.style.backgroundColor = novaCor;
});
