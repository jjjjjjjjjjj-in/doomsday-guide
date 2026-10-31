// 視聴チェック・表示切り替え・進捗・カウントダウン
(function () {
  const STORE_KEY = "doomsday-watched-v2";
  let watched = new Set();
  try { watched = new Set(JSON.parse(localStorage.getItem(STORE_KEY) || "[]")); } catch (e) {}
  const save = () => { try { localStorage.setItem(STORE_KEY, JSON.stringify([...watched])); } catch (e) {} };

  const rows = [...document.querySelectorAll(".row[data-slug]")];
  const home = new Map(rows.map((r) => [r, r.parentElement]));
  const priorityView = document.getElementById("priority-view");
  const orderView = document.getElementById("order-view");
  const orderList = document.getElementById("order-list");
  const hideDone = document.getElementById("hide-done");

  function paint() {
    rows.forEach((r) => {
      const done = watched.has(r.dataset.slug);
      r.classList.toggle("done", done);
      r.hidden = hideDone.checked && done;
      const box = r.querySelector("input[type=checkbox]");
      if (box) box.checked = done;
    });
    const count = (sel) => {
      const list = rows.filter((r) => r.matches(sel));
      return [list.filter((r) => watched.has(r.dataset.slug)).length, list.length];
    };
    [["must", ".row.must"], ["all", ".row:not(.goal)"]].forEach(([key, sel]) => {
      const [done, total] = count(sel);
      document.getElementById(`progress-${key}`).innerHTML = `${done}<span>/ ${total}本</span>`;
      document.getElementById(`bar-${key}`).style.width = `${total ? (done / total) * 100 : 0}%`;
    });
  }

  document.addEventListener("change", (e) => {
    const slug = e.target.dataset && e.target.dataset.watch;
    if (!slug) return;
    e.target.checked ? watched.add(slug) : watched.delete(slug);
    save();
    paint();
  });
  hideDone.addEventListener("change", paint);

  // 優先度別 ⇔ 視聴順
  function setView(view) {
    document.querySelectorAll("[data-view]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.view === view)));
    const byOrder = [...rows].sort((a, b) => a.dataset.order - b.dataset.order);
    if (view === "order") {
      byOrder.forEach((r) => orderList.appendChild(r));
    } else {
      byOrder.forEach((r) => home.get(r).appendChild(r));
    }
    priorityView.hidden = view === "order";
    orderView.hidden = view !== "order";
    try { localStorage.setItem("doomsday-view", view); } catch (e) {}
  }
  document.querySelectorAll("[data-view]").forEach((b) => b.addEventListener("click", () => setView(b.dataset.view)));
  let initial = "priority";
  try { initial = localStorage.getItem("doomsday-view") || "priority"; } catch (e) {}
  setView(initial);

  // 記事から作品へのリンクで飛んできたら詳細を開く
  function openFromHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    const el = id && document.getElementById(id);
    if (el && el.classList.contains("row")) {
      const d = el.querySelector("details");
      if (d) d.open = true;
      el.scrollIntoView({ block: "start" });
    }
  }
  window.addEventListener("hashchange", openFromHash);

  // 公開日（日本時間 2026/12/18）までの日数
  const release = new Date("2026-12-18T00:00:00+09:00");
  const days = Math.ceil((release - new Date()) / 86400000);
  document.getElementById("countdown").innerHTML = days > 0 ? `${days}<span>日</span>` : "公開中";

  paint();
  openFromHash();
})();
