const form = document.getElementById("cadastro-vendedor-form");
const nomeInput = document.getElementById("nome");
const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");
const confirmarSenhaInput = document.getElementById("confirmarSenha");
const cpfInput = document.getElementById("cpf");
const telefoneInput = document.getElementById("telefone");
const enderecoInput = document.getElementById("endereco");
const cepInput = document.getElementById("cep");
const dataNascimentoInput = document.getElementById("data_nascimento");
const codigoVendedorInput = document.getElementById("codigo_vendedor");
const comissaoInput = document.getElementById("comissao_percentual");
const metaMensalInput = document.getElementById("meta_mensal");
const gerenteIdInput = document.getElementById("gerente_id");

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
  const codigo_vendedor = codigoVendedorInput.value.trim();
  const comissao_percentual = comissaoInput.value;
  const meta_mensal = metaMensalInput.value.trim();
  const gerente_id = gerenteIdInput.value.trim();

  mensagemCadastro.textContent = "";
  mensagemCadastro.className = "mensagem-cadastro";

  if (senha !== confirmarSenha) {
    mensagemCadastro.textContent = "As senhas não coincidem.";
    mensagemCadastro.classList.add("erro");
    return;
  }

  if (!email.toLowerCase().includes("@vendedor")) {
    mensagemCadastro.textContent = "O e-mail do vendedor deve conter @vendedor.";
    mensagemCadastro.classList.add("erro");
    return;
  }

  btnCadastrar.disabled = true;
  btnCadastrar.textContent = "Cadastrando...";

  try {
    const response = await fetch("http://127.0.0.1:5000/vendedor/cadastrar", {
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
        codigo_vendedor,
        comissao_percentual,
        meta_mensal: meta_mensal || null,
        gerente_id: gerente_id || null
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.erro || data.detalhes || "Erro ao cadastrar vendedor.");
    }

    mensagemCadastro.textContent = "Vendedor cadastrado com sucesso!";
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
    btnCadastrar.textContent = "Cadastrar vendedor";
  }
});