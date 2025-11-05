const API_URL = "http://localhost:5000";

function mostrarMensagem(texto) {
	const msgDiv = document.querySelector("#mensagem");

	msgDiv.textContent = texto;
	msgDiv.style.display = "block";

	setTimeout(() => {
		msgDiv.style.display = "none";
	}, 5000);
}

async function cadastrarUsuario(event) {
	event.preventDefault();

	const nome = document.querySelector("#nome").value;
	const email = document.querySelector("#email").value;
	const senha = document.querySelector("#senha").value;

	const dados = { nome, email, senha };

	try {
		const response = await fetch(`${API_URL}/usuarios`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(dados),
		});
		// Esperando o resultado da promessa
		const resultado = await response.json();

		if (response.ok) {
			// aqui entraria mostrar na div
			// alert("Usuario criado com sucesso");
			mostrarMensagem(resultado.mensagem);
			document.querySelector("#formCadastro").reset();
		} else {
			// aqui entraria mostrar erro na div
			alert("Erro ao cadastrar usuario");
		}
	} catch (erro) {
		// mostrar erro de servidor na div
		alert("Erro ao conectar com o servidor" + erro.mensagem);
	}
}

async function listarUsuarios() {
	// Pegar a tabela
	const tabela = document.querySelector("#tabela-usuarios");
	// Se for uma atualização, esconde ela para alterar
	tabela.style.display = "none";

	try {
		const response = await fetch(`${API_URL}/usuarios`);
		const dados = await response.json();

		if (response.ok) {
			// Pega o corpo (body) da tabela
			const conteudoTabela = document.querySelector("#tbody-usuarios");

			//Limpa o conteudo
			conteudoTabela.innerHTML = "";

			// Caso não tenha usuarios cadastrados
			if (dados.total === 0) {
				conteudoTabela.innerHTML = `<tr><td colspan="4" style="text-align: center;"> 
				Nenhum usuário cadastrado</td></tr>`;
			}
			// Se há usuarios cadastrados, devo montar a tabela dinamicamente
			else {
				dados.dados.forEach((usuario) => {
					// formatar data
					let dataFormatada = "N/A";

					const dataObj = new Date(usuario.criado);

					// verificar se a data é valida
					dataFormatada = dataObj.toLocaleDateString("pt-BR");

					// cria uma nova linha (table row)
					const tr = document.createElement("tr");

					// escreve a tabela no HTML
					tr.innerHTML = `
						<td>${usuario.id}</td>
						<td>${usuario.nome}</td>
						<td>${usuario.email}</td>
						<td>${dataFormatada}</td>
					`;

					conteudoTabela.appendChild(tr);
				});
			}

			tabela.style.display = "table";
		} else {
			mostrarMensagem(dados.erro);
		}
	} catch (erro) {
		mostrarMensagem("Erro ao carregar usuarios " + erro.mensagem);
	}
}
