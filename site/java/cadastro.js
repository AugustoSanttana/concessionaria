const form = document.getElementById("cadastro-form");
const nomeInput = document.getElementById("nome");
const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");
const confirmarSenhaInput = document.getElementById("confirmarSenha");
const cpfInput = document.getElementById("cpf");
const telefoneInput = document.getElementById("telefone");
const enderecoInput = document.getElementById("endereco");
const cepInput = document.getElementById("cep");
const dataNascimentoInput = document.getElementById("data_nascimento");
const rendaMensalInput = document.getElementById("renda_mensal");
const cnhInput = document.getElementById("cnh");
const categoriaCnhInput = document.getElementById("categoria_cnh");
const profissaoInput = document.getElementById("profissao");

const mensagemCadastro = document.getElementById("mensagem-cadastro");
const btnCadastrar = document.getElementById("btnCadastrar");
const toggleSenha = document.getElementById("toggleSenha");
const toggleConfirmarSenha = document.getElementById("toggleConfirmarSenha");

toggleSenha.addEventListener("click", () => {
  const tipoAtual = senhaInput.getAttribute("type");
  if (tipoAtual === "password") {
    senhaInput.setAttribute("type", "text");
    toggleSenha.textContent = "Ocultar";
  } else {
    senhaInput.setAttribute("type", "password");
    toggleSenha.textContent = "Mostrar";
  }
});

toggleConfirmarSenha.addEventListener("click", () => {
  const tipoAtual = confirmarSenhaInput.getAttribute("type");
  if (tipoAtual === "password") {
    confirmarSenhaInput.setAttribute("type", "text");
    toggleConfirmarSenha.textContent = "Ocultar";
  } else {
    confirmarSenhaInput.setAttribute("type", "password");
    toggleConfirmarSenha.textContent = "Mostrar";
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = nomeInput.value.trim();
  const email = emailInput.value.trim();
  const senha = senhaInput.value;
  const confirmarSenha = confirmarSenhaInput.value;
  const cpf = cpfInput.value.trim();
  const telefone = telefoneInput.value.trim();
  const endereco = enderecoInput.value.trim();
  const cep = cepInput.value.trim();
  const data_nascimento = dataNascimentoInput.value;
  const renda_mensal = rendaMensalInput.value.trim();
  const cnh = cnhInput.value.trim();
  const categoria_cnh = categoriaCnhInput.value.trim();
  const profissao = profissaoInput.value.trim();

  mensagemCadastro.textContent = "";
  mensagemCadastro.className = "mensagem-cadastro";

  if (senha !== confirmarSenha) {
    mensagemCadastro.textContent = "As senhas não coincidem.";
    mensagemCadastro.classList.add("erro");
    return;
  }

  btnCadastrar.disabled = true;
  btnCadastrar.textContent = "Cadastrando...";

  try {
    const response = await fetch("http://127.0.0.1:5000/cliente/cadastrar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        nome,
        email,
        senha,
        cpf,
        telefone,
        endereco,
        cep,
        data_nascimento,
        renda_mensal: renda_mensal || null,
        cnh: cnh || null,
        categoria_cnh: categoria_cnh || null,
        profissao: profissao || null
      })
    });

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await response.json()
      : { erro: await response.text() };

    if (!response.ok) {
      throw new Error(data.erro || data.detalhes || "Erro ao realizar cadastro.");
    }

    mensagemCadastro.textContent = "Cadastro realizado com sucesso!";
    mensagemCadastro.classList.add("sucesso");

    form.reset();

    setTimeout(() => {
      window.location.href = "login.html";
    }, 1000);
  } catch (error) {
    mensagemCadastro.textContent = error.message;
    mensagemCadastro.classList.add("erro");
  } finally {
    btnCadastrar.disabled = false;
    btnCadastrar.textContent = "Cadastrar";
  }
});