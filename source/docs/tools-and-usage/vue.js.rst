============
Vue.js 入门
============

Vue.js 是一个用于创建用户界面的开源 JavaScript 框架，也是一个创建单页应用的 Web 应用框架，能够简化 Web 开发。
Vue 所关注的核心是 MVC 模式中的视图层，同时，它也能方便地获取数据更新，并通过组件内部特定的方法实现视图与模型的交互。

Vue 主要特性包括：

- 组件：组件是基础 `HTML 元素 <https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element>`_\ 的扩展，可以方便地自定义其\ **数据**\ 与\ **行为**\ 。
- 模板：使用基于 `HTML 模板 <https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/template>`_\ 语法，可以将 `DOM <https://developer.mozilla.org/zh-CN/docs/Web/API/Document_Object_Model/Introduction>`_ 元素与底层 `Vue 实例 <https://cn.vuejs.org/v2/guide/instance.html>`_\ 中的数据\ **绑定**\ 。满足响应式设计。
- 响应式设计：在视图与对应的模型绑定后，Vue **自动观测模型的变动**\ ，并重新绘图。
- 过渡效果：Vue 在插入、更新或者移除 DOM 时，提供多种不同方式的应用过渡效果。
- 单文件组件：为了更好地适应复杂的项目，Vue 支持以 ``.vue`` 为扩展名的文件来定义一个完整组件，用以替代使用 ``Vue.component`` 注册组件的方式。

学习目标
~~~~~~~~

以\ `凤凰架构 <http://icyfenix.cn/>`_\ 为例，学习其\ `前端 <https://bookstore.icyfenix.cn/#/>`_\ 构建方式，达到能够复现的程度就可以了。\ `前端工程源代码 <https://github.com/fenixsoft/fenix-bookstore-frontend>`_\ 的目录结构如下：

.. code-block:: text

    fenix-bookstore-frontend
    +---build                   webpack 编译配置，该目录的内容一般不做改动
    +---config                  webpack 编译配置，用户需改动的内容提取至此
    +---dist                    编译输出结果存放的位置
    +---markdown                与项目无关，用于支持 markdown 的资源（如图片）
    +---src
    |   +---api                 本地与远程的 API 接口
    |   |   +---local           本地服务，如 localStorage、加密等
    |   |   +---mock            远程 API 接口的 Mock
    |   |   |   \---json        Mock 返回的数据
    |   |   \---remote          远程服务
    |   +---assets              资源文件，会被 webpack 哈希和压缩
    |   +---components          vue.js 的组件目录，按照使用页面的结构放置
    |   |   +---home
    |   |   |   +---cart
    |   |   |   +---detail
    |   |   |   \---main
    |   |   \---login
    |   +---pages               vue.js 的视图目录，存放页面级组件
    |   |   \---home
    |   +---plugins             vue.js 的插件，如全局异常处理器
    |   +---router              vue-router 路由配置
    |   \---store               vuex 状态配置
    |       \---modules         vuex 状态按名空间分隔存放
    \---static                  静态资源，编译时原样打包，不会做哈希和压缩


基本使用
~~~~~~~~

一般流程是：

- 在 template 中声明一个模块
- 在 script 中提供注册和绑定
- 在 style 中编写样式说明

安装 Vue.js
------------

在项目中安装 Vue.js 只需要下载 `vue.js <https://vuejs.org/js/vue.js>`_ 然后，用代码引入就可以了。

.. code-block:: html

    <script src="vue.js" type="text/javascript" charset="utf-8"></script>






