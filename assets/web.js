// Formularios: FormSubmit necesita una URL absoluta para volver a la página de gracias.
document.querySelectorAll("form[data-gracias]").forEach(function (f) {
  var next = f.querySelector('input[name="_next"]');
  if (next) next.value = new URL(f.dataset.gracias, location.href).href;
});

// Conversación de ejemplo: aparece mensaje a mensaje una sola vez, cuando el teléfono entra en pantalla.
(function () {
  if (!("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("js");
  var chat = document.getElementById("chat");
  if (!chat) return;
  var items = Array.prototype.slice.call(chat.children);
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) { items.forEach(function (el) { el.classList.add("visto"); }); return; }
  var reloj = document.getElementById("reloj");
  var pausas = [300, 1500, 700, 1300, 900];
  var typing = document.createElement("div");
  typing.className = "escribiendo visto";
  typing.setAttribute("aria-hidden", "true");
  typing.innerHTML = "<b></b><b></b><b></b>";
  function mostrar(i) {
    if (i >= items.length) { if (typing.parentNode) typing.remove(); return; }
    var el = items[i];
    var esBot = el.classList.contains("bot");
    if (esBot) { chat.insertBefore(typing, el); }
    setTimeout(function () {
      if (typing.parentNode) typing.remove();
      el.classList.add("visto");
      if (i === 3 && reloj) reloj.textContent = "22:15";
      mostrar(i + 1);
    }, pausas[i] || 800);
  }
  var visto = false;
  var io = new IntersectionObserver(function (entradas) {
    if (!visto && entradas[0].isIntersecting) { visto = true; mostrar(0); io.disconnect(); }
  }, { threshold: 0.4 });
  io.observe(chat);
})();

// Calculadora de clientes perdidos (todo en el navegador).
(function () {
  var ids = ["c-msg", "c-tarde", "c-perdidos", "c-cierre", "c-valor"];
  var els = ids.map(function (i) { return document.getElementById(i); });
  if (!els[0]) return;
  var out = document.getElementById("c-euros"), det = document.getElementById("c-detalle");
  var fmt = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 0 });
  function n(e) { var v = parseFloat(e.value); return isFinite(v) && v > 0 ? v : 0; }
  function calc() {
    var tarde = Math.min(n(els[1]), n(els[0]));
    var perdidosMes = tarde * Math.min(n(els[2]), 100) / 100;
    var ventasAno = perdidosMes * 12 * Math.min(n(els[3]), 10) / 10;
    var euros = ventasAno * n(els[4]);
    out.textContent = fmt.format(Math.round(euros / 100) * 100) + " €";
    det.textContent = "Unos " + fmt.format(perdidosMes * 12) + " clientes al año que se van con otro, de los que unos " +
      (ventasAno < 10 ? ventasAno.toLocaleString("es-ES", { maximumFractionDigits: 1 }) : fmt.format(ventasAno)) + " te habrían comprado.";
  }
  els.forEach(function (e) { e.addEventListener("input", calc); });
  calc();
})();
