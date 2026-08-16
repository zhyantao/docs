# JavaScript

## 基本语法

### 变量声明

JavaScript 作为运行在浏览器上的脚本语言，其设计初衷很简单，没想到后来发展的这么好。
所以一开始的设计有很多地方都不太合理，主要体现在作用域上。

JavaScript 声明变量的方式有三种，分别是 `var`、`let`、`const`。

`var` 是旧脚本中使用的变量声明的方式，现在编程一般不再用这个关键字了，它会引起很多问题。

- 用 `var` 声明的变量不是函数作用域就是全局作用域，没有块级作用域的概念；
- 用 `var` 声明的变量，可以重复声明；
- 用 `var` 声明的变量，可以在其声明语句前被使用。

在浏览器中，除非我们使用 `modules`，否则使用 `var` 声明的全局函数和变量会成为全局对象的属性。
因此如果是多人合作开发项目，很容易给环境造成污染。所以，现在已经基本上抛弃用 `var` 来声明变量了。

ES6 对 `var` 存在的问题进行改进，引入了 `let` 关键字。

如果变量声明后不允许修改的话可以用 `const`。

### 作用域

函数作用域、块级作用域、全局作用域。

在 ES5 中可以用大括号 `{...}` 括起来一组语句，作为一个区块，但是它却没有自己的作用域。
到了 ES6，用 `{...}` 括起来的部分就可以作为一个块级作用域了。

- 在块级作用域**内**声明的变量，只能在代码块中可见，出了区块就不能看见了。
- 在块级作用域**外**声明的变量，在代码块中可见。

这种块级作用域对于使用很有用。
需要注意的是特殊情况是，对于 `if`、`while`、`for`、`function` 等语法，比如下面这个代码块：
虽然变量 `i` 在 `{...}` 外面，但是在代码块中是可见的。

```{code-block} js
for (let i; i < 10; i++) {
    ...
}
```

关于更多细节，需要参考 <https://zh.javascript.info/closure>。

### 注释

在 JavaScript 中，分别用 `//` 和 `/** */` 进行行注释和块注释。

### 条件语句

用 `===` 表示判断

### 循环语句

用 `for...of` 遍历对象或数组比用 `for...in` 要更加简洁。

当然最笨的方法还是 `for...i` 的方式。

### 模块

引入模块语法，一个很重要的原因是 ES5 中没有作用域的概念，导致变量很容易被污染。

基本写法：

```{code-block} javascript
const module1 = new Object({
    _count : 0,
    m1 : function (){
        //...
    },
    m2 : function (){
        //...
    }
});
```

关于区块语法，需要进一步学习和补充，参考 <https://zh.javascript.info/modules-intro>。

## 数据类型

### 空值

null（0）、undefined（NaN）

### 数值

注意：`1 === 1.0 // true`，JS 中默认都是浮点数

常用函数：

- `parseInt()`
- `parseFloat()`
- `Boolean()`
- `isFinite()`
- `isNaN()`

### 字符串

建议统一使用单引号。

索引示例：`'hello'[1] // e`

JS 默认编码是 Unicode

Base64 编码和 ASCII 码的相互转换（不支持非 ASCII 码）：

- `btoa()`
- `atob()`

Tips：ES6 在表示字符串时，如果用反引号，可以分多行写一个字符串，但是单引号和双引号不行。

### 对象

格式：`{键值对的集合}`

Key 又叫属性，Value 可以是任意数据类型。

建议不要用 with 语句，因为它没有对作用域做清晰划分。

### 函数

函数的三种表达方法：

1. 普通表示：`function f() {}`
2. 匿名函数：`const f = function() {}`
3. 箭头函数：`const f = () => {}`

函数参数可以传值也可以传址。

闭包：解决 `var` 的作用域问题。
在函数内再定义一个函数，内部函数可以访问外部函数定义的变量。

立即调用函数：`(function() {})()`

### 数组

格式：`[]`

本质是特殊的对象。因此数组中的元素可以是任意数据类型。

数组中的可以含有空位：`[1, ,3]`

## 语法专题

### 数据类型的转换

`Number()`、`String()`、`Boolean()`

### 错误处理机制

`const err = new Error('错误提示');`

六种错误：

- SyntaxError
- ReferenceError：引用不存在的变量
- RangeError：数组或堆栈越界
- TypeError
- URIError
- EvalError：eval 中的函数没有正常执行

