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

    // verifica se produto já está no carrinho
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

function formatarPreco(valor) {
    return `R$ ${Number(valor).toFixed(2)}`;
}

function renderizarCarrinho() {
    const carrinho = getCarrinho();
    const container = document.getElementById('carrinho-itens');
    const resumo = document.getElementById('carrinho-resumo');
    const totalSpan = document.getElementById('carrinho-total');

    container.innerHTML = '';

    if (!carrinho || carrinho.length === 0) {
        container.innerHTML = '<p>Seu carrinho está vazio.</p>';
        resumo.style.display = 'none';
        return;
    }

    resumo.style.display = 'block';

    let totalGeral = 0;

    carrinho.forEach((item, index) => {
        const imgSrc = item.imagem_url
            ? `http://127.0.0.1:5000${item.imagem_url}`
            : 'https://via.placeholder.com/80x80?text=Sem+Imagem';

        const linha = document.createElement('article');
        linha.classList.add('carrinho-item');

        const subtotal = item.preco * item.quantidade;
        totalGeral += subtotal;

        linha.innerHTML = `
            <img src="${imgSrc}" alt="${item.nome}" class="carrinho-item-imagem">
            <div class="carrinho-item-info">
                <h2>${item.nome}</h2>
                <p>Preço: ${formatarPreco(item.preco)}</p>
                <p>Quantidade: ${item.quantidade}</p>
                <p>Subtotal: ${formatarPreco(subtotal)}</p>
            </div>
            <button class="btn-remover">Remover</button>
        `;

        // Remover item
        const btnRemover = linha.querySelector('.btn-remover');
        btnRemover.addEventListener('click', () => {
            const novoCarrinho = getCarrinho();
            novoCarrinho.splice(index, 1);
            salvarCarrinho(novoCarrinho);
            atualizarContadorCarrinho();
            renderizarCarrinho();
        });

        container.appendChild(linha);
    });

    totalSpan.textContent = formatarPreco(totalGeral);
}

document.addEventListener('DOMContentLoaded', () => {
    atualizarContadorCarrinho();
    renderizarCarrinho();

    const btnPagamento = document.getElementById('btn-ir-pagamento');
    btnPagamento.addEventListener('click', () => {
        // Aqui você pode redirecionar para uma página de pagamento futuramente
        alert('Aqui entraria a tela de pagamento 🙂');
    });
});
