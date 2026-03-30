const url = 'http://127.0.0.1:5000/user_routes/cadastrar';

async function cadastro() {
    let nome = document.getElementById('nome').value;
    let cpf = document.getElementById('cpf').value;
    let email = document.getElementById('email').value;
    let senha = document.getElementById('senha').value;
    let endereco = document.getElementById('endereco').value;

    if (!nome || !email || !senha || !cpf || !endereco) {
        alert("Todos os campos são obrigatórios.");
        return;
    }

    try {
        let response = await fetch(url, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, email, senha, cpf, endereco })
        });

        let data = await response.json();

        if (response.ok) {
            console.log(data);
            alert(data.mensagem || "Cadastro realizado com sucesso!");
            window.location.href = '../html/home_usuario.html';
        } else {
            alert(data.erro || "Erro no cadastro. Por favor, tente novamente.");
        }

    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro no cadastro, tente novamente.");
    }
}

document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault();
    cadastro();
});
