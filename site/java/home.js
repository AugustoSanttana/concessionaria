const API_BASE_URL = "http://127.0.0.1:5000";
const track = document.querySelector(".carousel-track");
const next = document.querySelector(".next");
const prev = document.querySelector(".prev");

const carrosFixos = [
  {
    marca: "BMW",
    modelo: "M3",
    combustivel: "Motor 3.0",
    quilometragem: "510cv",
    ano: "2022",
    preco: 450000,
    imagem_url: "/uploads/bmw-m3.avif"
  },
  {
    marca: "Porsche",
    modelo: "911",
    combustivel: "Turbo S",
    quilometragem: "650cv",
    ano: "2023",
    preco: 950000,
    imagem_url: "/uploads/porsche.911.avif"
  },
  {
    marca: "Audi",
    modelo: "RS6",
    combustivel: "V8 Biturbo",
    quilometragem: "600cv",
    ano: "2022",
    preco: 720000,
    imagem_url: "/uploads/Audi.rs6.webp"
  }
];

function formatarPreco(valor) {
  return Number(valor).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL"
  });
}

function montarImagem(url) {
  if (!url) {
    return "https://via.placeholder.com/400x250?text=Sem+Imagem";
  }

  if (url.startsWith("http")) {
    return url;
  }

  return `${API_BASE_URL}${url}`;
}

function criarCardCarro(carro) {
  const card = document.createElement("div");
  card.className = "car-card";

  card.innerHTML = `
    <img src="${montarImagem(carro.imagem_url)}" alt="${carro.marca} ${carro.modelo}">
    <h4>${carro.marca} ${carro.modelo}</h4>
    <p>${carro.combustivel || "Não informado"} • ${carro.quilometragem || "Não informado"} • ${carro.ano || "Ano não informado"}</p>
    <span class="price">${formatarPreco(carro.preco || 0)}</span>
    <button>Comprar</button>
  `;

  return card;
}

function renderizarCarrosFixos() {
  carrosFixos.forEach((carro) => {
    track.appendChild(criarCardCarro(carro));
  });
}

async function carregarVeiculosCadastrados() {
  try {
    const response = await fetch(`${API_BASE_URL}/veiculo/compra/listar`);
    const carros = await response.json();

    if (!response.ok) {
      throw new Error("Erro ao listar veículos.");
    }

    if (!Array.isArray(carros) || carros.length === 0) {
      return;
    }

    carros.forEach((carro) => {
      track.appendChild(criarCardCarro(carro));
    });

  } catch (error) {
    console.error("Erro ao carregar veículos cadastrados:", error);
  }
}

next.addEventListener("click", () => {
  track.scrollBy({ left: 300, behavior: "smooth" });
});

prev.addEventListener("click", () => {
  track.scrollBy({ left: -300, behavior: "smooth" });
});

async function iniciarCarrossel() {
  track.innerHTML = "";
  renderizarCarrosFixos();
  await carregarVeiculosCadastrados();
}

iniciarCarrossel();