const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");
const mensagemLogin = document.getElementById("mensagem-login");
const btnEntrar = document.getElementById("btnEntrar");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = emailInput.value.trim();
  const senha = senhaInput.value;

  mensagemLogin.textContent = "";
  mensagemLogin.className = "mensagem-login";

  btnEntrar.disabled = true;
  btnEntrar.textContent = "Entrando...";

  const isVendedor = email.toLowerCase().includes("@vendedor");

  // 🔥 DEFINE A ROTA CERTA
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

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await response.json()
      : { erro: await response.text() };

    if (!response.ok) {
      throw new Error(data.erro || "Erro ao fazer login.");
    }

    mensagemLogin.textContent = "Login realizado com sucesso!";
    mensagemLogin.classList.add("sucesso");

    // 🔥 REDIRECIONAMENTO CORRETO
    setTimeout(() => {
      if (isVendedor) {
        window.location.href = "home_vendedor.html";
      } else {
        window.location.href = "home_usuario.html";
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