`throw new Error('错误提示');`

`try...catch...finally`

## 标准库

### Object 对象

凡是定义在 Object.prototype 对象上的属性和方法，将被所有实例对象共享

### JSON 对象

是一个值，且只能值一个值。

### 属性描述对象

一种内部数据结构，用来描述对象的属性，控制它的行为。比如该属性是否可写、可遍历等等。

### Array 对象

用于数组。

### 包装对象

常用的包装对象有：

- Boolean 对象。
- Number 对象
- String 对象

### RegExp 对象

提供正则表达式功能。

## 面向对象编程

JavaScript 语言的对象体系，不是基于 "类" 的，而是基于构造函数（constructor）和原型链（prototype）。

### 基本使用

ES5 声明类的模板：`const V = function() {this.a = 100;}` 跟普通函数的写法无异。ES6 有了 `class` 关键字。

使用 "类" 的模板创建对象：`const v = new V();`

`this` 指向当前对象。

### 继承

每一个函数都有 `prototype` 属性，指向一个对象：意思是继承这个对象。

所有对象都有自己的原型对象（`prototype`）。

用 `prototype` 属性定义的方法或属性，将被子类共享。

将 `prototype.constructor` 指向自己以声明默认构造函数。

## 异步操作

JavaScript 现在采用单线程模型，将来也是。

AJAX = Asynchronous JavaScript and XML（异步的 JavaScript 和 XML）。
AJAX 最大的优点是在不重新加载整个页面的情况下，可以与服务器交换数据并更新部分网页内容。

### 异步操作的模式

回调函数：（意思是，我们在别的地方把函数定义好了，现在需要用到这个函数直接调用就好了）

```{code-block} javascript
function f1 (callback) {
    callback(); // 执行 callback 函数
}
```

事件监听：

```{code-block} javascript
f1.on('done', f2) // 如果 f1 执行完了，就开始执行 f2
```

发布/订阅：

```{code-block} javascript
jQuery.subscribe('done', f2)
```

### 异步操作的流程控制

串行执行：递归调用

并行执行：`items.forEach() {}`

串行和并行混合

### 定时器

`setTimeout()`：设定一段时间后执行某个函数

`setInterval()`：设定每隔一段时间执行某个函数，无限循环

`clearTimeout()`

`clearInterval()`

`debounce()`：防止用户在一段时间内重复提交

### Promise 对象

JavaScript 的异步操作解决方案，为异步操作提供统一接口。

`Promise` 是一个对象，也是一个构造函数。

优点：用 `then` 方法，像写同步操作一样编写异步操作。

`(new Promise(f1)).then(f2).then(f3);`

