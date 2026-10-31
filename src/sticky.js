// 画面下の広告バー。閉じたらそのタブでは出さない
(function () {
  const bar = document.getElementById("sticky-ad");
  if (!bar) return;
  let closed = false;
  try { closed = sessionStorage.getItem("sticky-ad-closed") === "1"; } catch (e) {}
  bar.hidden = closed;
  document.body.classList.toggle("has-sticky", !closed);
  document.getElementById("sticky-ad-close").addEventListener("click", () => {
    bar.hidden = true;
    document.body.classList.remove("has-sticky");
    try { sessionStorage.setItem("sticky-ad-closed", "1"); } catch (e) {}
  });
})();
