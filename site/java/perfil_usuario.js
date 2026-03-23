async function carregarPerfil() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Você precisa estar logado para acessar o perfil!");
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/user_routes/perfil", {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await response.json();

 
    document.getElementById("nomeUsuario").innerText = data.nome;
    document.getElementById("emailUsuario").innerText = data.email;
    document.getElementById("cpfUsuario").innerText = data.cpf;
    document.getElementById("enderecoUsuario").innerText = data.endereco;

   
    const lista = document.getElementById("listaAgendamentos");
    lista.innerHTML = "";

    if (data.agendamentos.length === 0) {
      lista.innerHTML = "<p>Você ainda não possui agendamentos.</p>";
      return;
    }

    data.agendamentos.forEach((ag) => {
      const card = document.createElement("div");
      card.classList.add("card-agendamento");

      card.innerHTML = `
        <div class="card-info">
          <p><strong>Serviço:</strong> ${ag.servico}</p>
          <p><strong>Profissional:</strong> ${ag.profissional}</p>
          <p><strong>Data:</strong> ${ag.data} às ${ag.hora}</p>
          <p><strong>Status:</strong> <span class="status ${ag.status}">${ag.status}</span></p>
        </div>
        ${
          ag.status === "pendente"
            ? `<button class="btn-cancelar" onclick="cancelarAgendamento(${ag.id})">Cancelar</button>`
            : ""
        }
      `;

      lista.appendChild(card);
    });
  } catch (err) {
    console.error(err);
    alert("Erro ao carregar o perfil.");
  }
}

async function cancelarAgendamento(id) {
  const token = localStorage.getItem("token");
  if (!confirm("Tem certeza que deseja cancelar este agendamento?")) return;

  const response = await fetch(
    `http://127.0.0.1:5000/agendamento/cancelar/${id}`,
    {
      method: "PUT",
      headers: { Authorization: `Bearer ${token}` },
    }
  );

  const data = await response.json();
  alert(data.mensagem || data.erro);
  carregarPerfil();
}

window.onload = carregarPerfil;
