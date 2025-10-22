const API_URL = "http://127.0.0.1:5000";

async function listarUsuarios() {
	const resp = await fetch(`${API_URL}/usuarios`);
	const dados = await resp.json();
	const tbody = document.querySelector("#tabelaUsuarios tbody");
	tbody.innerHTML = "";
	dados.dados.forEach((u) => {
		const tr = document.createElement("tr");
		tr.innerHTML = `
      <td>${u.id}</td>
      <td>${u.nome}</td>
      <td>${u.email}</td>
      <td><button onclick="deletarUsuario(${u.id})">Excluir</button></td>`;
		tbody.appendChild(tr);
	});
}

document
	.getElementById("formCadastro")
	.addEventListener("submit", async (e) => {
		e.preventDefault();
		const nome = nome.value;
		const email = email.value;
		const senha = senha.value;

		const resp = await fetch(`${API_URL}/usuarios`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ nome, email, senha }),
		});

		if (resp.ok) {
			alert("Usuário cadastrado!");
			listarUsuarios();
			e.target.reset();
		} else {
			const erro = await resp.json();
			alert(erro.erro);
		}
	});

async function deletarUsuario(id) {
	if (!confirm("Excluir este usuário?")) return;
	await fetch(`${API_URL}/usuarios/${id}`, { method: "DELETE" });
	listarUsuarios();
}

listarUsuarios();
