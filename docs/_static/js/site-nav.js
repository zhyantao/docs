/**
 * site-nav.js — 在页面顶部注入跨站导航条（与 zhyantao.github.io 各站页眉一致）
 * 站点：ZHYANTAO / DOCS / PS1 / CALLGRAPH / RISC-V / BOT
 */
(function () {
  "use strict";

  var SITES = [
    { href: "https://zhyantao.github.io/", label: "ZHYANTAO" },
    { href: "https://zhyantao.github.io/docs/", label: "DOCS", active: true },
    { href: "https://zhyantao.github.io/PS1-generator/", label: "PS1" },
    { href: "https://zhyantao.github.io/callgraphs-generator/", label: "CALLGRAPH" },
    { href: "https://zhyantao.github.io/riscv-bitlab/", label: "RISC-V" },
    { href: "https://zhyantao.github.io/trading/", label: "BOT" },
  ];

  function build() {
    if (document.querySelector(".site-nav")) return;

    var nav = document.createElement("nav");
    nav.className = "site-nav";
    nav.setAttribute("aria-label", "站点导航");

    var inner = document.createElement("div");
    inner.className = "site-nav-inner";

    SITES.forEach(function (site) {
      var a = document.createElement("a");
      a.href = site.href;
      a.textContent = site.label;
      if (site.active) a.className = "active";
      inner.appendChild(a);
    });

    nav.appendChild(inner);

    // 插到页面最顶部（原有主题导航条在它下方）
    document.body.insertBefore(nav, document.body.firstChild);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
