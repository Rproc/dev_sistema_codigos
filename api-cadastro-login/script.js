const API_URL = "http://localhost:5000";

// para otimizar o tempo

function mostrarMensagem(mensagem) {
	// pegar o elemento do HTML (onde vamos mostrar a msg)
	const divMsg = document.querySelector("#mensagem");

	divMsg.textContent = mensagem;

	// mostrar a div
	divMsg.style.display = "block";

	// vc quer que a div fique para sempre na tela?
	setTimeout(() => {
		divMsg.style.display = "none";
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
			mostrarMensagem("Usuario cadastrado com sucesso");
			document.querySelector("#formCadastro").reset();
		} else {
			// aqui entraria mostrar erro na div
			mostrarMensagem("Erro ao cadastrar usuario");
		}
	} catch (erro) {
		// mostrar erro de servidor na div
		mostrarMensagem("Erro ao conectar com o servidor" + erro.message);
	}
}

async function listarUsuarios() {
	const loading = document.querySelector("#loading");
	loading.style.display = "block";
	// primeira coisa: pegar a tabela
	const tabela = document.querySelector("#tabela-usuarios");

	// segunda coisa: esconder a tabela
	tabela.style.display = "none";

	try {
		// primeira coisa no try: fazer a requisição

		const response = await fetch(`${API_URL}/usuarios`);
		const resultado = await response.json();

		if (response.ok) {
			// ideia: pegar a tabela (sendo apenas o body)
			const tbody = document.querySelector("#conteudo-tabela");

			// primeira coisa ao pegar o tbody
			tbody.innerHTML = "";

			if (resultado.total === 0) {
				// Informar que não tem usuarios
				// tabela que diz que não tem usuarios
				tbody.innerHTML = `
				<tr><td colspan="5" 
				style="text-align: center;">
				Nenhum usuário cadastrado</td></tr>`;
			} else {
				// montar a tabela de usuarios
				resultado.dados.forEach((usuario) => {
					let dataFormatada = "N/A";
					if (usuario.criado) {
						try {
							// primeiro cria um objeto Date
							const data = new Date(usuario.criado);
							if (!isNaN(data.getTime())) {
								dataFormatada =
									data.toLocaleDateString("pt-BR");
							}
						} catch (erro) {
							console.error("Erro ao formatar data " + erro);
						}
					}
					// criar a linha
					const tr = document.createElement("tr");

					// Vamos escrever os dados na linha
					tr.innerHTML = `
						<td>${usuario.id}</td>
						<td>${usuario.nome}</td>
						<td>${usuario.email}</td>
						<td>${dataFormatada}</td>
						<td class="acoes">
							<button class="btn-editar"
							onclick=
							editarUsuario(${usuario.id})>
							Editar</button>
							<button class="btn-excluir" 
							onclick=
							"deletarUsuario(${usuario.id}, 
							'${usuario.nome}')">🗑️</button>
						</td>
						`;

					// adicionar ao coropo da tabela
					tbody.appendChild(tr);
				});
			}
			tabela.style.display = "table";
		}
	} catch (erro) {
		mostrarMensagem("Erro ao carregar usuarios " + erro);
	} finally {
		// Independentemente de sucesso ou erro
		loading.style.display = "none";
	}
}

async function deletarUsuario(id_usuario, nome) {
	// confirm() mostra uma caixa de dialogo
	// de confirmação (Ok, cancelar)
	// caminho triste

	if (
		!confirm(
			`Você está preste a excluir o usuario ${nome}. Deseja proseguir?`
		)
	) {
		// se cancelar
		return;
	}
	// confirma a exclusão
	try {
		const response = await fetch(
			`${API_URL}/usuarios/
			${id_usuario}`,
			{
				method: "DELETE",
			}
		);
		const resultado = await response.json();

		if (response.ok) {
			mostrarMensagem(resultado.mensagem);
			listarUsuarios();
		} else {
			// aqui são os erros que vem da rota
			// da api
			mostrarMensagem(resultado.erro);
		}
	} catch (erro) {
		// aqui fica o erro que vem da requisição
		mostrarMensagem("Erro ao deletar usuário: " + erro);
	}
}

async function editarUsuario(id_usuario) {
	const novoNome = prompt("Digite o novo nome:");

	// verificar se o novo nome esta compativel
	// com os requisitos da api

	if (!novoNome || novoNome.trim().length < 3) {
		mostrarMensagem(`Nome inválido, 
			pois deve ter mais de 2 caracteres`);
		return;
	}
	try {
		const response = await fetch(
			`${API_URL}/usuarios/
			${id_usuario}`,
			{
				method: "PATCH",
				headers: {
					"Content-type": "application/json",
				},
				body: JSON.stringify({
					nome: novoNome.trim(),
				}),
			}
		);

		const resultado = await response.json();

		if (response.ok) {
			mostrarMensagem(resultado.mensagem);
			listarUsuarios();
		} else {
			mostrarMensagem(resultado.erro);
		}
	} catch (erro) {
		mostrarMensagem("Erro ao atualizar o usuário: " + erro);
	}
}

// Quando a pagina termina de carregar, chama a função
// "onload" é um evento que dispara quando todo o HTML
// é carregado
window.onload = function () {
	listarUsuarios();
};
