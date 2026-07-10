/* Private visitor counter.
 * - Real visitors increment a shared count (deduped to once per 6h per browser).
 * - Only the owner sees the number; the owner's own visits are read-only (never counted).
 * Owner mode is toggled per browser via the URL hash:
 *     https://www.hanbaeklyu.com/#stats-on    -> start showing the counter here
 *     https://www.hanbaeklyu.com/#stats-off   -> hide it again
 * The choice is remembered in localStorage, so you set it once per device. */
(function () {
  var API = "https://abacus.jasoncameron.dev";
  var NS = "hanbaeklyu.com", KEY = "visits";

  var owner = false;
  try {
    if (location.hash === "#stats-on") localStorage.setItem("hl_owner", "1");
    if (location.hash === "#stats-off") localStorage.removeItem("hl_owner");
    owner = localStorage.getItem("hl_owner") === "1";
  } catch (e) {}

  if (owner) {
    // read-only: show the number, do not increment
    fetch(API + "/get/" + NS + "/" + KEY)
      .then(function (r) { return r.json(); })
      .then(function (d) { show((d && (d.value != null ? d.value : d.count)) || 0); })
      .catch(function () {});
    return;
  }

  // visitor: increment at most once per 6 hours per browser
  var count = true;
  try {
    var last = +localStorage.getItem("hl_last") || 0;
    count = (Date.now() - last) > 6 * 3600 * 1000;
  } catch (e) {}
  if (!count) return;
  fetch(API + "/hit/" + NS + "/" + KEY).catch(function () {});
  try { localStorage.setItem("hl_last", String(Date.now())); } catch (e) {}

  function show(n) {
    var el = document.createElement("div");
    el.textContent = "👁 " + Number(n).toLocaleString() + " visits";
    el.title = "Visible only to you · add #stats-off to the URL to hide";
    el.style.cssText =
      "position:fixed;right:10px;bottom:10px;z-index:1000;" +
      "background:rgba(26,26,26,.85);color:#fff;" +
      "font:12px/1.4 -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;" +
      "padding:4px 10px;border-radius:12px;pointer-events:none;" +
      "box-shadow:0 1px 4px rgba(0,0,0,.25)";
    document.body.appendChild(el);
  }
})();
