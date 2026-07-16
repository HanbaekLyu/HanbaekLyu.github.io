/* Rock-solid tracking of file downloads and outbound-link clicks as GoatCounter events.
 * - External links (incl. arXiv .pdf links) record their full path, e.g.
 *       link: arxiv.org/abs/2407.14942
 *   so you can always tell which link/paper was clicked.
 * - Local file downloads record the filename, e.g.  file: CV.pdf
 * - The private GoatCounter dashboard link (the owner "Analytics" button) is ignored.
 * Delivery uses fetch({keepalive:true}) (falls back to sendBeacon / Image) so the
 * event completes even if the page navigates or the tab is backgrounded — mobile too.
 * Tracked links also open in a new tab (keeps visitors on the site). */
(function () {
  var FILE_RE = /\.(pdf|pptx?|key|zip|csv|txt|png|jpe?g|gif|svg)(\?|#|$)/i;

  var sc = document.querySelector("script[data-goatcounter]");
  var ENDPOINT = sc ? sc.getAttribute("data-goatcounter") : null;

  function kindOf(url) {
    if (/(^|\.)goatcounter\.com$/i.test(url.host)) return null;  // owner dashboard link
    if (url.host !== location.host) return "link";               // external first
    if (FILE_RE.test(url.pathname)) return "file";               // local download
    return null;
  }
  function parse(a) {
    var href = a && a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || /^(javascript|mailto|tel):/i.test(href)) return null;
    try { return new URL(href, location.href); } catch (_) { return null; }
  }
  function send(path, title) {
    if (!ENDPOINT) return;
    var u = ENDPOINT +
      "?p=" + encodeURIComponent(path) +
      "&t=" + encodeURIComponent(title || path) +
      "&e=true" +
      "&r=" + encodeURIComponent(document.referrer || "") +
      "&rnd=" + Math.random().toString(36).slice(2);
    try { if (window.fetch) { fetch(u, { mode: "no-cors", keepalive: true }); return; } } catch (_) {}
    try { if (navigator.sendBeacon) { navigator.sendBeacon(u); return; } } catch (_) {}
    new Image().src = u;
  }

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

  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[href]") : null;
    var url = parse(a);
    if (!url) return;
    var kind = kindOf(url);
    if (kind === "file") {
      send("file: " + url.pathname.split("/").pop(), "Download " + url.pathname);
    } else if (kind === "link") {
      send("link: " + url.host + url.pathname + url.search, "Outbound " + url.href);
    }
  }, true);
})();
