document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);

    const nome = urlParams.get("nome");
    const preco = urlParams.get("preco");
    const imagem = urlParams.get("imagem");
    const info = urlParams.get("info");
    const descricao = urlParams.get("descricao");

    if (nome) document.getElementById("det-nome").innerText = nome;
    if (preco) document.getElementById("det-preco").innerText = preco;
    if (imagem) document.getElementById("det-img").src = imagem;
    if (info) document.getElementById("det-info").innerText = info;
    if (descricao) document.getElementById("det-descricao").innerText = descricao;
});