const campos = ["logradouro", "bairro", "cidade", "uf"];
const statusConsulta = document.querySelector('[role="status"]');
const botao = document.querySelector("button");
let sequencia = 0;

function limpar() {
  for (const campo of campos) document.getElementById(campo).value = "";
}

document.querySelector("#cep").addEventListener("input", () => {
  sequencia++;
  limpar();
  statusConsulta.textContent = "";
  botao.disabled = false;
});

document.querySelector("form").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const atual = ++sequencia;
  const cep = document.getElementById("cep").value.trim();
  limpar();
  botao.disabled = true;
  statusConsulta.textContent = "Consultando…";
  try {
    const resposta = await fetch("/ceps/" + encodeURIComponent(cep));
    const dados = await resposta.json();
    if (atual !== sequencia) return;
    if (!resposta.ok) throw new Error(dados.detail || "Falha na consulta.");
    for (const campo of campos) document.getElementById(campo).value = dados[campo];
    statusConsulta.textContent = "Endereço encontrado.";
  } catch (erro) {
    if (atual === sequencia) statusConsulta.textContent =
      erro instanceof TypeError ? "Falha de conexão com a API." : erro.message;
  } finally {
    if (atual === sequencia) botao.disabled = false;
  }
});
