const urlAgendamento = 'http://127.0.0.1:5000/agendamento/criar';
const urlCabeleireiros = 'http://127.0.0.1:5000/cabeleireiro/listar';

const select = document.getElementById('barbeiro');

// Função para carregar os cabeleireiros no select
async function carregarCabeleireiros() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(urlCabeleireiros, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            // Limpa opções antigas
            select.innerHTML = '<option value="">Selecione...</option>';

            data.forEach(b => {
                if (!b.is_admin) {  // Ignora admin
                    const option = document.createElement('option');
                    option.value = b.id;  // envia ID ao criar agendamento
                    option.textContent = b.nome;
                    select.appendChild(option);
                }
            });
        } else {
            alert(data.erro || "Erro ao carregar barbeiros");
        }
    } catch (error) {
        console.error("Erro ao buscar barbeiros:", error);
        alert("Erro no servidor. Tente novamente mais tarde.");
    }
}

// Chama ao carregar a página
carregarCabeleireiros();

async function criarAgendamento(event) {
    event.preventDefault(); 

    const cliente_id = localStorage.getItem('user_id'); 
    const cabeleireiro_id = document.getElementById('barbeiro').value;
    const servico = document.getElementById('servico').value;
    const data = document.getElementById('data').value;
    const hora = document.getElementById('hora').value;

    if (!cabeleireiro_id || !servico || !data || !hora) {
        alert("Preencha todos os campos do agendamento.");
        return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
        alert("Você precisa estar logado para agendar.");
        return;
    }

    try {
        const response = await fetch(urlAgendamento, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify({ 
                cliente_id, 
                profissional_id: cabeleireiro_id,  // agora envia ID
                servico, 
                data, 
                hora 
            })
        });

        const dataResp = await response.json();

        if (response.ok) {
            alert("Agendamento realizado com sucesso!");
            document.querySelector('.form-agendamento').reset();
            window.location.href = '../html/home_usuario.html';
        } else {
            alert(dataResp.erro || "Erro ao criar agendamento. Tente novamente.");
        }

    } catch (error) {
        console.error("Erro ao conectar com a API:", error);
        alert("Erro no servidor. Tente novamente mais tarde.");
    }
}

document.querySelector('.form-agendamento').addEventListener('submit', criarAgendamento);
