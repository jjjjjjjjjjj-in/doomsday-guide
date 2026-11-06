// 視聴チェック・表示切り替え・進捗・カウントダウン
(function () {
  const STORE_KEY = "doomsday-watched-v2";
  let watched = new Set();
  try { watched = new Set(JSON.parse(localStorage.getItem(STORE_KEY) || "[]")); } catch (e) {}
  const save = () => { try { localStorage.setItem(STORE_KEY, JSON.stringify([...watched])); } catch (e) {} };

  const EN = document.documentElement.lang === "en";
  const rows = [...document.querySelectorAll(".row[data-slug]")];
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
      const slugs = [...new Set(rows.filter((r) => r.matches(sel)).map((r) => r.dataset.slug))];
      return [slugs.filter((s) => watched.has(s)).length, slugs.length];
    };
    [["must", ".row.must"], ["all", ".row:not(.goal)"]].forEach(([key, sel]) => {
      const [done, total] = count(sel);
      document.getElementById(`progress-${key}`).innerHTML = `${done}<span>/ ${total}${EN ? "" : "本"}</span>`;
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

  // ホーム画面から開いているときは「ホーム画面に追加」の案内を出さない
  const standalone = window.navigator.standalone === true ||
    (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches);
  const tip = document.getElementById("home-tip");
  if (tip && standalone) tip.hidden = true;

  // リンクをコピー
  const copyBtn = document.getElementById("copy-link");
  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      const url = copyBtn.dataset.url;
      const el = copyBtn.querySelector(".app-label") || copyBtn;
      const label = el.textContent;
      const done = () => { el.textContent = copyBtn.dataset.done; copyBtn.classList.add("copied"); setTimeout(() => { el.textContent = label; copyBtn.classList.remove("copied"); }, 2000); };
      try { navigator.clipboard.writeText(url).then(done, () => window.prompt("URL", url)); } catch (e) { window.prompt("URL", url); }
    });
  }

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
  document.getElementById("countdown").innerHTML = days > 0 ? `${days}<span>${EN ? "days" : "日"}</span>` : (EN ? "Out now" : "公開中");

  paint();
  openFromHash();
})();
