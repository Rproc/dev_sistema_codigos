// URL base da API - ALTERE se sua API estiver em outro endereço
const API_URL = "http://localhost:5000";

// Variável para armazenar dados do usuário logado
let usuarioLogado = null;

/**
 * Função para mostrar mensagens na tela
 * @param {string} texto - Texto da mensagem
 * @param {string} tipo - Tipo da mensagem: 'sucesso' ou 'erro'
 */
function mostrarMensagem(texto, tipo) {
	// Seleciona o elemento de mensagem pelo ID
	const mensagemDiv = document.getElementById("mensagem");

	// Define o texto da mensagem
	mensagemDiv.textContent = texto;

	// Remove classes anteriores e adiciona a nova
	mensagemDiv.className = "mensagem " + tipo;

	// Mostra a mensagem
	mensagemDiv.style.display = "block";

	// Esconde a mensagem após 5 segundos
	setTimeout(() => {
		mensagemDiv.style.display = "none";
	}, 5000);
}

/**
 * Função para fazer login
 * @param {Event} event - Evento do formulário
 */
async function fazerLogin(event) {
	// Previne o comportamento padrão do formulário (recarregar a página)
	event.preventDefault();

	// Obtém os valores dos campos do formulário
	const email = document.getElementById("login-email").value;
	const senha = document.getElementById("login-senha").value;

	try {
		// Faz a requisição POST para a API
		// fetch() retorna uma Promise
		const response = await fetch(`${API_URL}/login`, {
			method: "POST", // Tipo de requisição
			headers: {
				"Content-Type": "application/json", // Informa que estamos enviando JSON
			},
			body: JSON.stringify({ email, senha }), // Converte objeto em JSON
		});

		// Converte a resposta para JSON
		const dados = await response.json();

		// Verifica se a requisição foi bem sucedida (status 200-299)
		if (response.ok) {
			// Armazena os dados do usuário logado
			usuarioLogado = dados.usuario;

			// Mostra informações do usuário
			document.getElementById("nome-logado").textContent =
				usuarioLogado.nome;
			document.getElementById("email-logado").textContent =
				usuarioLogado.email;
			document.getElementById("usuario-info").style.display = "block";

			// Esconde o formulário de login
			document.getElementById("secao-login").style.display = "none";

			// Limpa o formulário
			document.getElementById("form-login").reset();

			// Mostra mensagem de sucesso
			mostrarMensagem(dados.mensagem, "sucesso");

			// Atualiza a lista de usuários
			listarUsuarios();
		} else {
			// Se houver erro, mostra a mensagem de erro
			mostrarMensagem(dados.erro, "erro");
		}
	} catch (erro) {
		// Captura erros de rede ou outros erros
		mostrarMensagem(
			"Erro ao conectar com o servidor: " + erro.message,
			"erro"
		);
	}
}

/**
 * Função para fazer logout
 */
function logout() {
	usuarioLogado = null;
	document.getElementById("usuario-info").style.display = "none";
	document.getElementById("secao-login").style.display = "block";
	mostrarMensagem("Logout realizado com sucesso", "sucesso");
}

/**
 * Função para cadastrar um novo usuário
 * @param {Event} event - Evento do formulário
 */
async function cadastrarUsuario(event) {
	event.preventDefault();

	// Obtém os valores do formulário
	const nome = document.getElementById("nome").value;
	const email = document.getElementById("email").value;
	const senha = document.getElementById("senha").value;

	// Cria um objeto com os dados
	const dados = { nome, email, senha };

	try {
		const response = await fetch(`${API_URL}/usuarios`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(dados),
		});

		const resultado = await response.json();

		if (response.ok) {
			mostrarMensagem(resultado.mensagem, "sucesso");
			// Limpa o formulário
			document.getElementById("form-cadastro").reset();
			// Atualiza a lista
			listarUsuarios();
		} else {
			mostrarMensagem(resultado.erro, "erro");
		}
	} catch (erro) {
		mostrarMensagem(
			"Erro ao conectar com o servidor: " + erro.message,
			"erro"
		);
	}
}

/**
 * Função para listar todos os usuários
 */