`then()` 用法解析：[Ref](https://wangdoc.com/javascript/async/promise.html#then-%E7%94%A8%E6%B3%95%E8%BE%A8%E6%9E%90)

## DOM

- **Node 接口**：所有 DOM 节点的基类，提供 `nodeType`、`nodeName`、`parentNode`、`appendChild()`、`removeChild()` 等通用属性和方法。
- **NodeList 接口、HTMLCollection 接口**：节点集合。`querySelectorAll()` 返回静态 NodeList；`getElementsByTagName()` 等返回实时的 HTMLCollection。
- **ParentNode 接口、ChildNode 接口**：父节点提供 `children`、`querySelector()` 等查询子节点的能力；子节点提供 `remove()`、`before()`、`after()` 等操作自身位置的方法。
- **Document 接口**：代表整个文档，是 DOM 的入口。`document.getElementById()`、`document.createElement()`、`document.querySelector()` 都定义在这里。
- **Element 接口**：元素节点，提供 `className`、`innerHTML`、`getAttribute()`/`setAttribute()` 等属性和方法。
- **属性操作**：`getAttribute()`、`setAttribute()`、`hasAttribute()`、`removeAttribute()`；标准属性（如 `id`、`href`）也可通过元素对象的同名属性直接读写。
- **Text 节点、DocumentFragment 节点**：Text 是文本节点；DocumentFragment 是轻量容器，批量插入节点时先挂到它上面再一次性插入，可以避免多次重排。
- **CSS 操作**：通过 `element.style.xxx` 修改内联样式，通过 `element.classList.add()/remove()/toggle()` 切换类名，通过 `getComputedStyle()` 读取最终样式。
- **Mutation Observer API**：监听 DOM 结构变化（子节点增删、属性修改等），是旧 MutationEvent 的替代方案。

## 事件

- **EventTarget 接口**：事件机制的基础，提供 `addEventListener()`、`removeEventListener()`、`dispatchEvent()`。DOM 节点、`window`、`XMLHttpRequest` 等都实现了它。
- **事件模型**：事件分为三个阶段——捕获（capture）→ 目标（target）→ 冒泡（bubble）；`addEventListener(type, fn, useCapture)` 的第三个参数决定监听阶段。
- **Event 对象**：事件处理函数的参数，包含 `type`、`target`、`currentTarget`、`preventDefault()`、`stopPropagation()` 等属性和方法。
- **鼠标事件**：`click`、`dblclick`、`mousedown`、`mouseup`、`mousemove`、`mouseover`、`mouseout`、`contextmenu` 等。
- **键盘事件**：`keydown`、`keypress`、`keyup`，事件对象带有 `key`、`keyCode` 属性。
- **进度事件**：`load`、`error`、`abort`、`progress`，常用于图片、脚本、AJAX 等资源加载场景。
- **表单事件**：`submit`、`change`、`input`、`focus`、`blur`、`reset`。
- **触摸事件**：`touchstart`、`touchmove`、`touchend`、`touchcancel`，用于移动端。
- **拖拉事件**：`dragstart`、`drag`、`dragend`、`dragover`、`drop` 等，配合 `dataTransfer` 对象传递数据。
- **其他常见事件**：`scroll`、`resize`、`copy`/`cut`/`paste`、`hashchange`、`DOMContentLoaded`。
- **GlobalEventHandlers 接口**：定义在 `HTMLElement` 等元素上的 `onclick`、`onload` 等事件处理属性，是"属性赋值"风格的事件绑定。

## 浏览器模型

- **window 对象**：全局对象，既是 JS 代码的顶层作用域，也代表浏览器窗口，提供 `alert()`、`setTimeout()`、`location`、`history` 等成员。
- **Navigator 对象、Screen 对象**：`navigator` 提供浏览器和操作系统信息（如 `userAgent`）；`screen` 提供屏幕尺寸、分辨率等信息。
- **Cookie**：浏览器端的小型键值存储，随 HTTP 请求自动发送给服务器；用 `document.cookie` 读写，有大小（约 4KB）和数量限制。
- **XMLHttpRequest 对象**：传统的 AJAX 实现，通过 `open()`、`send()` 发起 HTTP 请求，用 `onreadystatechange`/`onload` 处理响应。
- **同源限制**：协议、域名、端口完全一致才算同源。跨源时脚本无法读取对方页面的 DOM、Cookie 和 AJAX 响应，是浏览器最重要的安全机制之一。
- **CORS 通信**：跨源资源共享。服务器通过 `Access-Control-Allow-Origin` 等响应头声明允许哪些源访问，浏览器据此放行跨源请求。
- **Storage 接口**：`localStorage`（永久保存）和 `sessionStorage`（会话级），都是键值对形式的本地存储，容量约 5MB。
- **History 对象**：管理浏览器历史记录，`pushState()`/`replaceState()` 可以实现无刷新的 URL 更新（SPA 路由的基础）。
- **Location 对象、URL 对象、URLSearchParams 对象**：`location` 代表当前页面地址，可跳转；`URL` 用于解析/构造 URL；`URLSearchParams` 用于方便地操作查询字符串。
- **ArrayBuffer 对象、Blob 对象、File 对象**：`ArrayBuffer` 是底层二进制缓冲区；`Blob` 是不变的二进制大对象；`File` 继承自 `Blob`，增加了文件名等信息。
- **FileList 对象、FileReader 对象**：`<input type="file">` 的 `files` 属性返回 FileList；`FileReader` 用于异步读取文件内容（文本、DataURL、ArrayBuffer）。
- **表单、FormData 对象**：`FormData` 以键值对收集表单数据，可以直接作为 `fetch()`/`XMLHttpRequest` 的请求体（multipart/form-data）。
- **IndexedDB API**：浏览器内置的 NoSQL 数据库，支持索引和事务，容量远大于 localStorage，适合存储大量结构化数据。

Web Worker

---

1. JavaScript 基础教程 <https://wangdoc.com/javascript/>
2. 现代 JavaScript 教程 <https://zh.javascript.info/>
3. JavaScript 思维导图 <https://kdocs.cn/l/cqVRohCmQWBZ>
