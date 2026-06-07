document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);

    const nome     = urlParams.get("nome");
    const preco    = urlParams.get("preco");
    const imagem   = urlParams.get("imagem");
    const info     = urlParams.get("info");
    const descricao = urlParams.get("descricao");

    if (nome)     document.getElementById("det-nome").innerText = nome;
    if (preco)    document.getElementById("det-preco").innerText = preco;
    if (imagem)   document.getElementById("det-img").src = imagem;
    if (info)     document.getElementById("det-info").innerText = info;
    if (descricao) document.getElementById("det-descricao").innerText = descricao;

    // ── Solicitar Proposta ──────────────────────────────────────────────
    const btnProposta = document.querySelector(".btn-primary");
    if (btnProposta) {
        btnProposta.addEventListener("click", async () => {
            const token = localStorage.getItem("token");

            if (!token) {
                alert("Você precisa estar logado para solicitar uma proposta.\nFaça login e tente novamente.");
                window.location.href = "login.html";
                return;
            }

            btnProposta.disabled = true;
            btnProposta.textContent = "Enviando...";

            try {
                const response = await fetch("http://127.0.0.1:5000/cliente/proposta", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        nome_veiculo:  nome     || "",
                        preco_veiculo: preco    || "",
                        info_veiculo:  info     || "",
                        descricao:     descricao || ""
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    alert(`✅ Proposta enviada com sucesso!\nConfira o seu e-mail.`);
                } else {
                    alert(`❌ Erro: ${data.erro || "Não foi possível enviar a proposta."}`);
                }
            } catch (err) {
                alert("❌ Erro de conexão com o servidor. Tente novamente mais tarde.");
                console.error(err);
            } finally {
                btnProposta.disabled = false;
                btnProposta.textContent = "Solicitar Proposta";
            }
        });
    }
});
