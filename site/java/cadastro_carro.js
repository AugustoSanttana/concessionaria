const API_BASE_URL = "http://127.0.0.1:5000";

const form = document.getElementById("form-cadastro-carro");
const mensagem = document.getElementById("mensagem");
const btnSubmit = document.getElementById("btn-submit");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  mensagem.textContent = "";
  mensagem.className = "mensagem";
  btnSubmit.disabled = true;
  btnSubmit.textContent = "Cadastrando...";

  try {
    const formData = new FormData(form);

    const response = await fetch(`${API_BASE_URL}/veiculo/compra/cadastrar`, {
      method: "POST",
      body: formData
    });

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await response.json()
      : { erro: await response.text() };

    if (!response.ok) {
      throw new Error(data.erro || data.detalhes || "Erro ao cadastrar veículo.");
    }

    mensagem.textContent = "Veículo cadastrado com sucesso!";
    mensagem.classList.add("sucesso");

    form.reset();

    setTimeout(() => {
      window.location.href = "home_vendedor.html";
    }, 1200);
  } catch (error) {
    console.error("Erro no cadastro do veículo:", error);
    mensagem.textContent = error.message;
    mensagem.classList.add("erro");
  } finally {
    btnSubmit.disabled = false;
    btnSubmit.textContent = "Cadastrar veículo";
  }
});