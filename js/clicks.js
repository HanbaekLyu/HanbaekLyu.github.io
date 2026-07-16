/* Rock-solid tracking of file downloads and outbound-link clicks as GoatCounter events.
 * Strategy: tracked links (files + external) are made to open in a new tab, so THIS page
 * never unloads on click and the GoatCounter event beacon always completes.
 * Events appear in the dashboard's Pages panel flagged as events, e.g.
 *     file: CV.pdf           link: arxiv.org/abs/2407.14942
 * Internal navigation links are left untouched. Depends on GoatCounter's count.js. */
(function () {
  var FILE_RE = /\.(pdf|pptx?|key|zip|csv|txt|png|jpe?g|gif|svg)(\?|#|$)/i;

  function kindOf(url) {
    if (FILE_RE.test(url.pathname)) return "file";
    if (url.host !== location.host) return "link";
    return null;
  }
  function parse(a) {
    var href = a && a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || /^(javascript|mailto|tel):/i.test(href)) return null;
    try { return new URL(href, location.href); } catch (_) { return null; }
  }

  // Make tracked links open in a new tab (so this page stays put on click).
  function markLinks() {
    var links = document.getElementsByTagName("a"), i, a, url;
    for (i = 0; i < links.length; i++) {
      a = links[i];
      if (a.target) continue;
      url = parse(a);
      if (url && kindOf(url)) { a.target = "_blank"; a.rel = "noopener"; }
    }
  }
  if (document.readyState !== "loading") markLinks();
  else document.addEventListener("DOMContentLoaded", markLinks);

  function track(path, title) {
    if (window.goatcounter && window.goatcounter.count) {
      window.goatcounter.count({ path: path, title: title || path, event: true });
    }
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[href]") : null;
    var url = parse(a);
    if (!url) return;
    var kind = kindOf(url);
    if (kind === "file") track("file: " + url.pathname.split("/").pop(), "Download " + url.pathname);
    else if (kind === "link") track("link: " + url.host + url.pathname, "Outbound " + url.href);
  }, true);
})();
