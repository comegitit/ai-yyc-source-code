/*
 * Microsoft Clarity, gated behind a localStorage self-exclusion flag.
 *
 * Toggle on a device that has no dev console (i.e. a phone):
 *   https://ai-yyc.com/?notrack=1   stop tracking this browser
 *   https://ai-yyc.com/?notrack=0   start tracking it again
 * Either one shows a short confirmation so the visit is not ambiguous.
 *
 * The flag is per-browser and per-device, so it has to be set once on each.
 * No IP blocking: the owner's connection is dual-stack and dynamic, and
 * Clarity only matches IPv4, so a block would fail silently half the time.
 */
(function () {
  var p = new URLSearchParams(location.search);
  var toggled = null;

  if (p.get("notrack") === "1") {
    localStorage.setItem("noTrack", "1");
    toggled = "Analytics off for this browser";
  }
  if (p.get("notrack") === "0") {
    localStorage.removeItem("noTrack");
    toggled = "Analytics on for this browser";
  }

  if (toggled) {
    var show = function () {
      var el = document.createElement("div");
      el.textContent = toggled;
      el.setAttribute("role", "status");
      el.style.cssText =
        "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:9999;" +
        "max-width:90vw;padding:12px 20px;border-radius:6px;background:#1a1a1a;color:#fff;" +
        "font:16px/1.4 system-ui,sans-serif;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.3);";
      document.body.appendChild(el);
      setTimeout(function () {
        el.remove();
      }, 3000);
    };
    if (document.body) {
      show();
    } else {
      document.addEventListener("DOMContentLoaded", show);
    }
  }

  if (localStorage.getItem("noTrack")) return;

  // Clarity's vendor snippet, unmodified.
  (function (c, l, a, r, i, t, y) {
    c[a] =
      c[a] ||
      function () {
        (c[a].q = c[a].q || []).push(arguments);
      };
    t = l.createElement(r);
    t.async = 1;
    t.src = "https://www.clarity.ms/tag/" + i;
    y = l.getElementsByTagName(r)[0];
    y.parentNode.insertBefore(t, y);
  })(window, document, "clarity", "script", "yiw91bgryt");
})();
