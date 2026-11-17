/**
 * auto-toggle-sidebar.js — 子页面默认收起左侧边栏
 *
 * 本脚本在 <head> 中执行（html_js_files），于首帧渲染前给 <html> 打上
 * sidebar-auto-hidden 标记；tufte.css 据此在桌面端（≥960px）把左侧边栏
 * 初始渲染为收起状态，避免「先显示、再滑走」的加载闪烁。
 *
 * 为什么不用点击 .sidebar-toggle 的方案：
 *   pydata-sphinx-theme 的复选框在移动端是「勾选 = 打开抽屉」，而
 *   sphinx-book-theme 在桌面端又是「勾选 = 隐藏边栏」，语义相反。
 *   点击隐藏复选框在移动端反而会把抽屉打开。改为纯 CSS 标记方案后：
 *     - 桌面端子页面：默认收起，顶栏按钮可随时展开（带过渡动画）；
 *     - 移动端：抽屉默认关闭（checkbox 未勾选），不受影响；
 *     - 首页/章节 hub 页：桌面端保持边栏可见（不加标记即可）。
 */
(function () {
  "use strict";

  var path = window.location.pathname;

  // 首页与章节 hub 页（*/index.html）视为「首页」：桌面端保留边栏。
  // 其余子页面一律自动收起。
  var isHomepage = path === "/" || path.endsWith("index.html");

  if (!isHomepage) {
    document.documentElement.classList.add("sidebar-auto-hidden");
  }
})();
