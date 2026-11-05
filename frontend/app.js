const $ = (s) => document.querySelector(s);

function tex(el, latex, display = true) {
  if (window.katex) katex.render(latex, el, { throwOnError: false, strict: false, displayMode: display });
  else el.textContent = latex;
}

async function chamar(url, corpo) {
  const opcoes = corpo
    ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) }
    : undefined;
  const r = await fetch(url, opcoes);
  const dados = await r.json();
  if (!r.ok) throw new Error(typeof dados.detail === "string" ? dados.detail : "Dados inválidos.");
  return dados;
}

let exercicio = null;

// Abas
function abrir(aba) {
  $("#resolver").hidden = aba !== "resolver";
  $("#praticar").hidden = aba !== "praticar";
  $("#aba-resolver").classList.toggle("ativa", aba === "resolver");
  $("#aba-praticar").classList.toggle("ativa", aba === "praticar");
  if (aba === "praticar" && !exercicio) carregar();
}
$("#aba-resolver").onclick = () => abrir("resolver");
$("#aba-praticar").onclick = () => abrir("praticar");

// Resolver
$("#form-resolver").onsubmit = async (e) => {
  e.preventDefault();
  const saida = $("#saida");
  saida.innerHTML = "";
  try {
    const d = await chamar("/api/resolver", { modo: $("#modo").value, entrada: $("#entrada").value });
    d.passos.forEach((p) => {
      const div = document.createElement("div");
      div.className = "passo";
      saida.appendChild(div);
      tex(div, p);
    });
    const r = document.createElement("div");
    r.className = "resposta";
    saida.appendChild(r);
    tex(r, d.resposta);
  } catch (err) {
    saida.innerHTML = '<p class="erro"></p>';
    saida.firstChild.textContent = err.message;
  }
};

// Praticar (a pontuação fica guardada no navegador)
let rating = 1000;
try { rating = Number(localStorage.getItem("rating")) || 1000; } catch {}
const salvar = () => { try { localStorage.setItem("rating", rating); } catch {} };

async function carregar() {
  try {
    exercicio = await chamar(`/api/exercicio?rating=${rating}`);
    $("#nivel").textContent = `Nível ${exercicio.nivel}, pontuação ${rating}`;
    $("#instrucao").textContent = exercicio.instrucao;
    tex($("#expressao"), exercicio.expressao);
    $("#resposta").value = "";
    $("#feedback").textContent = "";
    $("#proximo").hidden = true;
    $("#form-praticar button").disabled = false;
    $("#resposta").focus();
  } catch (err) {
    $("#feedback").textContent = err.message;
  }
}

$("#form-praticar").onsubmit = async (e) => {
  e.preventDefault();
  try {
    const d = await chamar("/api/responder", { id: exercicio.id, resposta: $("#resposta").value, rating });
    rating = d.rating;
    salvar();
    const fb = $("#feedback");
    fb.className = d.correto ? "certo" : "erro";
    fb.textContent = d.correto ? "Correto!" : `Não foi dessa vez. A resposta era: ${d.resposta_certa}`;
    $("#nivel").textContent = `Nível ${exercicio.nivel}, pontuação ${rating}`;
    $("#proximo").hidden = false;
    $("#form-praticar button").disabled = true;
  } catch (err) {
    $("#feedback").className = "erro";
    $("#feedback").textContent = err.message;
  }
};
$("#proximo").onclick = carregar;