async function listarUsuarios() {
	// Mostra o indicador de loading
	const loadingDiv = document.getElementById("loading");
	loadingDiv.style.display = "block";

	// Esconde a tabela temporariamente
	const tabela = document.getElementById("tabela-usuarios");
	tabela.style.display = "none";

	try {
		// Faz requisição GET para listar usuários
		const response = await fetch(`${API_URL}/usuarios`);
		const dados = await response.json();

		if (response.ok) {
			// Seleciona o corpo da tabela
			const tbody = document.getElementById("tbody-usuarios");

			// Limpa o conteúdo anterior
			tbody.innerHTML = "";

			// Verifica se há usuários
			if (dados.dados.length === 0) {
				tbody.innerHTML =
					'<tr><td colspan="5" style="text-align: center;">Nenhum usuário cadastrado</td></tr>';
			} else {
				// Para cada usuário, cria uma linha na tabela
				dados.dados.forEach((usuario) => {
					// Formata a data
					// Verifica se a data existe e é válida
					let dataFormatada = "N/A";
					if (usuario.criado) {
						try {
							// Tenta criar o objeto Date e formatar
							const dataObj = new Date(usuario.criado);
							// Verifica se a data é válida
							if (!isNaN(dataObj.getTime())) {
								dataFormatada =
									dataObj.toLocaleDateString("pt-BR");
							}
						} catch (erro) {
							console.error("Erro ao formatar data:", erro);
						}
					}

					// Cria uma nova linha (tr)
					const tr = document.createElement("tr");

					// Define o HTML interno da linha
					// Template literals (${}) permitem inserir variáveis no texto
					tr.innerHTML = `
                        <td>${usuario.id}</td>
                        <td>${usuario.nome}</td>
                        <td>${usuario.email}</td>
                        <td>${dataFormatada}</td>
                        <td class="acoes">
                            <button class="btn-editar" onclick="editarUsuario(${usuario.id})">Editar</button>
                            <button class="btn-deletar" onclick="deletarUsuario(${usuario.id}, '${usuario.nome}')">Deletar</button>
                        </td>
                    `;

					// Adiciona a linha ao tbody
					tbody.appendChild(tr);
				});
			}

			// Mostra a tabela
			tabela.style.display = "table";
		} else {
			mostrarMensagem(dados.erro, "erro");
		}
	} catch (erro) {
		mostrarMensagem("Erro ao carregar usuários: " + erro.message, "erro");
	} finally {
		// finally sempre executa, independente de sucesso ou erro
		// Esconde o loading
		loadingDiv.style.display = "none";
	}
}

/**
 * Função para deletar um usuário
 * @param {number} id - ID do usuário
 * @param {string} nome - Nome do usuário (para confirmação)
 */
async function deletarUsuario(id, nome) {
	// confirm() mostra uma caixa de diálogo de confirmação
	if (!confirm(`Tem certeza que deseja deletar o usuário ${nome}?`)) {
		return; // Se cancelar, não faz nada
	}

	try {
		// Faz requisição DELETE
		const response = await fetch(`${API_URL}/usuarios/${id}`, {
			method: "DELETE",
		});

		const dados = await response.json();

		if (response.ok) {
			mostrarMensagem(dados.mensagem, "sucesso");
			listarUsuarios(); // Atualiza a lista
		} else {
			mostrarMensagem(dados.erro, "erro");
		}
	} catch (erro) {
		mostrarMensagem("Erro ao deletar usuário: " + erro.message, "erro");
	}
}

/**
 * Função para editar um usuário
 * @param {number} id - ID do usuário
 */
async function editarUsuario(id) {
	// prompt() mostra uma caixa de diálogo para entrada de texto
	const novoNome = prompt("Digite o novo nome:");

	// Se cancelar ou deixar vazio, não faz nada
	if (!novoNome || novoNome.trim().length < 3) {
		mostrarMensagem("Nome deve ter pelo menos 3 caracteres", "erro");
		return;
	}

	try {
		// Faz requisição PATCH (atualização parcial)
		const response = await fetch(`${API_URL}/usuarios/${id}`, {
			method: "PATCH",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ nome: novoNome.trim() }),
		});

		const dados = await response.json();

		if (response.ok) {
			mostrarMensagem(dados.mensagem, "sucesso");
			listarUsuarios(); // Atualiza a lista
		} else {
			mostrarMensagem(dados.erro, "erro");
		}
	} catch (erro) {
		mostrarMensagem("Erro ao editar usuário: " + erro.message, "erro");
	}
}

// Executa quando a página termina de carregar
// window.onload é um evento que dispara quando todo o HTML foi carregado
window.onload = function () {
	// Carrega a lista de usuários automaticamente
	listarUsuarios();
};
