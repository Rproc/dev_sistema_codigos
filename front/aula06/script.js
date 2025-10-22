async function listarUsuarios() {
	const resp = await fetch("http://127.0.0.1:5000/usuarios");
	const dados = await resp.json();
	const tbody = document.querySelector("#tabelaUsuarios tbody");
	tbody.innerHTML = "";
	dados.dados.forEach((u) => {
		const tr = document.createElement("tr");
		tr.innerHTML = `<td>${u.id}</td><td>${u.nome}</td><td>${u.email}</td>`;
		tbody.appendChild(tr);
	});
}

listarUsuarios();
