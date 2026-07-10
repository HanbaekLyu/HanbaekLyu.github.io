/* Owner-only "Analytics" button linking to the private GoatCounter dashboard.
 * Enable on a device once by visiting any page with #stats-on in the URL:
 *     https://www.hanbaeklyu.com/#stats-on    -> show the button here
 *     https://www.hanbaeklyu.com/#stats-off   -> hide it again
 * The choice is remembered per browser in localStorage. Visitors never see it. */
(function () {
  var DASHBOARD = "https://colourgraph.goatcounter.com";
  var owner = false;
  try {
    if (location.hash === "#stats-on") localStorage.setItem("hl_owner", "1");
    if (location.hash === "#stats-off") localStorage.removeItem("hl_owner");
    owner = localStorage.getItem("hl_owner") === "1";
  } catch (e) {}
  if (!owner) return;

  var a = document.createElement("a");
  a.href = DASHBOARD;
  a.target = "_blank";
  a.rel = "noopener";
  a.textContent = "📊 Analytics";
  a.title = "Private GoatCounter dashboard · add #stats-off to hide";
  a.style.cssText =
    "position:fixed;right:12px;bottom:12px;z-index:1000;" +
    "background:#1a1a1a;color:#fff;text-decoration:none;" +
    "font:600 12px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;" +
    "padding:8px 12px;border-radius:20px;box-shadow:0 2px 6px rgba(0,0,0,.3)";
  a.onmouseenter = function () { a.style.background = "#c5050c"; };
  a.onmouseleave = function () { a.style.background = "#1a1a1a"; };
  document.body.appendChild(a);
})();
