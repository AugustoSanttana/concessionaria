const urlLoginUsuario = 'http://127.0.0.1:5000/user_routes/login';
const urlLoginCabeleireiro = 'http://127.0.0.1:5000/cabeleireiro/login';

async function login() {
    let email = document.getElementById('email').value;
    let senha = document.getElementById('senha').value;

    if (!email || !senha) {
        alert("Preencha todos os campos.");
        return;
    }

    async function tentarLogin(url, email, senha, tipo) {
        try {
            let response = await fetch(url, {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, senha: senha })
            });

            if (!response.ok) return null;

            let data = await response.json();
            data.tipo = tipo;  
            return data;
        } catch (error) {
            console.error(`Erro ao tentar login em ${url}:`, error);
            return null;
        }
    }

    let data = await tentarLogin(urlLoginUsuario, email, senha, "usuario");

    if (!data) {
        data = await tentarLogin(urlLoginCabeleireiro, email, senha, "cabeleireiro");
    }

    if (!data) {
        alert("Credenciais inválidas");
        return;
    }

    console.log("Resposta da API:", data);
    alert("Login realizado com sucesso!");

    if (data.token) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("tipoUsuario", data.tipo); 
    }

    if (data.nome && data.id) {
        localStorage.setItem("usuario_nome", data.nome);
        localStorage.setItem("usuario_id", data.id);
    }

    if (data.tipo === "cabeleireiro") {
        window.location.href = '../html/home_cabeleireiro.html';
    } else {
        window.location.href = '../html/home_usuario.html';
    }
}

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    login();
});
