const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");
const mensagemLogin = document.getElementById("mensagem-login");
const btnEntrar = document.getElementById("btnEntrar");
const toggleSenha = document.getElementById("toggleSenha");

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

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = emailInput.value.trim();
  const senha = senhaInput.value;

  mensagemLogin.textContent = "";
  mensagemLogin.className = "mensagem-login";

  btnEntrar.disabled = true;
  btnEntrar.textContent = "Entrando...";

  const isVendedor = email.toLowerCase().includes("@vendedor");
  const rotaLogin = isVendedor
    ? "http://127.0.0.1:5000/vendedor/login"
    : "http://127.0.0.1:5000/cliente/login";

  try {
    const response = await fetch(rotaLogin, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, senha })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.erro || "Erro ao fazer login.");
    }

    mensagemLogin.textContent = "Login realizado com sucesso!";
    mensagemLogin.classList.add("sucesso");

    setTimeout(() => {
      if (isVendedor) {
        window.location.href = "home_vendedor.html";
      } else {
        window.location.href = "home.html";
      }
    }, 700);

  } catch (error) {
    mensagemLogin.textContent = error.message;
    mensagemLogin.classList.add("erro");
  } finally {
    btnEntrar.disabled = false;
    btnEntrar.textContent = "Entrar";
  }
});