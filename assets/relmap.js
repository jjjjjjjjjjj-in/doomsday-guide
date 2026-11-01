// キャラクター相関図：データ（#relmap-data）から SVG を描き、ドラッグで移動・ピンチ／ホイールで拡大縮小・タップで人物の説明を開く
// 人物は写真カード（四角）。関係は矢印で、向きごとに短い言葉（ab: a→b、ba: b→a）。向きのない関係は label。
(function () {
  const dataEl = document.getElementById("relmap-data");
  const stage = document.getElementById("relmap");
  if (!dataEl || !stage) return;
  const D = JSON.parse(dataEl.textContent);
  const T = D.text;
  const NS = "http://www.w3.org/2000/svg";
  // カードの大きさ（幅・写真の高さ・名前欄の高さ）
  const CARD = { lead: [176, 176, 62], main: [138, 138, 54], sub: [116, 116, 50] };
  const svgEl = (tag, attrs, parent) => {
    const el = document.createElementNS(NS, tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // ---- 位置（x,y がなければ中心のまわりに自動で並べ、重なれば押し広げる）
  const people = D.people.map((p) => {
    const [w, ph, nh] = CARD[p.role] || CARD.sub;
    return { ...p, w, ph, nh, h: ph + nh };
  });
  const byId = Object.fromEntries(people.map((p) => [p.id, p]));
  const center = byId[D.center] || people[0];
  const auto = people.filter((p) => p.x == null);
  auto.forEach((p, i) => {
    const a = p.angle != null ? (p.angle * Math.PI) / 180 : (2 * Math.PI * i) / auto.length - Math.PI / 2;
    const dist = (p.ring || 2) === 1 ? 320 : 560;
    p.x = (center.x || 0) + Math.cos(a) * dist;
    p.y = (center.y || 0) + Math.sin(a) * dist;
  });
  for (let k = 0; k < 80; k++) {
    let moved = false;
    for (let i = 0; i < people.length; i++) for (let j = i + 1; j < people.length; j++) {
      const a = people[i], b = people[j];
      const ox = (a.w + b.w) / 2 + 60 - Math.abs(b.x - a.x), oy = (a.h + b.h) / 2 + 60 - Math.abs(b.y - a.y);
      if (ox > 0 && oy > 0) {
        const horiz = ox < oy, push = (horiz ? ox : oy) / 2, sx = Math.sign(b.x - a.x) || 1, sy = Math.sign(b.y - a.y) || 1;
        if (a !== center) { if (horiz) a.x -= sx * push; else a.y -= sy * push; }
        if (b !== center) { if (horiz) b.x += sx * push; else b.y += sy * push; }
        moved = true;
      }
    }
    if (!moved) break;
  }

  // ---- SVG を組み立てる
  const svg = svgEl("svg", { class: "relmap-svg", role: "img", "aria-label": T.aria });
  const defs = svgEl("defs", {}, svg);
  ["love", "family", "friend", "ally", "enemy", "org"].forEach((t) => {
    const m = svgEl("marker", { id: `rm-arrow-${t}`, viewBox: "0 0 10 10", refX: 8.5, refY: 5, markerWidth: 5.5, markerHeight: 5.5, orient: "auto-start-reverse", markerUnits: "strokeWidth" }, defs);
    svgEl("path", { d: "M0,0 L10,5 L0,10 z", class: `rm-head t-${t}` }, m);
  });
  const view = svgEl("g", { class: "rm-view" }, svg);
  const gGroups = svgEl("g", { class: "rm-groups" }, view);
  const gEdges = svgEl("g", { class: "rm-edges" }, view);
  const gNodes = svgEl("g", { class: "rm-nodes" }, view);
  const gLabels = svgEl("g", { class: "rm-labels" }, view);
  stage.prepend(svg);

  (D.groups || []).forEach((g) => {
    const t = svgEl("text", { x: g.x, y: g.y, class: "rm-group", "text-anchor": "middle" }, gGroups);
    t.textContent = g.label;
  });

  // カードの縁で線を止める（中心から相手の方向へ伸ばしたとき、四角の外周と交わる点）
  const edgePoint = (p, tx, ty, pad) => {
    const dx = tx - p.x, dy = ty - p.y;
    const hw = p.w / 2 + pad, hh = p.h / 2 + pad;
    const k = 1 / Math.max(Math.abs(dx) / hw, Math.abs(dy) / hh, 1e-6);
    return [p.x + dx * k, p.y + dy * k];
  };

  const edges = [];
  D.links.forEach((l) => {
    const a = byId[l.a], b = byId[l.b];
    if (!a || !b) return;
    const dirs = [];
    if (l.ab) dirs.push({ from: a, to: b, text: l.ab });
    if (l.ba) dirs.push({ from: b, to: a, text: l.ba });
    if (!dirs.length) dirs.push({ from: a, to: b, text: l.label || "", plain: true });
    const both = dirs.length === 2;
    const parts = dirs.map((d, i) => {
      // 2方向あるときは、線を少し左右にずらして2本並べる
      const dx = d.to.x - d.from.x, dy = d.to.y - d.from.y, len = Math.hypot(dx, dy) || 1;
      const off = both ? 9 : 0, nx = (-dy / len) * off, ny = (dx / len) * off;
      const bend = (l.bend || 0) * len * (d.from === a ? 1 : -1);
      const mx = (d.from.x + d.to.x) / 2 + nx, my = (d.from.y + d.to.y) / 2 + ny;
      const cx = mx - (dy / len) * bend, cy = my + (dx / len) * bend;
      const aim = (p, q) => (bend ? [cx, cy] : [q.x + nx, q.y + ny]);
      const [x1, y1] = edgePoint({ ...d.from, x: d.from.x + nx, y: d.from.y + ny }, ...aim(d.from, d.to), 4);
      const [x2, y2] = edgePoint({ ...d.to, x: d.to.x + nx, y: d.to.y + ny }, ...aim(d.to, d.from), 6);
      const path = svgEl("path", {
        d: bend ? `M${x1},${y1} Q${cx},${cy} ${x2},${y2}` : `M${x1},${y1} L${x2},${y2}`,
        class: `rm-edge t-${l.type}`, "marker-end": d.plain ? "" : `url(#rm-arrow-${l.type})`,
      }, gEdges);
      const pointAt = (t) => bend
        ? [(1 - t) * (1 - t) * x1 + 2 * (1 - t) * t * cx + t * t * x2, (1 - t) * (1 - t) * y1 + 2 * (1 - t) * t * cy + t * t * y2]
        : [x1 + (x2 - x1) * t, y1 + (y2 - y1) * t];
      const lg = svgEl("g", { class: `rm-label t-${l.type}` }, gLabels);
      const lines = String(d.text).split("\n");
      const bg = svgEl("rect", { rx: 7 }, lg);
      const text = svgEl("text", { "text-anchor": "middle" }, lg);
      lines.forEach((s, i2) => {
        const ts = svgEl("tspan", { x: 0, dy: i2 === 0 ? `${-(lines.length - 1) * 0.6 + 0.35}em` : "1.2em" }, text);
        ts.textContent = s;
      });
      // 2方向のときは、それぞれの言葉を矢印の出発側に寄せる
      return { path, lg, bg, text, pointAt, prefer: both ? 0.5 : (l.at == null ? 0.5 : l.at), side: both ? 1 : 0 };
    });
    const label = dirs.map((d) => (d.plain ? d.text.replace(/\n/g, " ") : `${d.from.short}→${d.to.short}「${d.text.replace(/\n/g, " ")}」`)).join(" / ");
    edges.push({ ...l, a, b, parts, label });
  });

  const nodes = people.map((p) => {
    const g = svgEl("g", { class: `rm-node r-${p.role} tone-${p.tone || "gold"}`, transform: `translate(${p.x},${p.y})`, tabindex: 0, role: "button",
      "aria-label": `${p.name}（${p.actor}）` }, gNodes);
    const x0 = -p.w / 2, y0 = -p.h / 2;
    svgEl("rect", { x: x0 - 5, y: y0 - 5, width: p.w + 10, height: p.h + 10, rx: 14, class: "rm-frame" }, g);
    const clipId = `rm-c-${p.id}`;
    const cp = svgEl("clipPath", { id: clipId }, defs);
    svgEl("rect", { x: x0, y: y0, width: p.w, height: p.ph, rx: 9 }, cp);
    if (p.img) {
      svgEl("image", { href: p.img, x: x0, y: y0, width: p.w, height: p.ph, "clip-path": `url(#${clipId})`, preserveAspectRatio: "xMidYMid slice" }, g);
    } else {
      svgEl("rect", { x: x0, y: y0, width: p.w, height: p.ph, rx: 9, class: "rm-ph" }, g);
      // 仮の顔アイコン（シルエット＋頭文字）
      const cx = 0, top = y0 + p.ph * 0.2, r = p.ph * 0.2;
      svgEl("circle", { cx, cy: top + r, r, class: "rm-sil" }, g);
      svgEl("path", { d: `M${-p.w * 0.36},${y0 + p.ph} Q${-p.w * 0.36},${top + r * 2.3} 0,${top + r * 2.3} Q${p.w * 0.36},${top + r * 2.3} ${p.w * 0.36},${y0 + p.ph} Z`, class: "rm-sil", "clip-path": `url(#${clipId})` }, g);
      const t = svgEl("text", { class: "rm-initials", "text-anchor": "middle", x: 0, y: y0 + p.ph - p.ph * 0.1, "font-size": p.ph * 0.2 }, g);
      t.textContent = p.initials;
    }
    const ny = y0 + p.ph;
    svgEl("rect", { x: x0, y: ny - 2, width: p.w, height: p.nh + 2, class: "rm-band" }, g);
    const fs = { lead: 22, main: 18, sub: 15.5 }[p.role] || 15.5;
    const nm = svgEl("text", { class: "rm-name", "text-anchor": "middle", x: 0, y: ny + p.nh * 0.46, "font-size": fs }, g);
    nm.textContent = p.short || p.name;
    const ac = svgEl("text", { class: "rm-actor", "text-anchor": "middle", x: 0, y: ny + p.nh * 0.82, "font-size": Math.round(fs * 0.66) }, g);
    ac.textContent = p.actor;
    // 名前が枠からはみ出すときは縮める
    [nm, ac].forEach((el) => { const w = el.getComputedTextLength(); if (w > p.w - 10) el.setAttribute("textLength", p.w - 10), el.setAttribute("lengthAdjust", "spacingAndGlyphs"); });
    if (p.badge) {
      const bx = p.w / 2 - 4, by = y0 + 2, br = { lead: 30, main: 26, sub: 23 }[p.role] || 23;
      const bgc = svgEl("g", { class: "rm-badge", transform: `translate(${bx},${by})` }, g);
      svgEl("circle", { r: br }, bgc);
      const lines = p.badge.split("\n");
      const bt = svgEl("text", { "text-anchor": "middle", "font-size": br * (lines.length > 1 ? 0.52 : (p.badge.length > 3 ? 0.5 : 0.62)) }, bgc);
      lines.forEach((s, i) => { const ts = svgEl("tspan", { x: 0, dy: i === 0 ? `${-(lines.length - 1) * 0.55 + 0.36}em` : "1.1em" }, bt); ts.textContent = s; });
    }
    p.g = g;
    return p;
  });

  // ラベルの背景の大きさを文字に合わせ、線の上でカードや他のラベルと重なりにくい位置に置く
  const rects = nodes.map((p) => { const bb = p.g.getBBox(); return { x: bb.x + p.x - 4, y: bb.y + p.y - 4, w: bb.width + 8, h: bb.height + 8 }; });
  const overlap = (r, q) => Math.max(0, Math.min(r.x + r.w, q.x + q.w) - Math.max(r.x, q.x)) * Math.max(0, Math.min(r.y + r.h, q.y + q.h) - Math.max(r.y, q.y));
  edges.forEach((ed) => ed.parts.forEach((pt) => {
    const bb = pt.text.getBBox();
    pt.bg.setAttribute("x", bb.x - 7); pt.bg.setAttribute("y", bb.y - 4);
    pt.bg.setAttribute("width", bb.width + 14); pt.bg.setAttribute("height", bb.height + 8);
    const w = bb.width + 14, h = bb.height + 8;
    let best = null;
    for (let t = 0.1; t <= 0.901; t += 0.025) {
      let [x, y] = pt.pointAt(t);
      if (pt.side) {
        // 2方向の言葉は、線をはさんで反対側に置く
        const [xa, ya] = pt.pointAt(Math.max(0, t - 0.02)), [xb, yb] = pt.pointAt(Math.min(1, t + 0.02));
        const len = Math.hypot(xb - xa, yb - ya) || 1, nx = -(yb - ya) / len, ny = (xb - xa) / len;
        const d = Math.abs(nx) * (w / 2 + 6) + Math.abs(ny) * (h / 2 + 6);
        x += nx * d * pt.side; y += ny * d * pt.side;
      }
      const r = { x: x - w / 2, y: y + bb.y - 4, w, h };
      const score = rects.reduce((sum, q) => sum + overlap(r, q), 0) + Math.abs(t - pt.prefer) * 500;
      if (!best || score < best.score) best = { score, x, y, r };
    }
    pt.lg.setAttribute("transform", `translate(${best.x},${best.y})`);
    rects.push(best.r);
  }));
  // 古い書き方との互換：選んだ人物の線を強調するときに使う
  edges.forEach((ed) => {
    ed.path = { classList: { toggle: (c, v) => ed.parts.forEach((pt) => pt.path.classList.toggle(c, v)) } };
    ed.lg = { classList: { toggle: (c, v) => ed.parts.forEach((pt) => pt.lg.classList.toggle(c, v)) } };
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
    : `<span class="rm-ph-html tone-${p.tone || "gold"} r-${p.role}" style="width:${size}px;height:${size}px;font-size:${size * 0.36}px">${esc(p.initials)}</span>`;
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
      return `<li><button type="button" class="rm-rel" data-goto="${esc(o.id)}">${avatarHtml(o, 32)}<span><b>${esc(o.name)}</b><small><span class="rm-chip t-${ed.type}">${esc(T.types[ed.type])}</span>${esc(ed.label)}</small></span></button></li>`;
    }).join("");
    const credit = p.credit && p.credit.illustration
      ? `<p class="rm-credit">${esc(T.illus)}</p>`
      : p.credit
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
