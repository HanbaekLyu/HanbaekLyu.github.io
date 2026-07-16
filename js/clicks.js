/* Track file downloads and outbound-link clicks as GoatCounter events.
 * Events show up in the dashboard's Pages panel with a "event" flag, e.g.
 *     file: CV.pdf          (a file was downloaded/opened)
 *     link: arxiv.org/...    (an external link was clicked)
 * Depends on GoatCounter's count.js (window.goatcounter). */
(function () {
  var FILE_RE = /\.(pdf|pptx?|key|zip|csv|txt|png|jpe?g|gif|svg)(\?|#|$)/i;

  function track(path, title) {
    if (window.goatcounter && window.goatcounter.count) {
      window.goatcounter.count({ path: path, title: title || path, event: true });
    }
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || /^(javascript|mailto|tel):/i.test(href)) return;

    var url;
    try { url = new URL(href, location.href); } catch (_) { return; }

    if (FILE_RE.test(url.pathname)) {
      track("file: " + url.pathname.split("/").pop(), "Download " + url.pathname);
    } else if (url.host !== location.host) {
      track("link: " + url.host + url.pathname, "Outbound " + url.href);
    }
  }, true);
})();
