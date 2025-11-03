const API_URL = "http://127.0.0.1:5000";

/**
 * Função para listar todos os usuários
 *
 * @returns {Promise<void>} Promise que resolve quando a lista for carregada
 */
async function listarUsuarios() {
	try {
		const resp = await fetch(`${API_URL}/usuarios`);
		const dados = await resp.json();

		if (resp.ok) {
			const tbody = document.querySelector("#tabelaUsuarios tbody");
			tbody.innerHTML = "";
			dados.dados.forEach((u) => {
				const tr = document.createElement("tr");
				tr.innerHTML = `<td>${u.id}</td><td>${u.nome}</td><td>${u.email}</td>`;
				tbody.appendChild(tr);
			});
		}
	} catch (erro) {
		alert("Erro ao listar usuários: " + erro.message);
	}
}
async function cadastrarUsuario(event) {
	event.preventDefault();
	const nome = document.getElementById("nome").value;
	const email = document.getElementById("email").value;
	const senha = document.getElementById("senha").value;

	// console.log({ nome, email, senha });
	const dados = { nome, email, senha };

	try {
		const resp = await fetch(`${API_URL}/usuarios`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(dados),
		});

		const resultado = await response.json();

		if (resp.ok) {
			alert("Usuário cadastrado!");
			document.getElementById("form-cadastro").reset();
			listarUsuarios();
		} else {
			const erro = await resp.json();
			alert(erro.erro);
		}
	} catch (erro) {
		alert("Erro ao cadastrar usuário: " + erro.message);
	}
}
async function deletarUsuario(id) {
	if (!confirm("Excluir este usuário?")) return;
	await fetch(`${API_URL}/usuarios/${id}`, { method: "DELETE" });
	listarUsuarios();
}
// Executa quando a página termina de carregar
// window.onload é um evento que dispara quando todo o HTML foi carregado
window.onload = function () {
	// Carrega a lista de usuários automaticamente
	listarUsuarios();
};
