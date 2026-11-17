/**
 * auto-toggle-sidebar.js — 子页面默认收起左侧边栏，并记住会话内的手动开关
 *
 * 在 <head> 中执行（html_js_files），首帧渲染前决定边栏初始状态，
 * 避免「先显示、再滑走」的加载闪烁：
 *
 *   1. 会话状态优先：用户手动开/关过边栏（sessionStorage["sidebar-state"]）
 *      后，点上一页/下一页跳转时沿用该状态，边栏不再跳变；
 *   2. 否则默认行为：只有站点根首页显示边栏，其余页面（含章节 hub 页）
 *      一律默认收起 —— 阅读链路里边栏状态保持稳定。
 *
 * 实现说明：
 *   - checkbox 在 body 里，head 阶段取不到，所以先用 html 标记类完成
 *     首帧布局；DOMContentLoaded 时再同步 checkbox 并撤掉占位类，
 *     同步期间由 sidebar-pretransition 关闭过渡，视觉上无缝；
 *   - 主题的按钮点击处理器直接翻转 checkbox（不触发 change 事件），
 *     因此额外监听按钮 click，在主题处理器之后读取最终状态并持久化。
 */
(function () {
  "use strict";

  var parts = window.location.pathname.split("/").filter(Boolean);
  // 根首页："/"、"/index.html"，或部署在子路径下的 "/docs/"、"/docs/index.html"
  var isRootHome =
    parts.length <= 1 || (parts.length === 2 && parts[1] === "index.html");

  var stored = null;
  try {
    stored = sessionStorage.getItem("sidebar-state");
  } catch (e) {
    /* storage 不可用时回退到默认行为 */
  }

  var root = document.documentElement;
  if (stored === "open") {
    // sidebar-open 是首帧占位（可见）；sidebar-auto-hidden 保证同步后
    // 按钮可用、未勾选时可收起；pretransition 关闭同步期的过渡动画
    root.classList.add("sidebar-open", "sidebar-auto-hidden", "sidebar-pretransition");
  } else if (stored === "closed" || !isRootHome) {
    root.classList.add("sidebar-auto-hidden");
  }

  function onReady() {
    var cb = document.getElementById("pst-primary-sidebar-checkbox");
    var desktop = window.matchMedia("(min-width: 960px)").matches;

    // 会话状态为「打开」时同步 checkbox（桌面端），随后撤掉占位类：
    // 勾选状态与占位样式一致，且过渡被暂时关闭，切换无动画
    if (cb && desktop && stored === "open") {
      cb.checked = true;
    }
    root.classList.remove("sidebar-open");

    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        root.classList.remove("sidebar-pretransition");
      });
    });

    if (cb) {
      var persist = function () {
        try {
          sessionStorage.setItem(
            "sidebar-state",
            cb.checked ? "open" : "closed",
          );
        } catch (e) {}
      };
      // 移动端遮罩（label）点击 → 原生翻转 checkbox，触发 change
      cb.addEventListener("change", persist);
      // 桌面/移动端按钮点击 → 主题处理器直接翻转 checkbox（无 change），
      // 在 click 派发结束后（setTimeout）读取最终状态
      document
        .querySelectorAll("button.sidebar-toggle.primary-toggle")
        .forEach(function (btn) {
          btn.addEventListener("click", function () {
            setTimeout(persist, 0);
          });
        });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
