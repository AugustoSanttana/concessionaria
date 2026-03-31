const API_PRODUTOS = "http://127.0.0.1:5000/produto";

function getCarrinho() {
    const carrinhoJSON = localStorage.getItem('carrinho');
    return carrinhoJSON ? JSON.parse(carrinhoJSON) : [];
}

function salvarCarrinho(carrinho) {
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
}

function atualizarContadorCarrinho() {
    const carrinho = getCarrinho();
    const totalItens = carrinho.reduce((soma, item) => soma + item.quantidade, 0);
    const span = document.getElementById('cart-count');
    if (span) span.textContent = totalItens;
}

function adicionarAoCarrinho(produto, quantidadeSelecionada) {
    const carrinho = getCarrinho();

    const existente = carrinho.find(item => item.id === produto.id);

    if (existente) {
        existente.quantidade += quantidadeSelecionada;
    } else {
        carrinho.push({
            id: produto.id,
            nome: produto.nome,
            preco: produto.preco,
            imagem_url: produto.imagem_url,
            quantidade: quantidadeSelecionada
        });
    }

    salvarCarrinho(carrinho);
    atualizarContadorCarrinho();
    alert('Produto adicionado ao carrinho!');
}

async function carregarProdutos() {
    try {
        const response = await fetch(`${API_PRODUTOS}/listar`);
        if (!response.ok) {
            throw new Error('Erro ao buscar produtos');
        }

        const produtos = await response.json();
        const container = document.getElementById('produtos-list');
        container.innerHTML = '';

        if (!produtos || produtos.length === 0) {
            container.innerHTML = '<p>Não há produtos cadastrados no momento.</p>';
            return;
        }

        produtos.forEach(produto => {
            const imgSrc = produto.imagem_url
                ? `http://127.0.0.1:5000${produto.imagem_url}`
                : 'https://via.placeholder.com/200x200?text=Sem+Imagem';

            const card = document.createElement('article');
            card.classList.add('produto-card');

            card.innerHTML = `
                <img src="${imgSrc}" alt="${produto.nome}" class="produto-imagem">
                <h2 class="produto-nome">${produto.nome}</h2>
                <p class="produto-preco">R$ ${Number(produto.preco).toFixed(2)}</p>
                <div class="produto-controles">
                    <label>
                        Quantidade:
                        <input type="number" min="1" value="1" class="produto-qtd-input">
                    </label>
                    <button class="btn-add-carrinho">Adicionar ao carrinho</button>
                </div>
            `;

            const btn = card.querySelector('.btn-add-carrinho');
            const inputQtd = card.querySelector('.produto-qtd-input');

            btn.addEventListener('click', () => {
                const qtd = parseInt(inputQtd.value, 10);
                if (isNaN(qtd) || qtd <= 0) {
                    alert('Informe uma quantidade válida.');
                    return;
                }
                adicionarAoCarrinho(produto, qtd);
            });

            container.appendChild(card);
        });

    } catch (erro) {
        console.error('Erro ao carregar produtos:', erro);
        const container = document.getElementById('produtos-list');
        container.innerHTML = '<p>Erro ao carregar produtos. Tente novamente mais tarde.</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    atualizarContadorCarrinho();
    carregarProdutos();
});
