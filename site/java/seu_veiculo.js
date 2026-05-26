const form = document.getElementById("veiculo-form");
const grid = document.getElementById("veiculos-grid");

let veiculos = JSON.parse(localStorage.getItem("meusVeiculos")) || [];

renderizarVeiculos();

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const modelo = document.getElementById("modelo").value;
  const marca = document.getElementById("marca").value;
  const ano = document.getElementById("ano").value;
  const fotoInput = document.getElementById("foto");

  const arquivo = fotoInput.files[0];

  if (!arquivo) return;

  const reader = new FileReader();

  reader.onload = function () {

    const novoVeiculo = {
      modelo,
      marca,
      ano,
      foto: reader.result
    };

    veiculos.push(novoVeiculo);

    localStorage.setItem(
      "meusVeiculos",
      JSON.stringify(veiculos)
    );

    renderizarVeiculos();

    form.reset();
  };

  reader.readAsDataURL(arquivo);
});

function renderizarVeiculos() {

  grid.innerHTML = "";

  veiculos.forEach((veiculo) => {

    grid.innerHTML += `
      <div class="veiculo-card">

        <img src="${veiculo.foto}" alt="${veiculo.modelo}">

        <div class="veiculo-info">
          <h3>${veiculo.modelo}</h3>

          <p><strong>Marca:</strong> ${veiculo.marca}</p>

          <p><strong>Ano:</strong> ${veiculo.ano}</p>
        </div>

      </div>
    `;
  });
}