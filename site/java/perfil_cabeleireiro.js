async function carregarPerfilCabeleireiro() {
  const token = localStorage.getItem("token");

  if (!token) {
    alert("Você precisa estar logado!");
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/cabeleireiro/perfil", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      throw new Error("Erro ao carregar perfil do cabeleireiro");
    }

    const data = await response.json();

    document.getElementById("nomeUsuario").innerText = data.nome;
    document.getElementById("emailUsuario").innerText = data.email;
    document.getElementById("notaMedia").innerText = data.nota_media || "N/A";

    const servicosList = document.getElementById("servicos");
    servicosList.innerHTML = "";

    if (data.servicos && data.servicos.length > 0) {
      data.servicos.forEach(serv => {
        const li = document.createElement("li");
        li.textContent = `${serv.nome} - R$${serv.preco}`;
        servicosList.appendChild(li);
      });
    } else {
      servicosList.innerHTML = "<li>Nenhum serviço cadastrado.</li>";
    }

    const lista = document.getElementById("listaAgendamentos");
    lista.innerHTML = "";

    if (data.agendamentos && data.agendamentos.length > 0) {
      data.agendamentos.forEach(ag => {
        const card = document.createElement("div");
        card.classList.add("card-agendamento");

        card.innerHTML = `
          <div class="card-info">
            <p><strong>Cliente:</strong> ${ag.cliente}</p>
            <p><strong>Serviço:</strong> ${ag.servico}</p>
            <p><strong>Data:</strong> ${ag.data} às ${ag.hora}</p>
            <p><strong>Status:</strong> <span class="status ${ag.status}">${ag.status}</span></p>
          </div>
          ${
            ag.status === "pendente"
              ? `
                <button class="btn-concluir" onclick="concluirAgendamento(${ag.id})">Concluir</button>
                <button class="btn-cancelar" onclick="cancelarAgendamento(${ag.id})">Cancelar</button>
              `
              : ""
          }
        `;
        lista.appendChild(card);
      });
    } else {
      lista.innerHTML = "<p>Nenhum agendamento encontrado.</p>";
    }

  } catch (err) {
    console.error(err);
    alert("Erro ao carregar o perfil do cabeleireiro.");
  }
}

async function concluirAgendamento(id) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Você precisa estar logado!");
    window.location.href = "login.html";
    return;
  }

  if (!confirm("Deseja marcar este agendamento como concluído?")) return;

  try {
    const response = await fetch(`http://127.0.0.1:5000/cabeleireiro/agendamentos/${id}/concluir`, {
      method: "PUT",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}` 
      }
    });

    const data = await response.json();
    if (!response.ok) {
      alert(data.erro || "Erro ao concluir agendamento");
      return;
    }

    alert(data.mensagem);
    carregarPerfilCabeleireiro(); // Recarrega a lista de agendamentos
  } catch (err) {
    console.error("Erro ao conectar com a API:", err);
    alert("Erro no servidor. Tente novamente mais tarde.");
  }
}

async function cancelarAgendamento(id) {
  const token = localStorage.getItem("token");
  if (!confirm("Deseja cancelar este agendamento?")) return;

  const response = await fetch(`http://127.0.0.1:5000/barbearia/cancelar/${id}`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await response.json();
  alert(data.mensagem || data.erro);
  carregarPerfilCabeleireiro();
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("tipoUsuario");
  window.location.href = "login.html";
}

window.onload = carregarPerfilCabeleireiro;