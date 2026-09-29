/* core.js — moteur motion partagé MonCours.
   Chaque style définit window.BUILD = {1:fn,2:fn,3:fn,...} + window.BG (fn->couleur) puis appelle start().
   Rendu déterministe : ?scene=N&dur=MS, window.__seek(ms), window.__ready.
   Règle anti-vibration : tout entre une fois puis FIGE (fill:both, paused, seek). */
(function () {
  const ST = document.createElement("style");
  ST.textContent = `*{margin:0;box-sizing:border-box} html,body{height:100%;overflow:hidden;background:#000}
    #fit{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
    #stage{position:relative;flex:none;overflow:hidden}
    .e{position:absolute;will-change:transform,opacity} .w{display:inline-block;will-change:transform,opacity}`;
  document.head.appendChild(ST);
  const fit = document.createElement("div"); fit.id = "fit";
  const stage = document.createElement("div"); stage.id = "stage";
  fit.appendChild(stage); document.body.appendChild(fit);

  const items = [], all = [];
  const OUT = "cubic-bezier(.16,.84,.26,1)", POP = "cubic-bezier(.2,1.3,.35,1)";

  window.S = stage;
  window.E = function (cls, css, html) {
    const d = document.createElement("div"); d.className = "e " + (cls || "");
    if (css) d.style.cssText += ";" + css; if (html != null) d.innerHTML = html;
    stage.appendChild(d); return d;
  };
  window.add = function (node, kind, o) { items.push(Object.assign({ node, kind }, o || {})); return node; };

  // titre cinétique : segs=[[texte,orangeClass?],...] ; chaque MOT entre en cascade
  window.kinetic = function (cls, css, segs, base, step) {
    const box = window.E(cls, css, ""); let i = 0; base = base || 0; step = step || 70;
    for (const seg of segs) {
      const txt = seg[0], extra = seg[1] || "";
      for (const chunk of txt.split(/(\n)/)) {
        if (chunk === "\n") { box.appendChild(document.createElement("br")); continue; }
        for (const w of chunk.split(" ")) {
          if (w === "") continue;
          const sp = document.createElement("span"); sp.className = "w " + extra; sp.textContent = w;
          box.appendChild(sp); box.appendChild(document.createTextNode(" "));
          window.add(sp, "rise", { delay: base + i * step }); i++;
        }
      }
    }
    return box;
  };

  // étincelle 4/8 branches (scale-in puis fige ; spin optionnel isolé)
  window.spark = function (cx, cy, r, delay, col, spin) {
    col = col || "#E48A1C";
    const wrap = window.E("", `left:${cx - r}px;top:${cy - r}px;width:${2 * r}px;height:${2 * r}px`);
    const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    s.setAttribute("viewBox", "0 0 100 100"); s.setAttribute("width", 2 * r); s.setAttribute("height", 2 * r);
    s.innerHTML = `<g stroke="${col}" stroke-width="6" stroke-linecap="round">
      <line x1="50" y1="12" x2="50" y2="34"/><line x1="50" y1="66" x2="50" y2="88"/>
      <line x1="12" y1="50" x2="34" y2="50"/><line x1="66" y1="50" x2="88" y2="50"/>
      <line x1="24" y1="24" x2="38" y2="38"/><line x1="62" y1="62" x2="76" y2="76"/>
      <line x1="76" y1="24" x2="62" y2="38"/><line x1="38" y1="62" x2="24" y2="76"/></g>
      <circle cx="50" cy="50" r="8.5" fill="${col}"/>`;
    s.style.transformOrigin = "50% 50%"; wrap.appendChild(s);
    window.add(wrap, "pop", { delay }); if (spin) window.add(s, "spin", {});
    return wrap;
  };

  // SVG dessiné au trait (path/line) via stroke-dashoffset
  window.drawSVG = function (css, inner, delay, dur) {
    const wrap = window.E("", css);
    const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    s.setAttribute("viewBox", "0 0 100 100"); s.setAttribute("width", "100%"); s.setAttribute("height", "100%");
    s.innerHTML = inner; wrap.appendChild(s);
    wrap.querySelectorAll("path,line,polyline,circle,rect").forEach(p => {
      p.setAttribute("pathLength", "1"); p.style.strokeDasharray = "1"; window.add(p, "draw", { delay, dur });
    });
    return wrap;
  };

  const RISE = [{ opacity: 0, transform: "translateY(40px)" }, { opacity: 1, transform: "translateY(0)" }];
  const RISES = [{ opacity: 0, transform: "translateY(18px)" }, { opacity: 1, transform: "translateY(0)" }];
  const POPK = [{ opacity: 0, transform: "scale(.5)" }, { opacity: 1, transform: "scale(1)" }];
  const SLAM = [{ opacity: 0, transform: "scale(1.35)" }, { opacity: 1, transform: "scale(1)" }];

  function fitScale() { const W = window.STAGE_W || 1280, H = window.STAGE_H || 720; const s = Math.min(innerWidth / W, innerHeight / H); stage.style.transform = `scale(${s})`; }
  addEventListener("resize", fitScale);

  window.start = function () {
    const P = new URLSearchParams(location.search);
    const sc = parseInt(P.get("scene"), 10) || 1, dur = parseInt(P.get("dur"), 10) || 4000;
    stage.style.width = (window.STAGE_W || 1280) + "px"; stage.style.height = (window.STAGE_H || 720) + "px";
    (window.BUILD[sc] || window.BUILD[1])();
    document.body.style.background = (window.BG ? window.BG(sc) : "#FAF7EF");
    fitScale();
    const fin = Math.min(340, dur * .15), fout = Math.min(420, dur * .2);
    const sa = stage.animate([{ opacity: 0, offset: 0 }, { opacity: 1, offset: fin / dur },
      { opacity: 1, offset: (dur - fout) / dur }, { opacity: 0, offset: 1 }], { duration: dur, fill: "both", easing: "linear" });
    sa.pause(); all.push(sa);
    for (const it of items) {
      let a, n = it.node, d = it.delay || 0;
      switch (it.kind) {
        case "spin": a = n.animate([{ transform: "rotate(0)" }, { transform: "rotate(360deg)" }], { duration: 22000, iterations: Infinity, easing: "linear" }); break;
        case "pop": a = n.animate(POPK, { duration: 560, delay: d, fill: "both", easing: POP }); break;
        case "slam": a = n.animate(SLAM, { duration: 480, delay: d, fill: "both", easing: OUT }); break;
        case "rises": a = n.animate(RISES, { duration: 560, delay: d, fill: "both", easing: OUT }); break;
        case "draw": a = n.animate([{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: it.dur || 480, delay: d, fill: "both", easing: OUT }); break;
        case "type": n.style.clipPath = "inset(0 100% 0 0)"; a = n.animate([{ clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0 0 0)" }], { duration: it.dur || 700, delay: d, fill: "both", easing: `steps(${it.steps || 14})` }); break;
        case "wipe": a = n.animate([{ clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0 0 0)" }], { duration: it.dur || 420, delay: d, fill: "both", easing: OUT }); break;
        case "fade": a = n.animate([{ opacity: 0 }, { opacity: it.to != null ? it.to : 1 }], { duration: it.dur || 420, delay: d, fill: "both", easing: "linear" }); break;
        case "scanY": a = n.animate([{ transform: "translateY(0)" }, { transform: `translateY(${it.dist}px)` }], { duration: it.dur || 1600, delay: d, fill: "both", easing: "cubic-bezier(.45,0,.25,1)" }); break;
        default: a = n.animate(RISE, { duration: 640, delay: d, fill: "both", easing: OUT });
      }
      a.pause(); all.push(a);
    }
    seek(0); window.__ready = true;
  };
  function seek(ms) { for (const a of all) { try { a.currentTime = ms; } catch (e) {} } }
  window.__seek = seek;
})();
