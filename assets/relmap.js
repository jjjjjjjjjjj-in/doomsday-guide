// キャラクター相関図：データ（#relmap-data）から SVG を描き、ドラッグで移動・ピンチ／ホイールで拡大縮小・タップで人物の説明を開く
(function () {
  const dataEl = document.getElementById("relmap-data");
  const stage = document.getElementById("relmap");
  if (!dataEl || !stage) return;
  const D = JSON.parse(dataEl.textContent);
  const T = D.text;
  const NS = "http://www.w3.org/2000/svg";
  const R = { lead: 66, main: 48, sub: 36 };
  const NAME_SIZE = { lead: 25, main: 21, sub: 18 };
  const svgEl = (tag, attrs, parent) => {
    const el = document.createElementNS(NS, tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // ---- 位置を決める（x,y があればそのまま。なければ ring と angle、それもなければ空いた角度に自動で並べる）
  const people = D.people.map((p) => ({ ...p, r: R[p.role] || R.sub }));
  const byId = Object.fromEntries(people.map((p) => [p.id, p]));
  const center = byId[D.center] || people[0];
  const auto = people.filter((p) => p.x == null && p.angle == null);
  auto.forEach((p, i) => { p.ring = p.ring || 2; p.angle = (360 / auto.length) * i - 90; });
  people.forEach((p) => {
    if (p.x == null) {
      const dist = (p.ring || 2) === 1 ? 260 : 460;
      const a = (p.angle * Math.PI) / 180;
      p.x = (center.x || 0) + Math.cos(a) * dist;
      p.y = (center.y || 0) + Math.sin(a) * dist;
    }
  });
  // 重なりがあれば少しずつ押し広げる（手で置いた位置はほぼそのまま）
  for (let k = 0; k < 60; k++) {
    let moved = false;
    for (let i = 0; i < people.length; i++) for (let j = i + 1; j < people.length; j++) {
      const a = people[i], b = people[j];
      const dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy) || 1;
      const need = a.r + b.r + 46;
      if (d < need) {
        const push = (need - d) / 2, ux = dx / d, uy = dy / d;
        if (a !== center) { a.x -= ux * push; a.y -= uy * push; }
        if (b !== center) { b.x += ux * push; b.y += uy * push; }
        moved = true;
      }
    }
    if (!moved) break;
  }

  // ---- SVG を組み立てる
  const svg = svgEl("svg", { class: "relmap-svg", role: "img", "aria-label": T.aria });
  const defs = svgEl("defs", {}, svg);
  const clip = svgEl("clipPath", { id: "rm-clip", clipPathUnits: "objectBoundingBox" }, defs);
  svgEl("circle", { cx: 0.5, cy: 0.5, r: 0.5 }, clip);
  const view = svgEl("g", { class: "rm-view" }, svg);
  const gGroups = svgEl("g", { class: "rm-groups" }, view);
  const gEdges = svgEl("g", { class: "rm-edges" }, view);
  const gLabels = svgEl("g", { class: "rm-labels" }, view);
  const gNodes = svgEl("g", { class: "rm-nodes" }, view);
  stage.prepend(svg);

  (D.groups || []).forEach((g) => {
    const t = svgEl("text", { x: g.x, y: g.y, class: "rm-group", "text-anchor": "middle" }, gGroups);
    t.textContent = g.label;
  });

  const edges = D.links.map((l) => {
    const a = byId[l.a], b = byId[l.b];
    if (!a || !b) return null;
    const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
    const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy) || 1;
    const bend = (l.bend || 0) * len;
    const cx = mx - (dy / len) * bend, cy = my + (dx / len) * bend;
    const d = bend ? `M${a.x},${a.y} Q${cx},${cy} ${b.x},${b.y}` : `M${a.x},${a.y} L${b.x},${b.y}`;
    const path = svgEl("path", { d, class: `rm-edge t-${l.type}` }, gEdges);
    // 線の上の点（曲線なら曲線上の点）。t=0 が a、t=1 が b
    const pointAt = (t) => bend
      ? [(1 - t) * (1 - t) * a.x + 2 * (1 - t) * t * cx + t * t * b.x, (1 - t) * (1 - t) * a.y + 2 * (1 - t) * t * cy + t * t * b.y]
      : [a.x + dx * t, a.y + dy * t];
    const lg = svgEl("g", { class: `rm-label t-${l.type}` }, gLabels);
    const lines = String(l.label).split("\n");
    const bg = svgEl("rect", { rx: 6 }, lg);
    const text = svgEl("text", { "text-anchor": "middle" }, lg);
    lines.forEach((s, i) => {
      const ts = svgEl("tspan", { x: 0, dy: i === 0 ? `${-(lines.length - 1) * 0.6 + 0.35}em` : "1.2em" }, text);
      ts.textContent = s;
    });
    return { ...l, a, b, path, lg, bg, text, pointAt };
  }).filter(Boolean);

  const nodes = people.map((p) => {
    const g = svgEl("g", { class: `rm-node r-${p.role} s-${p.side}`, transform: `translate(${p.x},${p.y})`, tabindex: 0, role: "button",
      "aria-label": `${p.name}（${p.actor}）` }, gNodes);
    svgEl("circle", { r: p.r + 4, class: "rm-ring" }, g);
    if (p.img) {
      svgEl("image", { href: p.img, x: -p.r, y: -p.r, width: p.r * 2, height: p.r * 2, "clip-path": "url(#rm-clip)", preserveAspectRatio: "xMidYMid slice" }, g);
    } else {
      svgEl("circle", { r: p.r, class: "rm-ph" }, g);
      const t = svgEl("text", { class: "rm-initials", "text-anchor": "middle", dy: "0.36em", "font-size": p.r * 0.72 }, g);
      t.textContent = p.initials;
    }
    const nm = svgEl("text", { class: "rm-name", "text-anchor": "middle", y: p.r + 4 + NAME_SIZE[p.role], "font-size": NAME_SIZE[p.role] }, g);
    nm.textContent = p.short || p.name;
    const ac = svgEl("text", { class: "rm-actor", "text-anchor": "middle", y: p.r + 8 + NAME_SIZE[p.role] * 2, "font-size": Math.round(NAME_SIZE[p.role] * 0.72) }, g);
    ac.textContent = p.actor;
    p.g = g;
    return p;
  });

  // ラベルの背景の大きさを文字に合わせ、線の上で人物や他のラベルと重なりにくい位置に置く
  const rects = nodes.map((p) => { const bb = p.g.getBBox(); return { x: bb.x + p.x - 4, y: bb.y + p.y - 4, w: bb.width + 8, h: bb.height + 8 }; });
  const overlap = (r, q) => Math.max(0, Math.min(r.x + r.w, q.x + q.w) - Math.max(r.x, q.x)) * Math.max(0, Math.min(r.y + r.h, q.y + q.h) - Math.max(r.y, q.y));
  edges.forEach((ed) => {
    const bb = ed.text.getBBox();
    ed.bg.setAttribute("x", bb.x - 6); ed.bg.setAttribute("y", bb.y - 3);
    ed.bg.setAttribute("width", bb.width + 12); ed.bg.setAttribute("height", bb.height + 6);
    const w = bb.width + 12, h = bb.height + 6, prefer = ed.at == null ? 0.5 : ed.at;
    let best = null;
    for (let t = 0.15; t <= 0.851; t += 0.025) {
      const [x, y] = ed.pointAt(t);
      const r = { x: x - w / 2, y: y + bb.y - 3, w, h };
      const score = rects.reduce((sum, q) => sum + overlap(r, q), 0) + Math.abs(t - prefer) * 400;
      if (!best || score < best.score) best = { score, x, y, r };
    }
    ed.lg.setAttribute("transform", `translate(${best.x},${best.y})`);
    rects.push(best.r);
  });

  // ---- 拡大縮小と移動
  let s = 1, tx = 0, ty = 0;
  const apply = () => {
    view.setAttribute("transform", `translate(${tx},${ty}) scale(${s})`);
    stage.classList.toggle("is-far", s < 0.42);
  };
  const box = () => stage.getBoundingClientRect();
  const contentBox = () => {
    const bb = view.getBBox();
    return { x: bb.x, y: bb.y, w: bb.width, h: bb.height };
  };
  const fit = (animate, first) => {
    const b = box(), c = contentBox(), pad = 16;
    s = Math.min((b.width - pad * 2) / c.w, (b.height - pad * 2) / c.h);
    tx = b.width / 2 - (c.x + c.w / 2) * s;
    ty = b.height / 2 - (c.y + c.h / 2) * s;
    // 最初に開いたとき、スマホでは小さくなりすぎないよう、中心の2人に寄せて少し大きめに表示する（全体表示ボタンでは全体が入る）
    if (first && s < 0.5 && b.width < 760) {
      const leads = people.filter((p) => p.role === "lead");
      const cx = leads.reduce((a, p) => a + p.x, 0) / leads.length, cy = leads.reduce((a, p) => a + p.y, 0) / leads.length;
      s = 0.5;
      tx = b.width / 2 - cx * s;
      ty = b.height * 0.42 - cy * s;
    }
    if (animate) { view.classList.add("anim"); setTimeout(() => view.classList.remove("anim"), 260); }
    apply();
  };
  const zoomAt = (factor, cx, cy) => {
    const ns = Math.min(3, Math.max(0.15, s * factor));
    tx = cx - ((cx - tx) * ns) / s;
    ty = cy - ((cy - ty) * ns) / s;
    s = ns;
    apply();
  };
  const focusOn = (p) => {
    const b = box();
    const ns = Math.max(s, 0.9);
    s = ns;
    tx = b.width / 2 - p.x * s;
    if (sheetIsBottom()) {
      // スマホ：相関図を画面の上に合わせ、下から出る説明に隠れない高さに人物を置く
      window.scrollTo({ top: window.scrollY + b.top - 8 });
      const visible = Math.min(b.height, window.innerHeight - 8 - sheet.getBoundingClientRect().height);
      ty = Math.max(60, visible / 2) - p.y * s;
    } else {
      ty = b.height / 2 - p.y * s;
    }
    view.classList.add("anim"); setTimeout(() => view.classList.remove("anim"), 260);
    apply();
  };

  const pointers = new Map();
  let start = null, dragged = false, pinch = null;
  svg.addEventListener("pointerdown", (ev) => {
    svg.setPointerCapture(ev.pointerId);
    pointers.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
    dragged = false;
    if (pointers.size === 1) start = { x: ev.clientX, y: ev.clientY, tx, ty };
    if (pointers.size === 2) {
      const [p1, p2] = [...pointers.values()];
      pinch = { d: Math.hypot(p2.x - p1.x, p2.y - p1.y), s, tx, ty, mx: (p1.x + p2.x) / 2, my: (p1.y + p2.y) / 2 };
      dragged = true;
    }
  });
  svg.addEventListener("pointermove", (ev) => {
    if (!pointers.has(ev.pointerId)) return;
    pointers.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
    const b = box();
    if (pointers.size === 2 && pinch) {
      const [p1, p2] = [...pointers.values()];
      const d = Math.hypot(p2.x - p1.x, p2.y - p1.y);
      const ns = Math.min(3, Math.max(0.15, (pinch.s * d) / pinch.d));
      const mx = (p1.x + p2.x) / 2 - b.left, my = (p1.y + p2.y) / 2 - b.top;
      const ox = pinch.mx - b.left, oy = pinch.my - b.top;
      tx = mx - ((ox - pinch.tx) * ns) / pinch.s;
      ty = my - ((oy - pinch.ty) * ns) / pinch.s;
      s = ns;
      apply();
    } else if (pointers.size === 1 && start) {
      const dx = ev.clientX - start.x, dy = ev.clientY - start.y;
      if (Math.abs(dx) + Math.abs(dy) > 6) dragged = true;
      if (dragged) { tx = start.tx + dx; ty = start.ty + dy; apply(); }
    }
  });
  const up = (ev) => {
    const wasTap = !dragged && pointers.size === 1;
    pointers.delete(ev.pointerId);
    if (pointers.size < 2) pinch = null;
    if (pointers.size === 1) { const [p] = [...pointers.values()]; start = { x: p.x, y: p.y, tx, ty }; }
    if (wasTap && ev.type === "pointerup") {
      const hit = document.elementFromPoint(ev.clientX, ev.clientY);
      const g = hit && hit.closest(".rm-node");
      const p = g && nodes.find((n) => n.g === g);
      if (p) select(p, sheetIsBottom()); else select(null);
    }
  };
  svg.addEventListener("pointerup", up);
  svg.addEventListener("pointercancel", up);
  svg.addEventListener("wheel", (ev) => {
    ev.preventDefault();
    const b = box();
    zoomAt(Math.exp(-ev.deltaY * 0.0015), ev.clientX - b.left, ev.clientY - b.top);
  }, { passive: false });

  document.getElementById("rm-zoom-in").addEventListener("click", () => { const b = box(); zoomAt(1.3, b.width / 2, b.height / 2); });
  document.getElementById("rm-zoom-out").addEventListener("click", () => { const b = box(); zoomAt(1 / 1.3, b.width / 2, b.height / 2); });
  document.getElementById("rm-fit").addEventListener("click", () => { select(null); fit(true); });

  // ---- 関係の種類で絞り込む
  const hiddenTypes = new Set();
  document.querySelectorAll("[data-rm-type]").forEach((btn) => btn.addEventListener("click", () => {
    const t = btn.dataset.rmType;
    hiddenTypes.has(t) ? hiddenTypes.delete(t) : hiddenTypes.add(t);
    btn.setAttribute("aria-pressed", String(!hiddenTypes.has(t)));
    edges.forEach((ed) => {
      const off = hiddenTypes.has(ed.type);
      ed.path.classList.toggle("off", off);
      ed.lg.classList.toggle("off", off);
    });
  }));

  // ---- 人物の説明（スマホは画面下、PCは右側に開く）
  const sheet = document.getElementById("rm-sheet");
  const sheetBody = document.getElementById("rm-sheet-body");
  const sheetIsBottom = () => window.matchMedia("(max-width: 759px)").matches;
  const avatarHtml = (p, size) => p.img
    ? `<img src="${esc(p.img)}" alt="" width="${size}" height="${size}">`
    : `<span class="rm-ph-html s-${p.side} r-${p.role}" style="width:${size}px;height:${size}px;font-size:${size * 0.36}px">${esc(p.initials)}</span>`;
  let current = null;
  function select(p, center) {
    current = p;
    stage.classList.toggle("has-sel", !!p);
    nodes.forEach((n) => n.g.classList.toggle("sel", n === p));
    const linked = new Set();
    edges.forEach((ed) => {
      const on = p && (ed.a === p || ed.b === p);
      ed.path.classList.toggle("hl", !!on);
      ed.lg.classList.toggle("hl", !!on);
      if (on) { linked.add(ed.a); linked.add(ed.b); }
    });
    nodes.forEach((n) => n.g.classList.toggle("near", !!p && linked.has(n)));
    if (!p) { sheet.hidden = true; return; }
    const rels = edges.filter((ed) => ed.a === p || ed.b === p).map((ed) => {
      const o = ed.a === p ? ed.b : ed.a;
      return `<li><button type="button" class="rm-rel" data-goto="${esc(o.id)}">${avatarHtml(o, 32)}<span><b>${esc(o.name)}</b><small><span class="rm-chip t-${ed.type}">${esc(T.types[ed.type])}</span>${esc(String(ed.label).replace(/\n/g, " "))}</small></span></button></li>`;
    }).join("");
    const credit = p.credit
      ? `<p class="rm-credit">${T.photo}: <a href="${esc(p.credit.source_url)}" target="_blank" rel="noopener">${esc(p.credit.author)}</a> / <a href="${esc(p.credit.license_url)}" target="_blank" rel="noopener">${esc(p.credit.license)}</a></p>`
      : `<p class="rm-credit">${esc(T.placeholder)}</p>`;
    sheetBody.innerHTML = `
      <div class="rm-who">${avatarHtml(p, 72)}<div><p class="rm-group-tag s-${p.side}">${esc(p.group)}</p><h3 id="rm-sheet-title">${esc(p.name)}</h3><p class="rm-actor-line">${esc(T.actor)}: ${esc(p.actor)}</p></div></div>
      <p>${esc(p.desc)}</p>
      <h4>${esc(T.relations)}</h4><ul class="rm-rels">${rels}</ul>${credit}`;
    sheet.hidden = false;
    sheetBody.scrollTop = 0;
    if (center) focusOn(p);
  }
  sheetBody.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-goto]");
    if (b) select(byId[b.dataset.goto], true);
  });
  document.getElementById("rm-close").addEventListener("click", () => select(null));
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && current) select(null); });
  nodes.forEach((p) => p.g.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); select(p, true); }
  }));
  // ページ下の一覧からも開ける
  document.querySelectorAll("[data-rm-open]").forEach((a) => a.addEventListener("click", (ev) => {
    ev.preventDefault();
    stage.scrollIntoView({ behavior: "smooth", block: "start" });
    select(byId[a.dataset.rmOpen], true);
  }));

  fit(false, true);
  let lastW = box().width;
  window.addEventListener("resize", () => { const w = box().width; if (Math.abs(w - lastW) > 40) { lastW = w; fit(false); } });
  stage.classList.add("ready");
})();
