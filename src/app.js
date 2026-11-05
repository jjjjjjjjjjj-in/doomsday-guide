// 視聴チェック・表示切り替え・進捗・カウントダウン
(function () {
  const STORE_KEY = "doomsday-watched-v2";
  let watched = new Set();
  try { watched = new Set(JSON.parse(localStorage.getItem(STORE_KEY) || "[]")); } catch (e) {}
  const save = () => { try { localStorage.setItem(STORE_KEY, JSON.stringify([...watched])); } catch (e) {} };

  const EN = document.documentElement.lang === "en";
  const rows = [...document.querySelectorAll(".row[data-slug]")];
  const hideDone = document.getElementById("hide-done");
  const onlyOfficial = document.getElementById("only-official");
  const shareBox = document.getElementById("share");
  const shareProgress = document.getElementById("share-progress");
  const release = new Date("2026-12-18T00:00:00+09:00");
  const daysLeft = () => Math.ceil((release - new Date()) / 86400000);

  // 公式15作品の進み具合（ロキはシーズン1・2を両方観たら1本）
  function officialCount() {
    const groups = {};
    rows.filter((r) => r.dataset.official).forEach((r) => {
      (groups[r.dataset.official] = groups[r.dataset.official] || new Set()).add(r.dataset.slug);
    });
    const keys = Object.keys(groups);
    return [keys.filter((k) => [...groups[k]].every((s) => watched.has(s))).length, keys.length];
  }

  // 観た本数を入れたシェア文
  function updateShare(o, ot, m, mt) {
    if (!shareBox || !shareProgress) return;
    const d = daysLeft();
    const text = EN
      ? `Avengers: Doomsday prep: ${o}/${ot} of the Official 15 watched (${m}/${mt} must-watch titles).${d > 0 ? ` ${d} days to go!` : ""}`
      : `ドゥームズデイ予習、公式15作品のうち${o}本観た！（必ず観るべき作品は${m}/${mt}本）${d > 0 ? `公開まであと${d}日` : ""}`;
    shareProgress.href = "https://x.com/intent/post?text=" + encodeURIComponent(text) +
      "&url=" + encodeURIComponent(shareBox.dataset.url) + "&hashtags=" + encodeURIComponent(shareBox.dataset.tag);
  }

  function paint() {
    rows.forEach((r) => {
      const done = watched.has(r.dataset.slug);
      r.classList.toggle("done", done);
      r.hidden = (hideDone.checked && done) || (onlyOfficial && onlyOfficial.checked && !r.dataset.official && !r.classList.contains("goal"));
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
    const [o, ot] = officialCount();
    const po = document.getElementById("progress-official");
    if (po) {
      po.innerHTML = `${o}<span>/ ${ot}${EN ? "" : "本"}</span>`;
      document.getElementById("bar-official").style.width = `${ot ? (o / ot) * 100 : 0}%`;
    }
    updateShare(o, ot, ...count(".row.must"));
  }

  document.addEventListener("change", (e) => {
    const slug = e.target.dataset && e.target.dataset.watch;
    if (!slug) return;
    e.target.checked ? watched.add(slug) : watched.delete(slug);
    save();
    paint();
  });
  hideDone.addEventListener("change", paint);
  if (onlyOfficial) onlyOfficial.addEventListener("change", paint);

  // リンクをコピー
  const copyBtn = document.getElementById("copy-link");
  if (copyBtn && shareBox) {
    copyBtn.addEventListener("click", () => {
      const label = copyBtn.textContent;
      const done = () => { copyBtn.textContent = copyBtn.dataset.done; setTimeout(() => { copyBtn.textContent = label; }, 2000); };
      try {
        navigator.clipboard.writeText(shareBox.dataset.url).then(done, () => window.prompt("URL", shareBox.dataset.url));
      } catch (e) { window.prompt("URL", shareBox.dataset.url); }
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
  const days = daysLeft();
  document.getElementById("countdown").innerHTML = days > 0 ? `${days}<span>${EN ? "days" : "日"}</span>` : (EN ? "Out now" : "公開中");

  paint();
  openFromHash();
})();
